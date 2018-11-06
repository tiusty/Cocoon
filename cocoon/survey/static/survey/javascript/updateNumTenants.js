/**
 * This function makes sure that the correct number of tenant forms are displayed based on what
 *  the user selects
 *
 *  Arguments:
 *      None
 *
 *  Return:
 *      None
 *
 *  Assumptions:
 *      This reads the desired amount of desired forms by reading the value of the id_number_of_tenants element
 *      This assumes that the tabs and the sections have the correct format as shown below
 */
function updateNumTenants() {
    var number_of_tenants = parseInt($('#id_number_of_tenants').val());
    console.log(number_of_tenants);

    //  Makes sure that the form tabs and sections that the user wants to shown
    for(var i=0; i<number_of_tenants; i++){
        var tab = "#form_destination_tabs_" + (i+1);
        var section="#form_destination_section_"+(i+1);

        // If the tab or the section has the hide class then remove it
        if($(tab).hasClass('hide'))
        {
            $(tab).removeClass('hide');
        }
        if($(section).hasClass('hide'))
        {
            $(section).removeClass('hide');
        }

    }

    // Makes sure that all the form tabs and sections that are beyond the number of tenant forms
    //  the user wants are hidden
    for(var i=number_of_tenants; i < 5; i++)
    {
        var tab = "#form_destination_tabs_" + (i+1);
        var section="#form_destination_section_"+(i+1);

        // If the tab or the section does not have the hide class then add it
        if(!$(tab).hasClass('hide'))
        {
            $(tab).addClass('hide');
        }
        if(!$(section).hasClass('hide'))
        {
            $(section).addClass('hide');
        }

    }
}
