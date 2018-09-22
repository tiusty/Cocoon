/**
 * Created by srayment on 7/8/17.
 */


/*

 Hover event listeners that expand and shrink
 tile contents and expand/shrink corresponding
 map pins

 */
$(document).ready(function () {

    $('.tile').mouseover(function(){
        $(this).find('#thumbnailItem1').addClass('thumbnailItem1-hover');
        $(this).find('.thumbnailItem').addClass('thumbnailItem-hover');
        $(this).find('.thumbnailImage').addClass('thumbnailImage-hover');
        $(this).find('.scoreText').addClass('scoreText-hover');
        $(this).find('.infoBit').addClass('infoBit-hover');

        if (!locationMarkers[$(this).data('count')]["expanded"]) {
            hoverExpandMarker($(this).data('count'))
        }
    });

    $('.tile').mouseleave(function () {
        $(this).find('#thumbnailItem1').removeClass('thumbnailItem1-hover');
        $(this).find('.thumbnailItem').removeClass('thumbnailItem-hover');
        $('.thumbnailImage').removeClass('thumbnailImage-hover');
        $('.scoreText').removeClass('scoreText-hover');
        $('.infoBit').removeClass('infoBit-hover');
        if (!locationMarkers[$(this).data('count')]["expanded"]) {
            hoverShrinkMarker($(this).data('count'));
        }

    });

})
