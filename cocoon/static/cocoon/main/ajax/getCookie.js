/**
 * Created by awagu on 5/15/2017.
 */
/*
    Function: getCookie(name)

    Description:
    This function retrieves the Cookie and the CSRF token for the page.
    This function MUST be included with any page that wants to use an ajax request
    Without this function, any ajax request will be forbidden and therefore not work.

    Note: This function does not need to be called within the page. Just include this file
    and it will take care of the authentication for ajax requests
 */
function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });