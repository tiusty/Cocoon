function handleMenu() {
  /**
   * This function toggles the hamburger menu open/close
   * Toggles class .mobile-links_open
   **/
  document.querySelector('.hamburger-menu').addEventListener('click', function() {
    document.querySelector('.hamburger-menu').classList.toggle('mobile-links_open');
    document.querySelector('.mobile-links').classList.toggle('mobile-links_open');
  });

  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      document.querySelector('.hamburger-menu').classList.remove('mobile-links_open');
      document.querySelector('.mobile-links').classList.remove('mobile-links_open');
    }
  })
}

window.onload = handleMenu;