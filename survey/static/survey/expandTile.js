$('.tile').on('click', ':not(.glyphicon)',  function (e) {
    $(this).parent().addClass('tile-expanded');
})