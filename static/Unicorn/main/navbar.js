/**
 * Created by srayment on 6/20/17.
 */

$(document).ready(function () {

    if ($(window).scrollTop() < 60) {

        $('.navbar').show();

        $('.navbar').removeClass("navbar-animated");

        $(".navbar-brand").removeClass("nav-brand-animated");
        $(".nav > li > a").removeClass("link-animated");
        $(".nav-logo").removeClass("nav-logo-animated");
        $(".signup-button").removeClass("button-link-animated")
        $(".register-link").removeClass("register-link-animated");
    } else if ($(this).scrollTop() < 100) {
        $('.navbar').hide();


    } else {
        $('.navbar').addClass('navbar-animated');

        $(".navbar-brand").addClass("nav-brand-animated");
        $(".nav > li > a").addClass("link-animated");
        $(".nav-logo").addClass("nav-logo-animated");
        $(".signup-button").addClass("button-link-animated")
        $(".register-link").addClass("register-link-animated");
        $('.navbar').show();
    }

    $(window).scroll(function () {

         $(".sidenav").css("top", $('.navbar').height() - $(this).scrollTop());

        if ($(this).scrollTop() < 60) {

            $('.navbar').show();

            $('.navbar').removeClass("navbar-animated");

            $(".navbar-brand").removeClass("nav-brand-animated");
            $(".nav > li > a").removeClass("link-animated");
            $(".nav-logo").removeClass("nav-logo-animated");
            $(".signup-button").removeClass("button-link-animated")
            $(".register-link").removeClass("register-link-animated");
        } else if ($(this).scrollTop() < 100) {
            $('.navbar').hide();


        } else {
            $('.navbar').show();
            $('.navbar').addClass('navbar-animated');

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