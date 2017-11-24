import googlemaps
import json
from urllib import request,error

class maps_requester:

    maps = "https://maps.googleapis.com/maps/api/geocode/json?address="

    def __init__(self, key):
        self.key = "&key=" + key


    '''
    gets latitude and longitude from an address
    using google maps api
    @params
        address - address to locate
    '''
    def get_lat_lon_from_address(self, address):

        param_address = address.replace(' ','+')
        print(param_address)

        # TODO: Error check this request
        with request.urlopen(self.maps + param_address + self.key) as response:
            json_response = response.read()
            map_json = json.loads(json_response)

            # print(map_json["results"][0])

            if (map_json["status"] != "OK"):
                return -1
            else:
                #print(map_json["results"][0]["geometry"]["location"])
                lat = map_json["results"][0]["geometry"]["location"]["lat"]
                lng = map_json["results"][0]["geometry"]["location"]["lng"]
                return (lat,lng)

