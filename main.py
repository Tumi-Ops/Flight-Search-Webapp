import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, session, url_for, flash
from aws_dynamodb import table, add_flight
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from flight_form import FlightForm, TripAlertForm
from flask_bootstrap import Bootstrap5
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
Bootstrap5(app)
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.secret_key = os.urandom(24)

# For Signup and Login
oauth = OAuth(app)
oauth.register(
    name='oidc',
    authority='https://cognito-idp.eu-north-1.amazonaws.com/eu-north-1_qYg5i82HT',
    client_id=os.environ["COGNITO_CLIENT_ID"],
    client_secret=os.environ["COGNITO_CLIENT_SECRET"],
    server_metadata_url='https://cognito-idp.eu-north-1.amazonaws.com/eu-north-1_qYg5i82HT/.well-known/openid-configuration',
    client_kwargs={'scope': 'phone openid email'}
)


##########

@app.route("/login", methods=["GET", "POST"])
def login():
    return oauth.oidc.authorize_redirect('http://localhost:5000/authorize')


@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route("/", methods=["GET", "POST"])
def home():
    form = FlightForm()
    user = session.get('user')

    if user:
        if form.validate_on_submit():
            data_manage = DataManager()
            data_manage.get_iata_codes(city=form.city.data, og_loc=form.origin_location.data)

            fly_search = FlightSearch(data_manage)
            fly_search.get_flights(dep_date=form.departure_date.data,
                                   ret_date=form.return_date.data, ad=form.adults.data,
                                   child=form.children.data, inf=form.infants.data, tc=form.travel_class.data)

            fly_data = FlightData(data_manage, fly_search)

            session['flight_messages'] = fly_data.offer_messages
            session['structured_flights'] = fly_data.structured_flights
            session['details'] = {
                'origin': form.origin_location.data,
                'destination': form.city.data,
                'adults': form.adults.data,
                'children': form.children.data,
                'infants': form.infants.data,
                'travel_class': form.travel_class.data,
                'departure_date': form.departure_date.data.strftime('%Y-%m-%d'),
                'return_date': form.return_date.data.strftime('%Y-%m-%d')
            }
            return redirect(url_for('results'))
    if request.method == 'POST' and not user:
        flash("You must be logged in before searching for flights.", "danger")
    return render_template("index.html", form=form, user=user, active_page="home")


@app.route("/flight_results")
def results():
    # Retrieve data from session
    flight_messages = session.get('flight_messages', [])
    structured_flights = session.get('structured_flights', [])
    search_params = session.get('details', {})
    return render_template("results.html",
                           flight_messages=flight_messages,
                           structured_flights=structured_flights,
                           search_params=search_params, user=session.get('user'))


@app.route("/trip_alert", methods=["GET", "POST"])
def trip_alert():
    form = TripAlertForm()
    user = session.get('user')

    if user:
        email = user['email']
        if form.validate_on_submit():
            try:
                add_flight(email, str(datetime.now()), form.destination_city.data, form.origin_location.data,
                           form.max_price.data, form.adults.data, form.children.data,
                           form.infants.data, str(form.from_date.data), str(form.to_date.data))
                flash(f"Trip set successfully! You will be notified by email when it is found! "
                      f"\nCheck the 'Live Trips' tab, to view your trip.", "success")
            except Exception as e:
                flash(f"Error: {e}")

    if request.method == 'POST' and not user:
        flash("You must be logged in before creating alerts for flights.", "danger")
    return render_template("trip_alert.html", active_page="trip_alert", form=form, user=session.get('user'))

@app.route("/pricing")
def pricing():
    return render_template("pricing.html", active_page="pricing", user=session.get('user'))


@app.route("/faq")
def faq():
    return render_template("faq.html", active_page="faq", user=session.get('user'))


@app.route("/about")
def about():
    return render_template("about.html", active_page="about", user=session.get('user'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
