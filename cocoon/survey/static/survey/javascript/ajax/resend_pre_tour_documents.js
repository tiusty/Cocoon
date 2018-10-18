/*
    function: resend_pre_tour_documents(url)

    arguments:
    1. url: this is the url that the ajax request will be sent to

    description:
        Resends the pretour forms to the user.

 */
function resend_pre_tour_documents(url) {
    $.ajax({
        url: url,
        type: "post", //http method

        success: function (json) {
            console.log("success");
            if (json["result"] == 1) {
                console.log("Resend docs successful");
                $('#resendDocs').text('Resend Documents');
            }
            // need to handle error! create a div that is meant for errors
            else {
                console.log(json["message"]);
                $('#resendDocs').text('Resend Documents');

            }
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responsetext);
        }
    })
}

$('#resendDocs').click(function(){
    var $this = $(this);
    $this.text('Loading... Please wait');
})
