clickBind = $('.tile').on('click', function () {

    if (!($(this).hasClass('tile-expanded'))) {
        expand($(this));

        console.log("Clicked on Tile");
    }
});

/**
 * Centers the map on a marker and zooms in
 *
 * @param id - the ID property value of the marker
 * that corresponds with a tile
 */
function zoomInMarker(id) {
     map.setCenter(locationMarkers[id].getPosition());

     if ((map.zoom + 2) < 14) {
         map.setZoom(map.zoom + 2);
     }
}

/**
 * Re-centers the map on Boston and zooms out
 * to the default
 */
function zoomOutMarker() {
    map.setCenter(map.center);
    map.setZoom(MAPZOOM);
}

/**
 * Expands the marker circle
 *
 * @param id - the ID property value of the marker
 * that corresponds with a tile
 */
function hoverExpandMarker(id) {
    var currMarker = locationMarkers[id];
    var currIcon = currMarker.icon;
    currIcon.scale = 13;
    locationMarkers[id].setIcon(currIcon);
}

/**
 * Shrinks the marker circle
 *
 * @param id - the ID property value of the marker
 * that corresponds with a tile
 */
function hoverShrinkMarker(id) {
    var currMarker = locationMarkers[id];
    var icon = currMarker.getIcon();
    icon.scale = 10;
    locationMarkers[id].setIcon(icon);
}

/**
 * Expands the marker circle and sets its 'expanded' value
 * to true so that 'mouseoff' doesn't shrink it
 *
 * @param id - the ID property value of the marker
 * that corresponds with a tile
 */
function expandMarker(id) {
    var currMarker = locationMarkers[id];
    var currIcon = currMarker.icon;
    currIcon.scale = 13;

    locationMarkers[id]["expanded"] = true;
    locationMarkers[id].setIcon(currIcon);
}

/**
 * Shrinks the marker circle and sets its 'expanded' value
 * to false so that 'mouseoff' can shrink it
 *
 * @param id - the ID property value of the marker
 * that corresponds with a tile
 */
function shrinkMarker(id) {

    var currMarker = locationMarkers[id];
    var icon = currMarker.getIcon();
    icon.scale = 10;

    locationMarkers[id]["expanded"] = false;
    locationMarkers[id].setIcon(icon);

}

/**
 * Function that converts a tile into an expanded tile
 * with the necessary animations. Also expands the corresponding
 * map pin
 *
 * @param aTile - the tile to be expanded
 */
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
 * and adds back removed tiles, with animations. Also shrinks
 * the map pin back down.
 *
 * @param clickedElement - the clicked minimize button
 */
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

/**
 * Same functionality as minimize, but runs a callback on completion.
 *
 * Note: This is typically used when expansion of another tile should
 * occur directly after a tile is minimized.
 *
 * @param clickedElement - the clicked minimize button
 * @param callback - the function to execute after
 * @param argument - argument to pass to the callback
 */
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

// Prevents container element from triggering click event
$('.glyphicon-heart, .glyphicon-heart-empty, .expanded-close').click(function (e) {
    e.stopPropagation();
});