// Mobile Menu Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Create mobile menu toggle button
    const mobileToggle = document.createElement('button');
    mobileToggle.className = 'mobile-menu-toggle';
    mobileToggle.innerHTML = '☰';
    mobileToggle.setAttribute('aria-label', 'Toggle navigation menu');
    document.body.appendChild(mobileToggle);

    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // Get sidebar element
    const sidebar = document.querySelector('.sidebar');
    
    if (!sidebar) {
        console.warn('Sidebar element not found');
        return;
    }

    // Toggle sidebar function
    function toggleSidebar() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        
        // Update aria-expanded for accessibility
        const isOpen = sidebar.classList.contains('active');
        mobileToggle.setAttribute('aria-expanded', isOpen);
        
        // Prevent body scroll when sidebar is open
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }

    // Close sidebar function
    function closeSidebar() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    // Event listeners
    mobileToggle.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);

    // Close sidebar when clicking on nav links (mobile only)
    const navLinks = sidebar.querySelectorAll('.nav__item > a, .nav__sub-item > a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Only close on mobile screens
            if (window.innerWidth < 768) {
                closeSidebar();
            }
        });
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        // Close sidebar on desktop
        if (window.innerWidth >= 768) {
            closeSidebar();
        }
    });

    // Handle escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            closeSidebar();
        }
    });

    // Smooth scroll for anchor links
    const anchorLinks = sidebar.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close sidebar on mobile after smooth scroll
                if (window.innerWidth < 768) {
                    setTimeout(closeSidebar, 300);
                }
            }
        });
    });

    // Add keyboard navigation support
    let currentFocusIndex = -1;
    const focusableElements = sidebar.querySelectorAll('a, button');
    
    sidebar.addEventListener('keydown', function(e) {
        if (!sidebar.classList.contains('active')) return;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                currentFocusIndex = Math.min(currentFocusIndex + 1, focusableElements.length - 1);
                focusableElements[currentFocusIndex].focus();
                break;
            case 'ArrowUp':
                e.preventDefault();
                currentFocusIndex = Math.max(currentFocusIndex - 1, 0);
                focusableElements[currentFocusIndex].focus();
                break;
            case 'Home':
                e.preventDefault();
                currentFocusIndex = 0;
                focusableElements[currentFocusIndex].focus();
                break;
            case 'End':
                e.preventDefault();
                currentFocusIndex = focusableElements.length - 1;
                focusableElements[currentFocusIndex].focus();
                break;
        }
    });

    // Initialize focus index when sidebar opens
    mobileToggle.addEventListener('click', function() {
        if (sidebar.classList.contains('active')) {
            currentFocusIndex = 0;
            // Focus first link after a short delay
            setTimeout(() => {
                const firstLink = sidebar.querySelector('a');
                if (firstLink) firstLink.focus();
            }, 100);
        }
    });
});