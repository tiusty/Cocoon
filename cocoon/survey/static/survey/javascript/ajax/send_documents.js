/**
 * created by awagu on 5/15/2017.
 */
/*
    function: set_favorite(num, url)

    arguments:
    1. num: this is the id of the home that will be added as a favorite
    2. url: this is the url that the ajax request will be sent to

    description:
    this function creates an ajax request that will toggle a home in the users favorite list.
    if the home is already in the list then it will remove the home from the list,
    if the home is not in the list, then it will add the home to the list

 */
function send_documents(url) {
    console.log("send Documents");
    $.ajax({
        url: url,
        type: "post", //http method

        success: function (json) {
            console.log("success");
            if (json["result"] == 1) {
                console.log("Docs sent");
                $('#refresh_docs').html('Refresh Document Status');
            }
            else if (json["result"] == 2)
            {
                console.log("Docs signed");
                $('#schedule_homes').removeClass('disabled');
                $('#refresh_docs').hide()
            }
            // need to handle error! create a div that is meant for errors
            else {
                console.log(json["message"]);
            }
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responsetext);
        }
    })
}

$('#refresh_docs').click(function(){
    var $this = $(this);
    $this.text('Loading... Please wait');
})

