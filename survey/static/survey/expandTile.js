$('.tile').bind('click', ':not(.glyphicon)',  function () {
    //$(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $(this).removeClass('tile');
    $(this).children().hide()
    $('.tile').hide();

})



/********************

 Other  options to achieve a similar effect

 flexbox, animate flex-grow, flex-basis
 Jquery slideDown entrance animation\

 ********************/