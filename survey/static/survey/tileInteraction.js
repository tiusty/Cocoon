/**
 * Created by srayment on 7/8/17.
 */

$(document).ready(function () {

    /************************************************************

    Note: This functionality is now executed with django template

    // sets the color of the score based on the value
    $('.scoreText').each(function () {

        var scoreValue = parseInt($(this).text())

        if (scoreValue > 86) {
            $(this).addClass('great-match');
        } else if (scoreValue > 79 ) {
            $(this).addClass('good-match');
        } else if (scoreValue > 69) {
            $(this).addClass('acceptable-match');
        } else if (scoreValue > 59) {
            $(this).addClass('bad-match');
        } else {
            $(this).addClass('terrible-match');
        }
    });

    ************************************************************/

    // oversize the contents of the tile when hovered to suggest that
    // it can be expanded when clicked
    $('.tile').mouseover(function(){
        $(this).find('#thumbnailItem1').addClass('thumbnailItem1-hover');
        $(this).find('.thumbnailItem').addClass('thumbnailItem-hover');
        $(this).find('.thumbnailImage').addClass('thumbnailImage-hover');
        $(this).find('.scoreText').addClass('scoreText-hover');
        $(this).find('.infoBit').addClass('infoBit-hover');
    });

    $('.tile').mouseleave(function () {
        $(this).find('#thumbnailItem1').removeClass('thumbnailItem1-hover');
        $(this).find('.thumbnailItem').removeClass('thumbnailItem-hover');
        $('.thumbnailImage').removeClass('thumbnailImage-hover');
        $('.scoreText').removeClass('scoreText-hover');
        $('.infoBit').removeClass('infoBit-hover');
    });

    $('.tile').click(function() {
        addChosenMarker($(this).data().address);
    })
})
