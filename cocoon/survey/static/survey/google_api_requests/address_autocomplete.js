/*
    Brief: Enables autocomplete for the address

    Description: Enables the address completion in the destination form. This way the address can be located correctly.
        The actual address does not need to exist because google autocomplete will determine where the address should
        be if the address were to exist. Therefore, it is up to the user to make sure they are putting in the correct
        location
 */

// Stores the autocomplete result
var autocomplete;

// The different componenents of the autocomplete and the type desired for each field
var componentForm = {
                street_number: 'short_name',
                route: 'long_name',
                locality: 'long_name',
                administrative_area_level_1: 'short_name',
                country: 'long_name',
                postal_code: 'short_name'
                };

function initAutocomplete() {
    /**
     * This function is the initialization function for the autocomplete. In the script tag with the google
     *  api key, this function is used as the callback method.
     */
    // Create the autocomplete object
    autocomplete = new google.maps.places.Autocomplete(
    /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
        {types: ['geocode']});

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
    /**
     * This function fills in the destination form with the values provided form the google
     *  address autocomplete. The autocomplete is parsed and the values are added to the correct
     *  input forms so that the form will validate correctly.
     */
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    // Retrieves the number of forms that are active (i.e The number of commuters the user
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

            // Once we find the active tab then quit because there should only be one
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

        if (place.address_components[i].types[0] === "postal_code")
        {
            var val = place.address_components[i][componentForm["postal_code"]];
            document.getElementById('id_rentingdestinationsmodel_set-' + active_form_num + '-zip_code').value = val;
        }

        if (place.address_components[i].types[0] === "administrative_area_level_1")
        {
            var val = place.address_components[i][componentForm["administrative_area_level_1"]];
            document.getElementById('id_rentingdestinationsmodel_set-' + active_form_num + '-state').value = val;
        }

        if (place.address_components[i].types[0] === "locality")
        {
            var val = place.address_components[i][componentForm["locality"]];
            document.getElementById('id_rentingdestinationsmodel_set-' + active_form_num + '-city').value = val;
        }

    }

    var full_street_address = street_num + " " + street_address;

    // Sometimes if the address is a subpremise or something, the autocomplete will show up
    //  and let the user select the address but then it will not return the street address or street num.
    //  Therefore, if the street_num and street_address were not populated, then auto-populate
    //  with the user populated address.
    // Remember that population of the form fields only occurs when the user selected on the address from
    //  the google drop down list, so the address being added is still a valid address
    if ( !street_num || !street_address ) {
        var full_autocomplete = $('#autocomplete').val();
        full_street_address = full_autocomplete.split(',')[0];
    }

    // Now concatenate the street_num and street address to store the full address
    document.getElementById('id_rentingdestinationsmodel_set-' + active_form_num + '-street_address').value = full_street_address;

  }

function clean_autocomplete() {
    /**
    * This function cleans the autocomplete input box so the user can easily
    *    enter in a new address
    */
    document.getElementById('autocomplete').value = "";
}
