
function add_destination_form(form_add_value, number_of_formsets) {
    console.log(form_add_value);
    console.log(destination_form_number);
    // Creating variables for form name to prevent spelling errors
    var form_destination_div="form_destination_div";
    var form_destination_tabs="form_destination_tabs_";
    var form_destination_section="form_destination_section_";
    var form_destination_add_span="form_destination_add_span";
    var form_destination_minus_span="form_destination_minus_span";
    // Case if the user wants to add a form
    if(form_add_value === 1) {
        if (destination_form_number < number_of_formsets)
            destination_form_number += form_add_value;
            console.log(form_destination_tabs);
            $("#" + form_destination_tabs + destination_form_number).removeClass("hide")
    }
    else if (form_add_value === -1) {
        if (destination_form_number > 0) {
            $("#" + form_destination_tabs + destination_form_number).addClass("hide");
            $("#" + form_destination_section + destination_form_number).find('input:text').val('');
            $("#" + form_destination_section + destination_form_number).removeClass('active in');
            $("#" + form_destination_tabs + destination_form_number).removeClass('active');
            destination_form_number += form_add_value;

            // Active the new last form
            $("#" + form_destination_section + destination_form_number).addClass('active in');
            $("#" + form_destination_tabs + destination_form_number).addClass('active');
        }
    }

    if(destination_form_number === 3) {
        $("#" + form_destination_add_span).addClass('hide');
    }
    else {
        $("#" + form_destination_add_span).removeClass('hide');
    }

    if(destination_form_number === 0) {
        $("#" + form_destination_minus_span).addClass('hide');
        $("#" + form_destination_div).addClass('hide');
    }
    else {
        if(destination_form_number === 1)
        {
            $("#" + form_destination_section + destination_form_number).addClass('active in');
            $("#" + form_destination_tabs + destination_form_number).addClass('active');
        }
        $("#" + form_destination_minus_span).removeClass('hide');
        $("#" + form_destination_div).removeClass('hide');

    }
}