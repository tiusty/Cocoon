$('.tile').not('.glyphicon').bind('click', function (e) {
    e.stopPropagation()
    console.log(this)

    $(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $('.tile-expanded').children().hide();
    $(this).animate({"height":"750px"}, 150, function() {

        $('.tile').hide();
    })
})

$('.glyphicon').click(function (e) {
    e.stopPropagation();
})

/********************

 Other  options to achieve a similar effect

 flexbox, animate flex-grow, flex-basis
 Jquery slideDown entrance animation\

 ********************/