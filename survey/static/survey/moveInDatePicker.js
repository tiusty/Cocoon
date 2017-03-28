/**
 * Created by awagu on 2/24/2017.
 */
$( function() {
    var dateFormat = "mm/dd/yy",
      from = $( "#moveInDatePickerStart" )
        .datepicker({
          defaultDate: "+1w",
          changeMonth: true,
          numberOfMonths: 2,
          minDate: 0,
        })
        .on( "change", function() {
          to.datepicker( "option", "minDate", getDate( this ) );
        });;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
      to = $( "#moveInDatePickerEnd" )
          .datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 2,
      });

    // If the Start datepicker has a value then set the end date with that date as the default
    // minDate. If the date gets changed from there then it will follow the old method.
    var attr =  $( "#moveInDatePickerStart" ).attr('value');
    if (typeof attr !== typeof undefined && attr !== false) {
        $( "#moveInDatePickerEnd" ).datepicker( "option", "minDate", attr );
    }

    function getDate( element ) {
      var date;
      try {
        date = $.datepicker.parseDate( dateFormat, element.value );
      } catch( error ) {
        date = null;
      }

      return date;
    }
  } );