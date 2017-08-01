clickBind = $('.tile').bind('click', function () {

    if ($(this).hasClass('bound')) {
         $(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $('.tile-expanded').children().hide();
    $(this).animate({"height": "70vh"}, 150, function () {
        $('.tile').hide();
    });
    /*
     * Adds the unloaded templated html to the page
     */
    $(this).append($(this).children('#expanded-tile-contents').html());
    $(this).removeClass('bound');
    }
});

function minimize(clickedElement) {

    $('.expanded-tile-container').remove();

     $('.tile-expanded').animate({"height": "115px"}, 150, function() {
        $('.tile-expanded').addClass('tile');
        $('.tile').show();
        $('.tile-expanded').children().show();
        $('.tile').removeClass('tile-expanded');
        $('.tile').addClass('bound');
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

