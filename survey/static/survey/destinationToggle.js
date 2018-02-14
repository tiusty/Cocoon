
function add_destination_form(form_add_value) {
    destination_form_number += form_add_value;
    console.log(form_add_value)
    console.log(destination_form_number)
     $( "#form_destination_" + destination_form_number ).removeClass("hide")
}