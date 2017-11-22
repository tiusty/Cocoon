import googlemaps
import json
from urllib import request

class maps_requester:

    maps = "https://maps.googleapis.com/maps/api/geocode/json?address="

    def __init__(self, key):
        self.key = "&key=" + key


    def get_lat_lon_from_address(self, address):

        param_address = address.replace(' ','+')
        print(param_address)

        with request.urlopen(self.maps + param_address + self.key) as response:
            json_response = response.read()
            map_json = json.loads(json_response)
            print(map_json)

        '''
            if (map_json["status"] != "OK"):
                return -1
            else:
                lat = map_json["geometry"]["location"]["lat"]
                lng = map_json["geometry"]["location"]["lng"]
                return (lat,lng)
        '''