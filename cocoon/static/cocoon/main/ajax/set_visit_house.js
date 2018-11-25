/**
 * Created by awagu on 5/14/2017.
 */

/*
 Function: set_visit_house(num, url)

 Arguments:
 1. num: This is the id of the home that will be operated on
 2. url: This is the url for the ajax request

 Description:
 This function adds the home to the users visit list
 */
function set_visit_house(num, survey, url) {
    $.ajax({
        url: url,
        type: "POST", //http method
        data: {
            "visit_id": num, "survey": survey,
        },

        success: function (json) {
            console.log("success");
            if (json["result"] == 0) {
                console.log("removed");
            }
            else if (json["result"] == 1) {
                console.log("Added!");
                //generic success function that calls a function on the templates page script tags
                set_visit_house_success(json["homeId"]);
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
/*
    Function: set_visit_house_success(visit_id):

    Arguments:
        visit_id: The id of the house that has been added

    Description:
        This function is called after a successfully addition a home to the visit list, aka
            in set_visit_house(num, url). The function assumes that the div that contains
            the button/information for the visit list in the homeModal is called visitHomeSet.
            Everything in the div will be replaced and this will take the spot
 */
function set_visit_house_success(visit_id) {
    $("div#visitHomeSet" + visit_id).html('<p><b>Visit List:</b> Added!</p>');
}
