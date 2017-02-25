/**
 * Created by awagu on 2/24/2017.
 */
$( function() {
    $( "#moveInDatePicker" ).datepicker({
        // If the row is not complete, it starts showing days for the next month
        showOtherMonths: true,
        //Lets other months be selected
        selectOtherMonths: true,
        //Shows the today button and the done button
        showButtonPanel: true,
    });
    //Animation for the datepicker
    $( "#anim" ).on( "change", function() {
      $( "#moveInDatePicker" ).datepicker( "option", "showAnim", $( this ).val() );
    });
  } );