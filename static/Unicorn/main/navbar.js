/**
 * Created by srayment on 6/20/17.
 */

$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() <= 0 ) {
            console.log("scrolled to the top");
            $(".navbar-brand").addClass("nav-brand-animated")
        } else {
            console.log("scrolled regular")
        }
    })
})