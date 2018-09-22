/**
 * Created by awagu on 5/15/2017.
 */
/*
    Function: set_favorite(num, url)

    Arguments:
    1. num: This is the id of the home that will be added as a favorite
    2. url: This is the url that the ajax request will be sent to

    Description:
    This function creates an ajax request that will toggle a home in the users favorite list.
    If the home is already in the list then it will remove the home from the list,
    If the home is not in the list, then it will add the home to the list

 */
function set_favorite(num, url) {
    console.log("favorited");
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