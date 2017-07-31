$('.tile').bind('click', function () {
    console.log(this)

    $(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $('.tile-expanded').children().hide();
    $(this).animate({"height": "85vh"}, 150, function () {

        $('.tile').hide();
    })
    /*
     * Adds the unloaded templated html to the page
     */
    $(this).append($('#expanded-tile-contents').html());

    $(this).unbind('click');

})

$('.glyphicon-heart, .glyphicon-heart-empty').click(function (e) {
    e.stopPropagation();
})

function clicked() {
    console.log('glyphicon clicked!');
}

/********************

 Other  options to achieve a similar effect

 flexbox, animate flex-grow, flex-basis
 Jquery slideDown entrance animation\

 ********************/

