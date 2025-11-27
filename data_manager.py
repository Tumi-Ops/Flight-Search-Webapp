# This class is responsible for retrieving the IATA codes.
import amadeus
import requests

class DataManager:
    def __init__(self):
        self.ama_auth = None
        self.ama_response = None
        self.iata_codes = []

    def get_iata_codes(self, city, og_loc):
        """Gets the cities IATA codes from the Amadeus API"""
        locations = {"from":og_loc, "to": city}
        #Authenticing with the Amadeus
        self.ama_auth = requests.post(url=amadeus.amadeus_token_endpoint, data=amadeus.amadeus_token_params)
        amadeus_cities_header = {
            "accept": "application/vnd.amadeus+json",
            "Authorization": f"{self.ama_auth.json()['token_type']} {self.ama_auth.json()['access_token']}"
        }

        # Adding the found IATA codes to a list
        for x in locations:
            amadeus_cities_params = {"keyword": locations[x], "max": 1, "include": "AIRPORTS"}
            self.ama_response = requests.get(url=amadeus.amadeus_cities_endpoint, params=amadeus_cities_params,
                                             headers=amadeus_cities_header)
            try:
                self.iata_codes.append({x: self.ama_response.json()['data'][0]['iataCode']})
            except KeyError:
                self.iata_codes.append({x: "No IATA code found"})
        print(self.iata_codes)

        # self.iata_codes = [{'from': 'NYC'}, {'to': 'PAR'}]