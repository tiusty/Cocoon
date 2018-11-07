function add_destination_form(form_add_value, number_of_formsets) {
    /*
    Function controls the amount of forms to display on the survey page.
    The default value is stored in the html value and then is modified by this function from there

    Arguments:
        form_add_value (int): Expects 1 or -1. 1-> Add a form, -1-> delete a form
        number_of_formsets (int): Expects an int which is the max amount of formsets that is supported
            by the html file, this should be filled by a django template tag which passes the amount of
            formsets to create

    Return:
        None:
     */


    var destination_form_number = parseInt($('#id_number_destinations_filled_out').val());

    // Creating variables for form name to prevent spelling errors
    var form_destination_div="form_destination_div";
    var form_destination_tabs="form_destination_tabs_";
    var form_destination_section="form_destination_section_";
    var form_destination_add_span="form_destination_add_span";
    var form_destination_minus_span="form_destination_minus_span";

    // Case if the user wants to add a form
    if(form_add_value === 1) {

        // If there were no active forms and the user adds one, then set the max and min commute to the current
        //  slider values
        if (destination_form_number === 0)
        {
            var max_commute_id = "#id_tenants-0-max_commute";
            var min_commute_id = "#id_tenants-0-min_commute";

            $(min_commute_id).val($("#commute").slider("values", 0));
            $(max_commute_id).val($("#commute").slider("values", 1));
        }
        if (destination_form_number < number_of_formsets)
            destination_form_number += form_add_value;
            $("#" + form_destination_tabs + destination_form_number).removeClass("hide")
    }
    else if (form_add_value === -1) {
        if (destination_form_number > 0) {
            // When a subtraction is necessary, first hide the last form and delete its contents
            $("#" + form_destination_tabs + destination_form_number).addClass("hide");
            $("#" + form_destination_section + destination_form_number).find('input:text').val('');

            destination_form_number += form_add_value;

            // If the last form was active then set the second to last element as active
            //      otherwise keep the current one active
            if ($("#" + form_destination_tabs + (destination_form_number + 1)).hasClass('active')) {
                // Since the last element was active, make sure that the section and the tab is no longer active
                $("#" + form_destination_section + (destination_form_number + 1)).removeClass('active in');
                $("#" + form_destination_tabs + (destination_form_number + 1)).removeClass('active');

                // Now activate the second to last element
                $("#" + form_destination_section + destination_form_number).addClass('active in');
                $("#" + form_destination_tabs + destination_form_number).addClass('active');
            }
        }
    }


    // If all the formsets are deleted, then remove the minus button
    if(destination_form_number === 0) {
        // If all the forms are deleted, make sure to hide the whole form div as well
        $("#" + form_destination_minus_span).addClass('hide');
        $("#" + form_destination_div).addClass('hide');
    }
    else {
        // If there is at least one form, make sure the minus button is present
        //  and the form div is present
        $("#" + form_destination_minus_span).removeClass('hide');
        $("#" + form_destination_div).removeClass('hide');

    }

    // If there is only one form, then it should always be active
    //  This is mostly needed for the case when there are 0 forms and then they add a form
    if(destination_form_number === 1)
    {
        $("#" + form_destination_section + destination_form_number).addClass('active in');
        $("#" + form_destination_tabs + destination_form_number).addClass('active');
    }

    // If all the formsets are populated, then remove the add button
    if(destination_form_number === number_of_formsets) {
        $("#" + form_destination_add_span).addClass('hide');
    }
    else {
        $("#" + form_destination_add_span).removeClass('hide');
    }
    $('#id_number_destinations_filled_out').val(destination_form_number);
}