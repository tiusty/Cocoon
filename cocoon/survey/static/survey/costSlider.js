/**
 * Created by awagu on 12/31/2016.
 */
$( function() {
    $( "#cost" ).slider({
        range: true,
        min: 0,
        max: 5000,
        step: 50,
        values: [ costSliderMinInit, costSliderMaxInit ],
        slide: function( event, ui ) {
            $( "#amountCost" ).val( "Want To Pay: $" + ui.values[ 0 ].toLocaleString() + " - Max: $" + ui.values[ 1 ].toLocaleString() );
            $( "#id_desired_price").val(ui.values[0]);
            $( "#id_max_price").val(ui.values[1]);
        }
    });
    $( "#amountCost" ).val( "Want To Pay: $" + $( "#cost" ).slider( "values", 0 ).toLocaleString() +
        " - Max: $" + $( "#cost" ).slider( "values", 1 ).toLocaleString() );
    $( "#id_desired_price").val( $("#cost").slider("values", 0));
    $( "#id_max_price").val( $("#cost").slider("values", 1));
} );