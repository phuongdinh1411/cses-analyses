// Main JavaScript file for CSES Analyses site

document.addEventListener('DOMContentLoaded', function() {
  // Add smooth scrolling to all links
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });

  // Add active class to current navigation item
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav__item a, .nav__title a');
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.parentElement.classList.add('active');
    }
  });
}); 