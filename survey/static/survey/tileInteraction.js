/**
 * Created by srayment on 7/8/17.
 */

$(document).ready(function () {
    // oversize the contents of the tile when hovered to suggest that
    // it can be expanded when clicked
    $('.tile').mouseover(function(){
        $(this).find('.thumbnailImage').addClass('thumbnailImage-hover');
        $(this).find('.scoreText').addClass('scoreText-hover');
        $(this).find('.infoBit').addClass('infoBit-hover');
    });

    $('.tile').mouseleave(function () {
         $('.thumbnailImage').removeClass('thumbnailImage-hover');
        $('.scoreText').removeClass('scoreText-hover');
        $('.infoBit').removeClass('infoBit-hover');
    });
})