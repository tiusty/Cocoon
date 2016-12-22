/**
 * Created by awagu on 12/22/2016.
 */
function addMarkers(geocoder, resultsMap, myAddress)
{
	var address = myAddress;
	geocoder.geocode({'address': address},
	function(results, status)
	{
		if (status=='OK')
		{
			var marker = new google.maps.Marker({
				map: resultsMap,
				position: results[0].geometry.location
			});
		} else {
			alert('Geocode was not successful for the following reason: ' + status);
		}
	});
}