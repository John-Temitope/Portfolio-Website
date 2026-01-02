/*!
* Start Bootstrap - Business Frontpage v5.0.9 (https://startbootstrap.com/template/business-frontpage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-frontpage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


 // -- JavaScript to make the navbar responsive -->

document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.getElementById("mainNav");
  const navbarCollapse = document.getElementById("navbarResponsive");

  let lastScrollTop = 0;

  window.addEventListener("scroll", function () {

    // 🚫 Do not hide navbar when mobile menu is open
    if (navbarCollapse.classList.contains("show")) {
      return;
    }

    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
      navbar.classList.add("nav-hidden");
    } else {
      navbar.classList.remove("nav-hidden");
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const offcanvasEl = document.getElementById("offcanvasNavbar");

  offcanvasEl.addEventListener("shown.bs.offcanvas", () => {
    document.body.classList.add("offcanvas-open");
  });

  offcanvasEl.addEventListener("hidden.bs.offcanvas", () => {
    document.body.classList.remove("offcanvas-open");
  });
});

