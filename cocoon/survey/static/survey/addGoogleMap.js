/**
 * Created by awagu on 12/22/2016.
 */

var map;
var markers = [];
var MAPZOOM = 12;
var MAXZOOM = 13;

/**
 * function required by google maps api for initialization
 */
function initMap() {
	var mapDiv = document.getElementById('map');
	map = new google.maps.Map(mapDiv, {
		center: {lat:42.3601, lng: -71.0589},
		zoom: MAPZOOM,
        maxZoom: MAXZOOM
	});
	//distanceMatrix();
	var geocoder = new google.maps.Geocoder();
	for(i=0; i<myStreetAddresses.length;i++)
    {
	    addDestMarkers(geocoder, map, myStreetAddresses[i]);
    }
    // The destinations need to have the lat long because
    // Otherwise the geocoding goes over the limit
	for(i=0;i<myLocations.length; i++)
	{
        addLocationMarkers(map, myLocations[i]);
    }

}

// Adds a marker to the map and push to the array.
/**
 * Adds a marker to the map after initialization
 *
 * Note: Deprecated.
 *
 * @param address - location to add the new pin
 */
function addChosenMarker(address) {
    deleteMarkers();
    var geocoder = new google.maps.Geocoder();
    var marker;
    geocoder.geocode({'address': address},
        function (results, status) {
            if (status == 'OK') {
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    icon: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
                    zIndex: google.maps.Marker.MAX_ZINDEX + 1,
                });
                console.log(results);
                markers.push(marker);
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setMapOnAll(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}