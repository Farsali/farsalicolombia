$(document).ready(function () {
    $('#highlights-carousel').owlCarousel({
      loop: true,
      smartSpeed: 2000,
      items: 2,
      margin: 5,
      nav: true,
      responsive: {
        1270: {
          items: 4,
          margin: 20
        }
      }
    })

    $('#highlights-carousel-2').owlCarousel({
      loop: true,
      smartSpeed: 2000,
      items: 2,
      margin: 5,
      nav: true,
      responsive: {
        1270: {
          items: 4,
          margin: 20
        }
      }
    })
})
  