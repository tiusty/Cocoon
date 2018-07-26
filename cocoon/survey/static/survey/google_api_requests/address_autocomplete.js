/*
    Brief: Enables autocomplete for the address

    Description: Enables the address completion in the destination form. This way the address can be located correctly.
        The actual address does not need to exist because google autocomplete will determine where the address should
        be if the address were to exist. Therefore, it is up to the user to make sure they are putting in the correct
        location
 */

var placeSearch, autocomplete;
var componentForm = {
                street_number: 'short_name',
                route: 'long_name',
                locality: 'long_name',
                administrative_area_level_1: 'short_name',
                country: 'long_name',
                postal_code: 'short_name'
                };

function initAutocomplete() {
    // Create the autocomplete object
    autocomplete = new google.maps.places.Autocomplete(
    /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
        {types: ['geocode']});

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    // Retrives the number of forms that are active (i.e The number of commuters the user
    //  has selected)
    var destination_form_number = parseInt($('#id_number_destinations_filled_out').val());

    // If there is no active tab then set to -1
    var active_form_num = -1;

    // This determines which commuter is the actively selected commuter
    for (var j = 1; j <= destination_form_number; j++)
    {
        if ($('#form_destination_section_' + j).hasClass('active'))
        {
            // Since the tabs are base 1 and the input fields are base 0. Need to subtract 1
            //  so that the number is converted to the right base for the input fields
            active_form_num = j-1;
            break;
        }

    }


    // Since the street num and the street address are two different component fields in google
    //  Store the variables so that they can be concatenated together at the end
    var street_num = "";
    var street_address = "";

    // Loop through and select the required components to autofill the required fields
    for (var i = 0; i < place.address_components.length; i++) {
        if (place.address_components[i].types[0] === "street_number")
        {
            street_num = place.address_components[i][componentForm["street_number"]];
        }

        if (place.address_components[i].types[0] === "route")
        {
            street_address = place.address_components[i][componentForm["route"]]
        }

    }

    // Now concatenate the street_num and street address to store the full address
    var full_street_address = street_num + " " + street_address;
    document.getElementById('id_rentingdestinationsmodel_set-' + active_form_num + '-street_address_destination').value = full_street_address;


    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    // for (var i = 0; i < place.address_components.length; i++) {
    //   var addressType = place.address_components[i].types[0];
    //   if (componentForm[addressType]) {
    //     var val = place.address_components[i][componentForm[addressType]];
        // console.log(val);
        //   console.log(place.address_components);
        // $('#id_rentingdestinationsmodel_set-0-street_address_destination').value = val;
        // document.getElementById(addressType).value = val;
      // }
    // }
  }




// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initAutocomplete"
//     async defer></script>
