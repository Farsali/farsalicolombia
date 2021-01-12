$(document).ready(function () {
    var carousel = $('#product-slider')
  
    if ($(carousel).children().length > 1) {
      $(carousel).owlCarousel({
        loop: true,
        smartSpeed: 2000,
        items: 1,
        margin: 20,
        nav: true,
        navText: [
        '<div class="offers-canis-minor__arrow-left"></div>',
        '<div class="offers-canis-minor__arrow-right"></div>'
        ]
      })
    }
  })
  