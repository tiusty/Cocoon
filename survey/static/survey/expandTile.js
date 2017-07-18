$('.tile').bind('click', ':not(.glyphicon)',  function () {

    console.log(this)

    $(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $('.tile-expanded').children().hide();
    $(this).animate({"height":"750px"}, 150, function() {

        $('.tile').hide();
    })
})


/********************

 Other  options to achieve a similar effect

 flexbox, animate flex-grow, flex-basis
 Jquery slideDown entrance animation\

 ********************/