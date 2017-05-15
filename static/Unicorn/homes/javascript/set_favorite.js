/**
 * Created by awagu on 5/15/2017.
 */
function set_favorite(num, url) {
            $.ajax({
                url: url,
                type: "POST", //http method
                data: {"fav": num},

                success: function (json) {
                    console.log("success");
                    if (json["result"] == 0) {
                        console.log("removed");
                        $('span#glyph' + num).removeClass("glyphicon-heart").addClass("glyphicon-heart-empty");
                    }
                    else if (json["result"] == 1) {
                        console.log("Added!");
                        $('span#glyph' + num).removeClass("glyphicon-heart-empty").addClass("glyphicon-heart");
                    }
                    // Need to handle error! Create a div that is meant for errors
                    else {
                        console.log(json["result"]);
                    }
                },

                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            })
        }