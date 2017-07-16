$('.tile').bind('click', ':not(.glyphicon)',  function (e) {
    e.stop
    $(this).removeClass('tile');
    $(this).addClass('tile-expanded');
    $(this).empty()
    $('.tile').hide();

})