/**
 * Created by srayment on 8/27/17.
 */

clickBind = $('.tile').on('click', function () {
    expand($(this));
});

/**
 * Function that converts a tile into an expanded tile
 * with the necessary animations.
 *
 * @param aTile - the tile to be expanded
 */
function expand(aTile) {

    if ($(aTile).hasClass('bound')) {
        var isFavorite = $(aTile).find('.heartGlyph').hasClass("glyphicon-heart");
        console.log(isFavorite);
        $(aTile).removeClass('tile');
        $(aTile).addClass('tile-expanded');
        $(aTile).children().hide();
        $(aTile).animate({"height": "65vh"}, 200, function () {
            $(aTile).siblings('.tile').slideUp(150);
        });

        // Adds the templated HTML to the page
        $(aTile).append($(aTile).children('#expanded-tile-contents').html());

        // Updated the heart glyph on expansion
        if (isFavorite) {
            $(".expanded-tile-container").find(".expanded-glyph").removeClass("glyphicon-heart-empty").addClass('glyphicon-heart');
        } else {
            console.log("not here");
            $(".expanded-tile-container").find(".expanded-glyph").removeClass("glyphicon-heart").addClass('glyphicon-heart-empty');
        }

        $(aTile).removeClass('bound');
    }
}

/**
 * Function that converts an expanded tile to a regular tile
 * and adds back removed tiles, with animations.
 *
 * @param clickedElement - the clicked minimize button
 */
function minimize(clickedElement) {

    $(clickedElement).closest('.expanded-tile-container').hide();

    $(clickedElement).parents('.tile-expanded').animate({"height": "115px"}, 200, function () {

        $(clickedElement).parents('.tile-expanded').addClass('tile');
        $(clickedElement).parents('.tile').siblings('.tile').not('.toRemove').slideDown(150);
        $(clickedElement).parents('.tile').children().show();
        $(clickedElement).parents('.tile').removeClass('tile-expanded');
        $(clickedElement).parents('.tile').addClass('bound');
        $(clickedElement).closest('.expanded-tile-container').remove();

        $('.toRemove').fadeOut();

    })
}

// Prevents container element from triggering click event
$('.glyphicon-heart, .glyphicon-heart-empty, .expanded-close').click(function (e) {
    e.stopPropagation();
});