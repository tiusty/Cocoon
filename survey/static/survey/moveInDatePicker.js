/**
 * Created by awagu on 2/24/2017.
 */
$( function() {
    $( "#moveInDatePicker" ).datepicker();
    $( "#anim" ).on( "change", function() {
      $( "#moveInDatePicker" ).datepicker( "option", "showAnim", $( this ).val() );
    });
  } );