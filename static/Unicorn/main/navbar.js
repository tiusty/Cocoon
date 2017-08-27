/**
 * Created by srayment on 6/20/17.
 */

$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() < 35 ) {

            $(".sidenav").removeClass("sidenav-down");
            $(".navbar-brand").removeClass("nav-brand-animated");
            $(".nav > li > a").removeClass("link-animated");
            $(".nav-logo").removeClass("nav-logo-animated");
            $(".signup-button").removeClass("button-link-animated")
            $(".register-link").removeClass("register-link-animated");
        } else {

            $(".sidenav").addClass("sidenav-down");
            $(".navbar-brand").addClass("nav-brand-animated");
            $(".nav > li > a").addClass("link-animated");
            $(".nav-logo").addClass("nav-logo-animated");
            $(".signup-button").addClass("button-link-animated")
            $(".register-link").addClass("register-link-animated");
        }
    });

    $(window).resize(function () {
        if ($(this).width() <= 768) {

            // Also moves the sidenav down
            $(".sidenav").removeClass("sidenav-down");

            $(".navbar-brand").removeClass("nav-brand-animated");
            $(".nav > li > a").removeClass("link-animated");
            $(".nav-logo").removeClass("nav-logo-animated");
            $(".signup-button").removeClass("button-link-animated")
            $(".register-link").removeClass("register-link-animated");
        }
    })
})