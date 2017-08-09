/*

 This script is for rendering and unrendering tiles on the frontend before
 a page refresh occurs in order to make the process more seamless.

 If the tile is not in the actual html due to a page refresh, the DOM is
 augmented. Otherwise, it is just redisplayed block.

 Problems: Unfavoriting from expanded tiles is not implemented.

 Visit list tiles unfavorited do not update glyphs on expanding action after page reload

 */

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

        console.log("CLICKED MEEE");

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