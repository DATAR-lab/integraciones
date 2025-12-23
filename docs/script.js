// Navigation Menu Toggle
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
const navOverlay = document.getElementById('navOverlay');
const navLinks = document.querySelectorAll('.nav-menu a');

function toggleMenu() {
    navToggle.classList.toggle('active');
    navMenu.classList.toggle('active');
    navOverlay.classList.toggle('active');
}

function closeMenu() {
    navToggle.classList.remove('active');
    navMenu.classList.remove('active');
    navOverlay.classList.remove('active');
}

navToggle.addEventListener('click', toggleMenu);
navOverlay.addEventListener('click', closeMenu);

// Close menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            closeMenu();
            setTimeout(() => {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        }
    });
});

// Close menu on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        closeMenu();
    }
});

