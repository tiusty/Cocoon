clickBind = $('.tile').on('click', function () {

    if (!($(this).hasClass('tile-expanded'))) {
        expand($(this));

        console.log("Clicked on Tile");
    }
});

function zoomInMarker(id) {
     map.setCenter(locationMarkers[id].getPosition());
     map.setZoom(map.zoom + 3);
}

function zoomOutMarker() {
    map.setCenter(map.center);
    map.setZoom(MAPZOOM);
}

function hoverExpandMarker(id) {
    console.log(locationMarkers[id].icon['scale']);

    var currMarker = locationMarkers[id];
    var currIcon = currMarker.icon;
    currIcon.scale = 13;


    locationMarkers[id].setIcon(currIcon);
}

function hoverShrinkMarker(id) {
    var currMarker = locationMarkers[id];
    var icon = currMarker.getIcon();
    icon.scale = 10;


    locationMarkers[id].setIcon(icon);
}

function expandMarker(id) {

    console.log(locationMarkers[id].icon['scale']);

    var currMarker = locationMarkers[id];
    var currIcon = currMarker.icon;
    currIcon.scale = 13;

    locationMarkers[id]["expanded"] = true;
    locationMarkers[id].setIcon(currIcon);
}

function shrinkMarker(id) {

    var currMarker = locationMarkers[id];
    var icon = currMarker.getIcon();
    icon.scale = 10;

    locationMarkers[id]["expanded"] = false;
    locationMarkers[id].setIcon(icon);

}

function expand(aTile) {

    zoomInMarker($(aTile).data('count'));
    expandMarker($(aTile).data('count'));

    if ($(aTile).hasClass('bound')) {
        var isFavorite = $(aTile).find('.heartGlyph').hasClass("glyphicon-heart");
        console.log(isFavorite);
        $(aTile).removeClass('tile');
        $(aTile).addClass('tile-expanded');
        $(aTile).children().hide();
        $(aTile).animate({"height": "65vh"}, 200, function () {
            $(aTile).siblings('.tile').slideUp(150);
        });
        /*
         * Adds the unloaded templated html to the page
         */
        $(aTile).append($(aTile).children('#expanded-tile-contents').html());


        /*
         Updates the heart glyph when tile expanded
         */
        if (isFavorite) {
            $(".expanded-tile-container").find(".expanded-glyph").removeClass("glyphicon-heart-empty").addClass('glyphicon-heart');
        } else {
            console.log("not here");
            $(".expanded-tile-container").find(".expanded-glyph").removeClass("glyphicon-heart").addClass('glyphicon-heart-empty');
        }

        $(aTile).removeClass('bound');
    }
}

function minimize(clickedElement) {

    zoomOutMarker($(clickedElement).parents('.tile-expanded').data('count'));
    shrinkMarker($(clickedElement).parents('.tile-expanded').data('count'));

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

// to be called when a second function should execute after
function minimizeWithCallback(clickedElement, callback, argument) {

    shrinkMarker($(clickedElement).parents('.tile-expanded').data('count'));

    $(clickedElement).closest('.expanded-tile-container').hide();

    $(clickedElement).parents('.tile-expanded').animate({"height": "115px"}, 100, function () {

        $(clickedElement).parents('.tile-expanded').addClass('tile');
        !$(clickedElement).parents('.tile').siblings('.tile').not('.toRemove').show();
        $(clickedElement).parents('.tile').children().show();
        $(clickedElement).parents('.tile').removeClass('tile-expanded');
        $(clickedElement).parents('.tile').addClass('bound');

        $(clickedElement).closest('.expanded-tile-container').remove();

        $('.toRemove').fadeOut();

        callback(argument);
    })

}

$('.glyphicon-heart, .glyphicon-heart-empty, .expanded-close').click(function (e) {
    e.stopPropagation();
});


/********************

 Other  options to achieve a similar effect

 flexbox, animate flex-grow, flex-basis
 Jquery slideDown entrance animation\

 ********************/

