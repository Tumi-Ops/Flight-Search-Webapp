from flask import Flask, render_template, redirect, session, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'


class FlightForm(FlaskForm):
    city = StringField('Destination City, e.g. Paris', validators=[DataRequired()])
    origin_location = StringField('Origin City, e.g. Johannesburg', validators=[DataRequired()])
    adults = IntegerField('Adults, e.g. age 12 or older', validators=[NumberRange()])
    children = IntegerField('Children, e.g. ages 2 - 12', validators=[NumberRange()])
    infants = IntegerField('Infants, e.g. ages under 2', validators=[NumberRange()])
    travel_class = SelectField("Travel Class", choices=["ECONOMY",
                                                        "PREMIUM_ECONOMY",
                                                        "BUSINESS", "FIRST"],
                               validators=[DataRequired()])
    departure_date = DateField('Departure Date', validators=[DataRequired()])
    return_date = DateField('Return Date', validators=[DataRequired()])
    submit = SubmitField(label="Check Flights")


@app.route("/", methods=["GET", "POST"])
def home():
    form = FlightForm()
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
    return render_template("index.html", form=form)


@app.route("/flight_results")
def results():
    # Retrieve data from session
    flight_messages = session.get('flight_messages', [])
    structured_flights = session.get('structured_flights', [])
    search_params = session.get('details', {})

    return render_template("results.html",
                           flight_messages=flight_messages,
                           structured_flights=structured_flights,
                           search_params=search_params)


if __name__ == '__main__':
    app.run(debug=True)
