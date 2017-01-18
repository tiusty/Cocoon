/**
 * Created by awagu on 12/22/2016.
 */
function initMap() {
	var mapDiv = document.getElementById('map');
	var map = new google.maps.Map(mapDiv, {
		center: {lat:42.3601, lng: -71.0589},
		zoom: 8
	});
	distanceMatrix();
	var geocoder = new google.maps.Geocoder();
	addMarkers(geocoder, map, myStreetAddress);
	for(i=0;i<myDestinations.length; i++)
	{
        addMarkers(geocoder, map, myDestinations[i]);
    }
}