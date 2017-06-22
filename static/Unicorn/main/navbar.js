/**
 * Created by srayment on 6/20/17.
 */

$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() == 0 ) {
            console.log("scrolled to the top");
            $(".navbar-brand").removeClass("nav-brand-animated");
            $(".nav > li > a").removeClass("link-animated");
        } else {
            console.log("scrolled regular");
            $(".navbar-brand").addClass("nav-brand-animated");
            $(".nav > li > a").addClass("link-animated");
        }
    });

    $(window).resize(function () {
        if ($(this).width() <= 768) {
            $(".navbar-brand").removeClass("nav-brand-animated");
            $(".nav > li > a").removeClass("link-animated");
        }
    })
})