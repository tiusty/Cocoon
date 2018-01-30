/*

 This script is for rendering and unrendering tiles on the frontend before
 a page refresh occurs in order to make the process more seamless.

 If the tile is not in the actual html due to a page refresh, the DOM is
 augmented. Otherwise, it is just redisplayed block.

 */

/*

Note: This code is currently not used in production because it could result in
the loss of a home if a user unintentionally clicks unfavorite.

$(document).ready(function () {

    $(".heartGlyph").on('click', function () {

        if ($(this).hasClass('glyphicon-heart')) {
            console.log("favorited!");
            $('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').addClass('toRemove').fadeOut();
        } else {
            console.log("not favorited");

            if ($('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').length) {
                $('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').removeClass('toRemove').fadeIn();
            } else {
                console.log("ADDING HTML AGAIN");
                $('.favoriteTiles').append($(this).parents('.tile').clone(true, true));
            }
        }
    });

    $(".expanded-glyph").click(function () {

        if ($(this).hasClass('glyphicon-heart')) {
            console.log("favorited!");
            $('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').addClass('toRemove').fadeOut();
        } else {
            console.log("not favorited");

            if ($('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').length) {
                $('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').removeClass('toRemove').fadeIn();
            } else {
                console.log("ADDING HTML AGAIN");
                $('.favoriteTiles').append($(this).parents('.tile').clone(true, true));
            }

        }

    });

})

*/