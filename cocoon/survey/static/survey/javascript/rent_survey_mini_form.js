/**
 * This javascript files adds the functionality associated with the rent_mini_survey.html file
 *
 * Therefore if the mini survey is wanted, then this javascript file should be included with it
 *
 * Associated Html files:
 *      rent_survey_survey.html
 */

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("sidebarSurvey").style.width = "0";
    document.getElementById("sidebarSurvey").classList.remove("openNav")
}

/* Set the width of the side navigation to 250px */
function openNav() {
    document.getElementById("sidebarSurvey").classList.add("openNav");
    $('.sidenav').css("height", $(document).height() - $('.navbar').height() - $('.footer').height());

    if ($(window).width() < 768) {
        document.getElementById("sidebarSurvey").style.width = "100%";
    } else if ($(window).width() < 900) {
        document.getElementById("sidebarSurvey").style.width = "60%";
    } else {
        document.getElementById("sidebarSurvey").style.width = "40%";
    }
}

// When the nav opens, depending on the screen size, it will open a different amount
$(window).resize(function () {
    if ($(this).width() <= 768) {

        if ($('.openNav').length) {
            document.getElementById("sidebarSurvey").style.width = "100%";

        }


    } else if ($(window).width() < 900) {

        if ($('.openNav').length) {
            document.getElementById("sidebarSurvey").style.width = "60%";

        }

    } else {

        if ($('.openNav').length) {
            document.getElementById("sidebarSurvey").style.width = "40%";

        }

    }
});
