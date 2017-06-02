/**
 * Created by awagu on 5/15/2017.
 */
/**
 * Created by awagu on 5/14/2017.
 */

/*
    Function: set_visit_house(num, url)

    Arguments:
    1. num: This is the id of the home that will be operated on
    2. url: This is the url for the ajax request
    3. return_url: This is the url that the page should refresh to once the house is deleted

    Description:
    This function deletes the home from the users visit list
 */
function delete_visit_house(num, url, return_url) {
            $.ajax({
                url: url,
                type: "POST", //http method
                data: {
                    "visit_id": num,
                },

                success: function (json) {
                    console.log("success");
                    if (json["result"] == 0) {
                        console.log("removed");
                        window.location = return_url;
                    }
                    else if (json["result"] == 1) {
                        console.log("Added!");
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