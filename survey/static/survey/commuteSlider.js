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
            $( "#id_min_commute").val(ui.values[0]);
            $( "#id_max_commute").val(ui.values[1]);
        }
    });
    // If the ui value goes above 61 then start recording in hours
    if ($( "#commute" ).slider( "values", 1 ) >= 61)
    {
        if ($( "#commute" ).slider( "values", 0 ) >= 61)
        {
            $( "#amountCommute" ).val( Math.floor($( "#commute" ).slider( "values", 0 )/60) + " Hh " + ($( "#commute" ).slider( "values", 0 )%60) + " Min - "
                + Math.floor($( "#commute" ).slider( "values", 1 )/60) +  " Hh " + ($( "#commute" ).slider( "values", 1 )%60) + " Min");
        }
        else
        {
            $( "#amountCommute" ).val( $( "#commute" ).slider( "values", 0 ) +
        " Minutes - " + Math.floor($( "#commute" ).slider( "values", 1 )/60) +  " Hh " + ($( "#commute" ).slider( "values", 1 )%60) + " Min");
        }
    }
    else
    {
        $( "#amountCommute" ).val( $( "#commute" ).slider( "values", 0 ) +
        " Min - " + $( "#commute" ).slider( "values", 1 ) + " Min");
    }

    $( "#id_minCommute").val( $("#commute").slider("values", 0));
    $( "#id_maxCommute").val( $("#commute").slider("values", 1));
} );