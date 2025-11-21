// Global state
let allDestinations = [];
let filteredDestinations = [];

// Map marker positions (percentage-based for responsive design)
const markerPositions = {
    'ladakh': { top: '15%', left: '65%' },
    'spiti': { top: '22%', left: '58%' },
    'shimla': { top: '25%', left: '55%' },
    'manali': { top: '23%', left: '57%' },
    'goa': { top: '70%', left: '42%' },
    'gokarna': { top: '72%', left: '44%' },
    'munnar': { top: '85%', left: '52%' },
    'ooty': { top: '82%', left: '54%' },
    'alleppey': { top: '83%', left: '50%' },
    'hampi': { top: '73%', left: '50%' }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDestinations();
    setupSearch();
    setupNavbar();
});

// Load destinations from API
async function loadDestinations() {
    try {
        const response = await fetch('/api/destinations');
        allDestinations = await response.json();
        filteredDestinations = [...allDestinations];
        renderDestinations();
        renderMap();
    } catch (error) {
        console.error('Error loading destinations:', error);
        showError();
    }
}

// Render destination cards
function renderDestinations() {
    const grid = document.getElementById('destinationsGrid');
    
    if (filteredDestinations.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
                <h3>No destinations found</h3>
                <p>Try adjusting your search criteria</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = filteredDestinations.map(dest => `
        <div class="destination-card" onclick="navigateToDestination('${dest.id}')" style="animation: fadeInUp 0.5s ease;">
            <img src="/static/images/destinations/${dest.id}.jpg" alt="${dest.name}" class="card-image" onerror="this.src='/static/images/placeholder.jpg'">
            <div class="card-content">
                <div class="card-header">
                    <div>
                        <h3 class="card-title">${dest.name}</h3>
                        <p class="card-tagline">${dest.tagline}</p>
                    </div>
                    <span class="card-region">${dest.region}</span>
                </div>
                <p class="card-description">${dest.description}</p>
                <div class="card-meta">
                    <span class="meta-item">
                        <span class="meta-icon">🌤️</span>
                        ${dest.best_time}
                    </span>
                    <span class="meta-item">
                        <span class="meta-icon">⏱️</span>
                        ${dest.duration}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

// Render interactive map
function renderMap() {
    const mapContainer = document.getElementById('india-map');
    
    mapContainer.innerHTML = allDestinations.map(dest => {
        const position = markerPositions[dest.id] || { top: '50%', left: '50%' };
        return `
            <div class="map-marker" 
                 style="top: ${position.top}; left: ${position.left};"
                 onclick="navigateToDestination('${dest.id}')"
                 onmouseenter="highlightCard('${dest.id}')"
                 onmouseleave="unhighlightCard('${dest.id}')">
                <div class="map-tooltip">${dest.name}</div>
            </div>
        `;
    }).join('');
}

// Search functionality
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    let debounceTimer;
    
    searchInput.addEventListener('input', function(e) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            performSearch(e.target.value);
        }, 300);
    });
}

async function performSearch(query) {
    if (!query.trim()) {
        filteredDestinations = [...allDestinations];
        renderDestinations();
        return;
    }
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        filteredDestinations = await response.json();
        renderDestinations();
    } catch (error) {
        console.error('Search error:', error);
    }
}

// Navigation
function navigateToDestination(destinationId) {
    window.location.href = `/destination/${destinationId}`;
}

function scrollToDestinations() {
    document.getElementById('destinations').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

// Navbar scroll effect
function setupNavbar() {
    window.addEventListener('scroll', function() {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Card highlighting from map
function highlightCard(destinationId) {
    const cards = document.querySelectorAll('.destination-card');
    cards.forEach(card => {
        if (card.onclick.toString().includes(destinationId)) {
            card.style.transform = 'translateY(-10px)';
            card.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.3)';
            card.style.borderColor = 'var(--primary)';
        }
    });
}

function unhighlightCard(destinationId) {
    const cards = document.querySelectorAll('.destination-card');
    cards.forEach(card => {
        if (card.onclick.toString().includes(destinationId)) {
            card.style.transform = '';
            card.style.boxShadow = '';
            card.style.borderColor = '';
        }
    });
}

// Error handling
function showError() {
    const grid = document.getElementById('destinationsGrid');
    grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
            <h3>Oops! Something went wrong</h3>
            <p>Unable to load destinations. Please try again later.</p>
            <button class="cta-button" onclick="location.reload()">Retry</button>
        </div>
    `;
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add entrance animations on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
setTimeout(() => {
    document.querySelectorAll('.destination-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}, 100);
