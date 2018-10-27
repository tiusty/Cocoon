/**
 * Created by awagu on 12/31/2016.
 */
$( function() {
    $( "#commute" ).slider({
        range: true,
        min: 0,
        max: 180,
        values: [ commuteSliderMinInit, commuteSliderMaxInit ],
        slide: function( event, ui ) {

            // Retrieve the current active commuter number
            var active_form_num = retrieve_active_commuter();

            // Set the max and min input values which will be changed with the slider
            var max_commute_id = "#id_tenants-" + active_form_num + "-max_commute";
            var min_commute_id = "#id_tenants-" + active_form_num + "-min_commute";

            // Set the display of the slider to visually show the values
            set_slider_display(ui.values[0], ui.values[1]);

            // Actually set the form fields values. These are set from the variables
            //  from the script tag on the main html page
            $(min_commute_id).val(ui.values[0]);
            $(max_commute_id).val(ui.values[1]);
        }
    });

    // Retrieve the current active commuter number
    var active_form_num = retrieve_active_commuter();

    // Set the max and min input values which will be changed with the slider
    var max_commute_id = "#id_tenants-" + active_form_num + "-max_commute";
    var min_commute_id = "#id_tenants-" + active_form_num + "-min_commute";

    // Set the display of the slider to visually show the values.
    // The values are pulled from the current values of the max and min fields of the current commuter
    set_slider_display($("#commute").slider("values", 0), $("#commute").slider("values", 1));

    // Set the new min and max values to the current slider values
    $(min_commute_id).val( $("#commute").slider("values", 0));
    $(max_commute_id).val( $("#commute").slider("values", 1));
} );

function retrieve_active_commuter() {
    /**
     * This function retrieves which commuter is the current active number. This is done by
     *  Determining how many forms have been filled out, then looping through all the form sections
     *  of the active commuters. The active commuter is determined by the section that is being displayed
     *  because it contains the 'active' class.
     *
     *  Return:
     *      active_form_number (int) -> The current commuter that is being selected. This number is
     *          based zero, so the first commuter returns 0, etc. -1 is returned if it
     *          can't find the active commuter
     */
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

    // Displays error if the active commuter cannot be found
    if (active_form_num === -1)
    {
        console.log("Error in retrieve_active_commuter, active_form_num: " + active_form_num)
    }

    return active_form_num;

}

function set_slider_display(min_value, max_value) {
    /**
     * This function sets the slider display value above the slider. This will display minutes when
     *  the value is 60 and under. The display will switch to hours and minutes when above 60 minutes
     *
     *  Arguments:
     *      min_value (int) -> This is the value of the minimum slider value
     *      max_value (int) -> This is the value of the maximum slider value
     *
     *  Return:
     *      None:
     */
    // If the ui value goes above 61 then start recording in hours
    if ( max_value >= 61)
    {
        if ( min_value >= 61)
        {
            $( "#amountCommute" ).val( Math.floor(min_value/60) + " Hh " + (min_value%60) + " Min - "
                + Math.floor(max_value/60) +  " Hh " + (max_value%60) + " Min");
        }
        else
        {
            $( "#amountCommute" ).val( min_value +
                " Minutes - " + Math.floor(max_value/60) +  " Hh " + (max_value%60) + " Min");
        }
    }
    else
    {
        $( "#amountCommute" ).val( min_value +
            " Min - " + max_value + " Min");
    }
}

function set_slider_values(thisVal) {
    /**
     * This function is called when the tab is clicked to change commuters. This function
     *  makes sure that the when the tab changes to a new commuter, the slider values are correctly
     *  switched to the new commuter
     *
     *  Arguments:
     *      thisVal (this) -> The tab this value is displayed to get the information regarding
     *        the tab. This way the section # can be extracted so that the tab being clicked on
     *        can be determined. The problem with relying on onclick(), is that the current active
     *        tab when the onclick is called is still the old tab. Therefore, with the 'this' being
     *        passed in, it passes the tab being clicked on.
     */
    // Retrieves the number of forms that are active (i.e The number of commuters the user
    //  has selected)
    // If there is no active tab then set to -1
    var active_form_num = -1;

    // This determines which tab is being used and then gets the number
    var tab_name = thisVal.href.substring(thisVal.href.lastIndexOf('/')+1);
    active_form_num = tab_name.match(/\d+/)[0];

    // Subtract one since the tabs are base 1, and the input fields are base 0. This
    //  will make sure the right commuter is selected
    active_form_num = active_form_num -1;

    // Displays error if the active commuter cannot be found
    if (active_form_num === -1)
    {
        console.log("Error in set_slider_values, active_form_num: " + active_form_num)
    }

    // Set the max and min input values which will be changed with the slider
    var max_commute_id = "#id_tenants-" + active_form_num + "-max_commute";
    var min_commute_id = "#id_tenants-" + active_form_num + "-min_commute";

    // Sets initial values to the fields if they are currently blank. Since when a form is
    //  deleted it clears out the fields, when a new one is selected it, needs to populate
    //   the existing fields with a default
    if (!$(min_commute_id).val())
    {
        // Sets default min value to 0
        $(min_commute_id).val(0);
    }
    if (!$(max_commute_id).val())
    {
        // Sets the default max value to 60
        $(max_commute_id).val(60);
    }

    // Set the display of the slider to visually show the values.
    // The values are pulled from the current values of the max and min fields of the selected commuter
    set_slider_display($(min_commute_id).val(), $(max_commute_id).val());

    // Sets the slider to the values from the selected commuters max and min
    $("#commute").slider("option", "values", [$(min_commute_id).val(), $(max_commute_id).val()])

}

