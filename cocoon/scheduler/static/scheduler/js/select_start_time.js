/**
 * Populates the start time for a given itinerary - completing the scheduling
 *
 * @param id - id of time slot of interest
 * @param url - url handled by the correct view function
 */
function selectStartTime(timeId, itineraryId, url) {
    $('#select-' + timeId).text("Loading...");

    $.ajax({
        url: url,
        type: "post", //http method
        data: {"time_id": timeId,
                "itinerary_id": itineraryId},

        success: function (json) {
            if (json["result"] == 0) {
                $('#select-' + timeId).removeClass().addClass('btn btn-disabled');
                $('#select-' + timeId).text("Selected");
                $('#select-' + timeId).attr("onclick", "");
            } else if (json["result"] == 1) {
                $('#select-' + timeId).removeClass().addClass('btn btn-disabled');
                $('#select-' + timeId).text("Unavailable");
                $('#select-' + timeId).attr("onclick", "");
            } else {
                $('#select-' + timeId).text("Claim");
            }
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText)
        }
    });
}