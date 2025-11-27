# Utilized Gen A.I. to upack and structure the json data in this class.
class FlightData:
    def __init__(self, dm_data, search_flight_data):
        self.flight_data = search_flight_data.flight_data
        self.ama_flight_offers = []
        self.ama_itineraries = []
        self.offer_messages = []
        self.flight_offers = []
        self.itineraries = []
        self.structured_flights = []

        if self.flight_data and len(self.flight_data) > 0:
            flight_response = self.flight_data[0]
            try:
                if flight_response['data']:  # Check if there are flight offers
                    try:
                        # Extract price and itinerary from the first flight offer
                        offer = flight_response['data'][0]
                        self.ama_flight_offers.append(float(offer['price']['grandTotal']))
                        self.ama_itineraries.append(offer['itineraries'])

                        # Since we found offers, add them to the main lists
                        self.flight_offers.append(float(offer['price']['grandTotal']))
                        self.itineraries.append(offer['itineraries'])

                        # Create structured data for HTML template
                        self.create_structured_data(offer, flight_response)

                    except (IndexError, KeyError) as e:
                        print(f"Error extracting flight data: {e}")
                        self.flight_offers.append("No offers found")
                else:
                    self.flight_offers.append("No flight offers available")
            except (IndexError, KeyError, TypeError) as e:
                print(f"Error extracting flight data: {e}")
                self.flight_offers.append("No offers found")
        else:
            self.flight_offers.append("No flight data available")

        # Formatting the offers into messages to send
        self.create_messages(flight_response)

    def create_structured_data(self, offer, flight_response):
        """Create structured data for easy HTML template usage"""
        outbound_itinerary = offer['itineraries'][0]
        return_itinerary = offer['itineraries'][1]

        # Outbound flight details
        outbound_segment = outbound_itinerary['segments'][0]
        outbound_departure = outbound_segment['departure']
        outbound_arrival = outbound_segment['arrival']

        # Return flight details
        return_segment = return_itinerary['segments'][0]
        return_departure = return_segment['departure']
        return_arrival = return_segment['arrival']

        # Get airline and aircraft info from dictionaries
        carrier_code = outbound_segment['carrierCode']
        airline_name = flight_response['dictionaries']['carriers'].get(carrier_code, carrier_code)
        aircraft_code = outbound_segment['aircraft']['code']
        aircraft_name = flight_response['dictionaries']['aircraft'].get(aircraft_code, aircraft_code)

        flight_info = {
            'price': float(offer['price']['grandTotal']),
            'currency': offer['price']['currency'],
            'airline': airline_name,
            'aircraft': aircraft_name,
            'seats_available': offer['numberOfBookableSeats'],
            'travel_class': offer['travelerPricings'][0]['fareDetailsBySegment'][0]['cabin'],
            'outbound': {
                'departure_airport': outbound_departure['iataCode'],
                'arrival_airport': outbound_arrival['iataCode'],
                'departure_time': outbound_departure['at'],
                'arrival_time': outbound_arrival['at'],
                'departure_date': outbound_departure['at'].split("T")[0],
                'departure_time_only': outbound_departure['at'].split("T")[1],
                'arrival_date': outbound_arrival['at'].split("T")[0],
                'arrival_time_only': outbound_arrival['at'].split("T")[1],
                'duration': outbound_itinerary['duration'],
                'flight_number': f"{outbound_segment['carrierCode']} {outbound_segment['number']}"
            },
            'return_flight': {
                'departure_airport': return_departure['iataCode'],
                'arrival_airport': return_arrival['iataCode'],
                'departure_time': return_departure['at'],
                'arrival_time': return_arrival['at'],
                'departure_date': return_departure['at'].split("T")[0],
                'departure_time_only': return_departure['at'].split("T")[1],
                'arrival_date': return_arrival['at'].split("T")[0],
                'arrival_time_only': return_arrival['at'].split("T")[1],
                'duration': return_itinerary['duration'],
                'flight_number': f"{return_segment['carrierCode']} {return_segment['number']}"
            }
        }

        self.structured_flights.append(flight_info)

    def create_messages(self, flight_response):
        """Create formatted messages"""
        for x in range(len(self.itineraries)):
            # Two itineraries: outbound and return
            outbound_itinerary = self.itineraries[x][0]  # First itinerary (outbound)
            return_itinerary = self.itineraries[x][1]  # Second itinerary (return)

            # Outbound flight details
            outbound_segment = outbound_itinerary['segments'][0]
            outbound_departure = outbound_segment['departure']
            outbound_arrival = outbound_segment['arrival']

            outbound_departure_date = outbound_departure['at'].split("T")[0]
            outbound_departure_time = outbound_departure['at'].split("T")[1]
            outbound_arrival_date = outbound_arrival['at'].split("T")[0]
            outbound_arrival_time = outbound_arrival['at'].split("T")[1]

            # Return flight details
            return_segment = return_itinerary['segments'][0]
            return_departure = return_segment['departure']
            return_arrival = return_segment['arrival']

            return_departure_date = return_departure['at'].split("T")[0]
            return_departure_time = return_departure['at'].split("T")[1]
            return_arrival_date = return_arrival['at'].split("T")[0]
            return_arrival_time = return_arrival['at'].split("T")[1]

            # Get airline and aircraft info from dictionaries
            carrier_code = outbound_segment['carrierCode']
            airline_name = flight_response['dictionaries']['carriers'].get(carrier_code, carrier_code)
            aircraft_code = outbound_segment['aircraft']['code']
            aircraft_name = flight_response['dictionaries']['aircraft'].get(aircraft_code, aircraft_code)

            message = (
                f"✈️ Flight Deal Alert! ✈️\n"
                f"Price: R{self.flight_offers[x]}\n"
                f"Airline: {airline_name}\n"
                f"Aircraft: {aircraft_name}\n\n"
                f"Outbound Flight:\n"
                f"• {outbound_departure['iataCode']} → {outbound_arrival['iataCode']}\n"
                f"• Depart: {outbound_departure_date} at {outbound_departure_time}\n"
                f"• Arrive: {outbound_arrival_date} at {outbound_arrival_time}\n"
                f"• Duration: {outbound_itinerary['duration']}\n\n"
                f"Return Flight:\n"
                f"• {return_departure['iataCode']} → {return_arrival['iataCode']}\n"
                f"• Depart: {return_departure_date} at {return_departure_time}\n"
                f"• Arrive: {return_arrival_date} at {return_arrival_time}\n"
                f"• Duration: {return_itinerary['duration']}\n\n"
            )

            self.offer_messages.append(message)

        # for x in self.offer_messages:
        #     print(x)
        #     print("-" * 50)
