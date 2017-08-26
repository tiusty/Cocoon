/**
 * Created by awagu on 12/22/2016.
 */

// Theses are markers that mark the destinations that the user wants to work/live at
function addDestMarkers(geocoder, resultsMap, myAddress)
{
	var address = myAddress;
	geocoder.geocode({'address': address},
	function(results, status)
	{
        if (status == 'OK') {
            var image = {
                url: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
                // This marker is 20 pixels wide by 32 pixels high.
                size: new google.maps.Size(20, 32),
                // The origin for this image is (0, 0).
                origin: new google.maps.Point(0, 0),
                // The anchor for this image is the base of the flagpole at (0, 32).
                anchor: new google.maps.Point(0, 32)
            };
            var marker = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location,
				icon: image
            });

		} else {
			alert('Geocode was not successful for the following reason: ' + status);
		}
	});
}
//These are markers that mark the locations that the user could live in aka housingList
function addLocationMarkers(resultsMap, pin)
{
	var latlon = {
		lat: pin.latitude,
		lng: pin.longitude
	};

	console.log(pin.color);

	var marker = new google.maps.Marker({
				map: resultsMap,
				position: latlon,
				//icon: "http://maps.google.com/mapfiles/ms/icons/red.png",
                icon: {
				    path: google.maps.SymbolPath.CIRCLE,
                    scale: 10,
                    strokeWeight: 2,
                    fillOpacity: 0.6,
                    fillColor: pin.color,
                    strokeColor: pin.color
                },
                id: pin.pinID,

				label: {
                   fontSize: '11px',
                   fontWeight: '900',
                   text: pin.label
                }
			});

	markers.push(marker);

    marker.addListener('click', function() {
        console.log(marker.label);

    })
}

