/**
 * Associates the logged in agent account with the itinerary
 *
 * @param id - id of the itinerary being claimed
 * @param url - url handled by the correct view function
 */
function claimItinerary(id, url) {
    $('#claim-' + id).text("Loading...");

    $.ajax({
        url: url,
        type: "post", //http method
        data: {"itinerary_id": id},

        success: function (json) {
            if (json["result"] == 0) {
                $('#claim-' + id).removeClass().addClass('btn btn-disabled');
                $('#claim-' + id).text("Claimed");
                $('#claim-' + id).attr("onclick", "");
            } else if (json["result"] == 1) {
                $('#claim-' + id).removeClass().addClass('btn btn-disabled');
                $('#claim-' + id).text("Unavailable");
                $('#claim-' + id).attr("onclick", "");
            } else {
                $('#claim-' + id).text("Claim");
            }
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText)
        }
    });
}