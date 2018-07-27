/**
 * Created by awagu on 12/31/2016.
 */
$( function() {
    $( "#commute" ).slider({
        range: true,
        min: 0,
        max: 180,
        values: [ commuteSliderMin, commuteSliderMax ],
        slide: function( event, ui ) {
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

            var max_commute_id = "#id_rentingdestinationsmodel_set-" + active_form_num + "-max_commute";
            var min_commute_id = "#id_rentingdestinationsmodel_set-" + active_form_num + "-min_commute";

            console.log("iterate");
            // If the ui value goes above 61 then start recording in hours
            if (ui.values[1] >= 61) {
                if (ui.values[0] >= 61) {
                    $( "#amountCommute" ).val( Math.floor(ui.values[ 0 ]/60) + " Hh " + (ui.values[0]%60) + " Min " +
                        " - " + Math.floor(ui.values[ 1 ]/60) + " Hh " + (ui.values[ 1 ]%60) + " Min");
                }
                else {
                    $( "#amountCommute" ).val( ui.values[ 0 ] + " Min - " + Math.floor(ui.values[ 1 ]/60) + " Hh " + (ui.values[ 1 ]%60) + " Min");
                }

            }
            else
            {
                $( "#amountCommute" ).val( ui.values[ 0 ] + " Min - " + ui.values[ 1 ] + " Min");
            }
            console.log(min_commute_id);
            console.log(max_commute_id);
            console.log(ui.values[0]);
            $(min_commute_id).val(ui.values[0]);
            $(max_commute_id).val(ui.values[1]);
        }
    });
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

    var max_commute_id = "#id_rentingdestinationsmodel_set-" + active_form_num + "-max_commute";
    var min_commute_id = "#id_rentingdestinationsmodel_set-" + active_form_num + "-min_commute";

    set_slider_display($("#commute").slider("values", 0), $("#commute").slider("values", 1));


    $(min_commute_id).val( $("#commute").slider("values", 0));
    $(max_commute_id).val( $("#commute").slider("values", 1));
} );

function set_slider_values(thisVal) {
    // Retrieves the number of forms that are active (i.e The number of commuters the user
    //  has selected)
    // If there is no active tab then set to -1
    var active_form_num = -1;

    // This determines which tab is being used and then gets the number
    var filename = thisVal.href.substring(thisVal.href.lastIndexOf('/')+1);
    active_form_num = filename.match(/\d+/)[0];
    active_form_num = active_form_num -1;

    var max_commute_id = "#id_rentingdestinationsmodel_set-" + active_form_num + "-max_commute";
    var min_commute_id = "#id_rentingdestinationsmodel_set-" + active_form_num + "-min_commute";

    console.log(min_commute_id);
    console.log($(min_commute_id).val());
    console.log(max_commute_id);
    console.log($(max_commute_id).val());

    if (!$(min_commute_id).val())
    {
        $(min_commute_id).val(0);
    }
    if (!$(max_commute_id).val())
    {
        $(max_commute_id).val(60);
    }
    set_slider_display($(min_commute_id).val(), $(max_commute_id).val());


    $("#commute").slider("option", "values", [$(min_commute_id).val(), $(max_commute_id).val()])

}

function set_slider_display(value_1, value_2) {
    // If the ui value goes above 61 then start recording in hours
    if ( value_2 >= 61)
    {
        if ( value_1 >= 61)
        {
            $( "#amountCommute" ).val( Math.floor(value_1/60) + " Hh " + (value_1%60) + " Min - "
                + Math.floor(value_2/60) +  " Hh " + (value_2%60) + " Min");
        }
        else
        {
            $( "#amountCommute" ).val( value_1 +
                " Minutes - " + Math.floor(value_2/60) +  " Hh " + (value_2%60) + " Min");
        }
    }
    else
    {
        $( "#amountCommute" ).val( value_1 +
            " Min - " + value_2 + " Min");
    }
}
