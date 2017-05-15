/**
 * Created by awagu on 5/14/2017.
 */
function set_visit_house(num, url) {
            $.ajax({
                url: url,
                type: "POST", //http method
                data: {"visit_id": num},

                success: function (json) {
                    console.log("success");
                    if (json["result"] == 0) {
                        console.log("removed");
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