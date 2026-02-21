// Leaflet map initialization and update logic

let map = null;
let markersLayer = null;

/**
 * Initialize the Leaflet map
 */
function initMap() {
    // Check if map element exists
    const mapElement = document.getElementById('map');
    if (!mapElement) {
        console.error('Map element not found');
        return;
    }

    // Remove old map if it exists
    if (map) {
        try {
            map.remove();
            map = null;
            markersLayer = null;
        } catch (e) {
            console.warn('Error removing old map:', e);
            map = null;
            markersLayer = null;
        }
    }

    // Create new map
    try {
        map = L.map('map').setView([20, 0], 2);

        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19,
        }).addTo(map);

        // Create markers layer
        markersLayer = L.layerGroup().addTo(map);

        // Load initial data
        updateMapData();
    } catch (e) {
        console.error('Error initializing map:', e);
    }
}

/**
 * Get color based on value
 */
function getColorForValue(value, unit) {
    if (value === null || value === undefined) {
        return '#95a5a6'; // Gray for no data
    }

    // For prevalence/rate indicators (lower is better)
    if (unit && unit.includes('per 100k')) {
        if (value < 1000) return '#2ecc71'; // Green - Low prevalence
        if (value < 3000) return '#f39c12'; // Orange - Medium prevalence
        return '#e74c3c'; // Red - High prevalence
    }

    // For index/score indicators (higher is better)
    if (value >= 75) return '#2ecc71'; // Green - High
    if (value >= 50) return '#f39c12'; // Orange - Medium
    return '#e74c3c'; // Red - Low
}

/**
 * Update map with new data
 */
function updateMapData() {
    // Clear existing markers
    if (markersLayer) {
        markersLayer.clearLayers();
    }

    // Get data from hidden script tag
    const mapDataElement = document.getElementById('map-data');
    if (!mapDataElement) {
        console.log('No map data element found');
        return;
    }

    let mapData;
    try {
        mapData = JSON.parse(mapDataElement.textContent);
    } catch (e) {
        console.error('Error parsing map data:', e);
        return;
    }

    if (!mapData || mapData.length === 0) {
        console.log('No map data available');
        return;
    }

    // Add markers for each data point
    mapData.forEach(point => {
        if (!point.latitude || !point.longitude) {
            return;
        }

        const color = getColorForValue(point.value, point.unit);

        // Create circle marker
        const marker = L.circleMarker([point.latitude, point.longitude], {
            radius: 8,
            fillColor: color,
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        });

        // Create popup content
        const popupContent = `
            <div class="map-popup">
                <h4>${point.country_name}</h4>
                <p><strong>Value:</strong> ${point.value !== null ? point.value.toFixed(2) : 'N/A'} ${point.unit || ''}</p>
                <p><small>${point.country_code}</small></p>
            </div>
        `;

        marker.bindPopup(popupContent);
        marker.addTo(markersLayer);
    });

    console.log(`Loaded ${mapData.length} data points on map`);
}

/**
 * Listen for htmx events to update map
 */
document.body.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'map-container') {
        console.log('Map container updated, refreshing map data');
        // Reinitialize map after content swap
        setTimeout(() => {
            initMap();
        }, 200);
    }
});

// Also listen for htmx errors
document.body.addEventListener('htmx:responseError', (event) => {
    console.error('htmx error:', event.detail);
    if (event.detail.target.id === 'map-container') {
        alert('An error occurred while loading data. Please try again.');
    }
});

/**
 * Initialize map on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('map');
    if (mapElement) {
        initMap();
    }
});
