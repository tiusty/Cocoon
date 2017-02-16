/**
 * Created by awagu on 12/31/2016.
 */
$( function() {
    $( "#cost" ).slider({
        range: true,
        min: 0,
        max: 5000,
        values: [ costSliderMin, costSliderMax ],
        slide: function( event, ui ) {
            $( "#amountCost" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
            $( "#id_minPrice").val(ui.values[0]);
            $( "#id_maxPrice").val(ui.values[1]);
        }
    });
    $( "#amountCost" ).val( "$" + $( "#cost" ).slider( "values", 0 ) +
        " - $" + $( "#cost" ).slider( "values", 1 ) );
    $( "#id_minPrice").val( $("#cost").slider("values", 0));
    $( "#id_maxPrice").val( $("#cost").slider("values", 1));
} );