/*
    function: send_documents(url)

    arguments:
    1. url: this is the url that the ajax request will be sent to

    description:
    This function either creates the documents if they are not created yet, or will
        query docusign to see if the documents have already been signed

 */
function send_documents(url) {
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

