/**
 * Created by awagu on 12/22/2016.
 */
/**
 * Created by Alex on 10/30/2016.
 */
function selectAddress(currNum) {
    var currAddress = "address" + currNum;
    var address = document.getElementById(currAddress).innerHTML;
    myDestination = address;
    console.log(address);
    addChosenMarker(address)
}


