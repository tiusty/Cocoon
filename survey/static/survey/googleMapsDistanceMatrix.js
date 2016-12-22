/**
 * Created by awagu on 12/22/2016.
 */
function distanceMatrix() {

//var origin = 'Greenwich, England';
//var origin = '12 Stony Brook Rd,Arlington MA, USA';
var origin = myStreetAddress;
//var destination = 'Boston, MA';
var destination = myDestination;
var service = new google.maps.DistanceMatrixService();
service.getDistanceMatrix(
{
	origins: [origin],
	destinations: [destination],
	travelMode: 'DRIVING',
	unitSystem: google.maps.UnitSystem.IMPERIAL,
	avoidHighways: false,
	avoidTolls: false,
},function callback(response,status) {
	if(status == 'OK') {
		var origins = response.originAddresses;
		var destinations = response.destinationAddresses;

		for(var i=0; i < origins.length; i++)
			var results = response.rows[i].elements;
			console.log(results);
			for(var j=0; j < results.length; j++) {
				var element = results[j];
				var distance = element.distance.text;
				var duration = element.duration.text;
				var from = origins[i];
				var to = destinations[j];

				document.getElementById('distanceMatrixOrigin').innerHTML = origins;
				document.getElementById("distanceMatrixDestination").innerHTML = destinations;
				document.getElementById("distanceMatrixTimeToDestination").innerHTML = duration;
				document.getElementById("distanceMatrixDistanceToDestination").innerHTML = distance;
			}
		}
	});
}
