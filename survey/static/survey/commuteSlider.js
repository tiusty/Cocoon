/**
 * Created by awagu on 12/31/2016.
 */
$( function() {
    $( "#commute" ).slider({
        range: true,
        min: 0,
        max: 180,
        values: [ 10, 60 ],
        slide: function( event, ui ) {
            // If the ui value goes above 61 then start recording in hours
            if (ui.values[ 1 ] >= 61)
            {
                $( "#amountCommute" ).val( ui.values[ 0 ] + " Minutes - " + Math.floor(ui.values[ 1 ]/60) + " Hour " + (ui.values[ 1 ]%60) + " Min");
            }
            else
            {
                $( "#amountCommute" ).val( ui.values[ 0 ] + " Minutes - " + ui.values[ 1 ] + " Minutes");
            }
            $( "#id_minCommute").val(ui.values[0]);
            $( "#id_maxCommute").val(ui.values[1]);
        }
    });
    $( "#amountCommute" ).val( $( "#commute" ).slider( "values", 0 ) +
        " Minutes - " + $( "#commute" ).slider( "values", 1 ) + " Minutes");
    $( "#id_minCommute").val( $("#commute").slider("values", 0));
    $( "#id_maxCommute").val( $("#commute").slider("values", 1));
} );