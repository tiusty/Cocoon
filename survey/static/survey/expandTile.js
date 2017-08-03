clickBind = $('.tile').bind('click', function () {

    if ($(this).hasClass('bound')) {
         $(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $(this).children().hide();
    $(this).animate({"height": "65vh"}, 150, function () {
        $(this).siblings('.tile').slideUp(200);
    });
    /*
     * Adds the unloaded templated html to the page
     */
    $(this).append($(this).children('#expanded-tile-contents').html());
    $(this).removeClass('bound');
    }
});

function minimize(clickedElement) {

    $(clickedElement).closest('.expanded-tile-container').hide();

    console.log($(clickedElement).parents());

     $(clickedElement).parents('.tile-expanded').animate({"height": "115px"}, 200, function() {

        $(clickedElement).parents('.tile-expanded').addClass('tile');
        $(clickedElement).parents('.tile').siblings('.tile').slideDown(200);
        $(clickedElement).parents('.tile').children().show();
        $(clickedElement).parents('.tile').removeClass('tile-expanded');
        $(clickedElement).parents('.tile').addClass('bound');

        $(clickedElement).closest('.expanded-tile-container').remove();

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

