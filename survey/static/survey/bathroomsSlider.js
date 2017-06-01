/**
 * Created by awagu on 3/14/2017.
 */
/**
 * Created by awagu on 12/31/2016.
 */
$( function() {
    $( "#bathrooms" ).slider({
        range: true,
        min: 0,
        max: 6,
        //step: .5,
        values: [ bathroomsMin , bathroomsMax ],
        slide: function( event, ui ) {
            $( "#amountBathrooms" ).val(ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            $( "#id_min_bathrooms").val(ui.values[0]);
            $( "#id_max_bathrooms").val(ui.values[1]);
        }
    });
    $( "#amountBathrooms" ).val($( "#bathrooms" ).slider( "values", 0 ) +
        " - " + $( "#bathrooms" ).slider( "values", 1 ) );
    $( "#id_min_bathrooms").val( $("#bathrooms").slider("values", 0));
    $( "#id_max_bathrooms").val( $("#bathrooms").slider("values", 1));
} );