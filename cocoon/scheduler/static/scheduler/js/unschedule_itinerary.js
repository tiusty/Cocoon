/**
 * Dissociates the start time from an itinerary
 *
 * @param id - id of the itinerary being unscheduled
 * @param url - url handled by the correct view function
 */
function unscheduleItinerary(id, url) {
    $.ajax({
        url: url,
        type: "post", //http method
        data: {"itinerary_id": id},

        success: function (json) {
            if (json["result"] == 0) {
                console.log("Succesfuly unscheduled")
            } else if (json["result"] == 1) {
                console.log("Error unschedling")
            }
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText)
        }
    });
}