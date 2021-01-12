$(document).ready(function () {
  $('#track').owlCarousel({
    loop: true,
    smartSpeed: 2000,
    items: 2,
    margin: 10,
    nav: true,
    responsive: {
      760: {
        items: 4
      },
      1200: {
        items: 5
      }
    }
  })
})
  