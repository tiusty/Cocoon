$('.tile').bind('click', ':not(.glyphicon)',  function () {
    $(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $(this).children().hide()
    //$('.tile').hide();

})