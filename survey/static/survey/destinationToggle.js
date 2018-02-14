
function add_destination_form(form_add_value, number_of_formsets) {
    console.log(form_add_value)
    console.log(destination_form_number)
    if(form_add_value === 1) {
        if (destination_form_number < number_of_formsets)
            destination_form_number += form_add_value;
            $("#form_destination_" + destination_form_number).removeClass("hide")
    }
    else if (form_add_value === -1) {
        if (destination_form_number > 0) {
            $("#form_destination_" + destination_form_number).addClass("hide")
            destination_form_number += form_add_value;
        }
    }

    if(destination_form_number === 3) {
        $("#form_destination_add_span").addClass('hide')
    }
    else {
        $("#form_destination_add_span").removeClass('hide')
    }

    if(destination_form_number === 0) {
        $("#form_destination_minus_span").addClass('hide')
    }
    else {
        $("#form_destination_minus_span").removeClass('hide')
    }
}