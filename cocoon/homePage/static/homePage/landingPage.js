const Slider = (function() {
  const onboardingSlider = document.getElementById('onboarding');
  const landingPage = document.getElementById('landing-page-body');
  const toggleSliderBtns = document.querySelectorAll('.toggle-slider');
  let onboarding;

  if (onboardingSlider) { onboardingSlider.style.display = 'none'; }


  function addListeners() {
    toggleSliderBtns.forEach(function(slider) {
      slider.addEventListener('click', toggleSlider)
    });
    document.getElementById('learn-1').addEventListener('click', function() {
      goToSlide(0);
    });
    document.getElementById('learn-2').addEventListener('click', function() {
      goToSlide(1);
    });
    document.getElementById('learn-3').addEventListener('click', function() {
      goToSlide(2);
    });
  }

  function initSlider() {
    /**
      * Options for the onboarding slider
    **/
    onboarding = tns({
      container: '.my-slider',
      items: 1,
      mouseDrag: true,
      nav: true,
      navContainer: '.circle-controls',
      navPosition: 'bottom',
      controls: false,
    });

    document.getElementById('slider-prev').addEventListener('click', function () {
      onboarding.goTo('prev');
    });
    document.getElementById('slider-next').addEventListener('click', function () {
      onboarding.goTo('next');
    });

  }

  function toggleSlider() {
    if (onboardingSlider.style.display === 'none') {
      goToSlide(0);
      show(onboardingSlider);
      hide(landingPage);
    } else {
      show(landingPage);
      hide(onboardingSlider);
    }
  }

  function hide(el) {
    el.style.display = 'none';
  }

  function show(el) {
    el.style.display = 'block';
  }

  function goToSlide(number) {
    landingPage.style.display = 'none';
    onboardingSlider.style.display = 'block';
    onboarding.goTo(number);
  }

  return {
    init: function() {
      initSlider();
      addListeners();
    }
  }

})();

const VideoModal = (function() {

  const videoWrapper = document.querySelector('.video-wrapper');

  function addListeners() {
    document.querySelector('.toggle-video').addEventListener('click', toggleVideo);
    document.querySelector('.close-video ').addEventListener('click', toggleVideo);
  }

  function toggleVideo(e) {
    e.stopPropagation();
    e.preventDefault();
    console.log(e)
    if (videoWrapper.style.display === 'none') {
      // show video
      window.scrollTo(0,0);
      videoWrapper.style.display = 'flex';
      document.querySelector('body').style.overflow = 'hidden';
    } else {
      // hide video
      videoWrapper.style.display = 'none';
      document.querySelector('body').style.overflow = 'auto';
    }
  }
  return {
    init: function() {
      addListeners();
    }
  }

})();

(function() {
  /**
    * Runs on load and calls functions that's needed for landing page
    * handleMenu -> creates mobile menu that can toggle
    * AOS -> scroll reveal elements
    * VideoModal adds ability to toggle video modal
    * Slider -> options for onboarding slider
  **/
  AOS.init();
  VideoModal.init();
  Slider.init();
})();