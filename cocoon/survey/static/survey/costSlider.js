/**
 * Created by awagu on 12/31/2016.
 */
$( function() {
    $( "#cost" ).slider({
        range: true,
        min: 0,
        max: 5000,
        step: 50,
        values: [ costSliderMin, costSliderMax ],
        slide: function( event, ui ) {
            $( "#amountCost" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
            $( "#id_min_price_survey").val(ui.values[0]);
            $( "#id_max_price_survey").val(ui.values[1]);
        }
    });
    $( "#amountCost" ).val( "$" + $( "#cost" ).slider( "values", 0 ) +
        " - $" + $( "#cost" ).slider( "values", 1 ) );
    $( "#id_min_price_survey").val( $("#cost").slider("values", 0));
    $( "#id_max_price_survey").val( $("#cost").slider("values", 1));
} );