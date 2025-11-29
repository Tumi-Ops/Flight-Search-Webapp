import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Flightsyte_DynamoDB')

def add_flight(email, username, destination, origin, max_price, adults, children, infants, from_date, to_date):
    table.put_item(
        Item={
            'email': email,
            'username': username,
            'destination_city': destination,
            'origin_location': origin,
            'max_price': max_price,
            'adults': adults,
            'children': children,
            'infants': infants,
            'from_date': str(from_date),
            'to_date': str(to_date)
        }
    )

def read_flights(email, username):
    response = table.get_item(
        Key={
            'email': email,
            'username': username
        }
    )
    item = response['Item']
    return item