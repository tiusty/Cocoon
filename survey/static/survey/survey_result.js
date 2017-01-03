/**
 * Created by awagu on 12/22/2016.
 */
/**
 * Created by Alex on 10/30/2016.
 */
$(document).ready(function () {
    $(".toggle-sidebar").click(function () {
        $("#sidebarSurvey").toggleClass("collapsedSide");
        $("#contentSurvey").toggleClass("col-sm-12 col-sm-9 col-sm-offset-3");

        return false;
    });
});