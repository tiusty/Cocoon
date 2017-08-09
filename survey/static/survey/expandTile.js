clickBind = $('.tile').on('click', function () {

    if ($(this).hasClass('bound')) {
        var isFavorite = $(this).find('.heartGlyph').hasClass("glyphicon-heart");
        console.log(isFavorite);
        $(this).removeClass('tile');
        $(this).addClass('tile-expanded');
        $(this).children().hide();
        $(this).animate({"height": "65vh"}, 200, function () {
            $(this).siblings('.tile').slideUp(200);
        });
        /*
         * Adds the unloaded templated html to the page
         */
        $(this).append($(this).children('#expanded-tile-contents').html());

        /*
         *  Adds the event listener for removing tile if unfavorited within the expanded tile
         *
         */

        $(".expanded-glyph").click(function () {

        if ($(this).hasClass('glyphicon-heart')) {
            console.log("favorited!");

            if ($('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').length) {
                 $('.favoriteTiles > .tile > .scoreItem > #' + $(this).prop('id')).parents('.tile').addClass('toRemove').fadeOut();
            } else {

                // If the tile is not there (Meaning it was clicked from the visit list side)
                $(this).parents('.tile-expanded').addClass("toRemove");

            }


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


        /*
           Updates the heart glyph when tile expanded
         */
        if (isFavorite) {
            $(".expanded-tile-container").find(".expanded-glyph").removeClass("glyphicon-heart-empty").addClass('glyphicon-heart');
        } else {
            console.log("not here");
            $(".expanded-tile-container").find(".expanded-glyph").removeClass("glyphicon-heart").addClass('glyphicon-heart-empty');
        }

        $(this).removeClass('bound');
    }
});

function minimize(clickedElement) {

    $(clickedElement).closest('.expanded-tile-container').hide();

    $(clickedElement).parents('.tile-expanded').animate({"height": "115px"}, 200, function () {

        $(clickedElement).parents('.tile-expanded').addClass('tile');
        !$(clickedElement).parents('.tile').siblings('.tile').not('.toRemove').slideDown(200);
        $(clickedElement).parents('.tile').children().show();
        $(clickedElement).parents('.tile').removeClass('tile-expanded');
        $(clickedElement).parents('.tile').addClass('bound');

        $(clickedElement).closest('.expanded-tile-container').remove();

        $('.toRemove').fadeOut();

    })
}

$('.glyphicon-heart, .glyphicon-heart-empty').click(function (e) {
    e.stopPropagation();
});


/********************

 Other  options to achieve a similar effect

 flexbox, animate flex-grow, flex-basis
 Jquery slideDown entrance animation\

 ********************/

