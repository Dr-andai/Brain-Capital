// htmx configuration and event handlers

/**
 * Configure htmx settings
 */
document.addEventListener('DOMContentLoaded', () => {
    // Configure htmx timeout
    if (typeof htmx !== 'undefined') {
        htmx.config.timeout = 30000; // 30 seconds

        // Enable debug logging in development
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            htmx.logAll();
        }
    }
});

/**
 * Global htmx event handlers
 */

// Before request
document.body.addEventListener('htmx:beforeRequest', (event) => {
    // Could add auth token here if needed
    // event.detail.xhr.setRequestHeader('X-Auth-Token', 'token');
});

// After swap
document.body.addEventListener('htmx:afterSwap', (event) => {
    console.log('Content swapped:', event.detail.target.id);
});

// On error
document.body.addEventListener('htmx:responseError', (event) => {
    console.error('htmx response error:', {
        path: event.detail.path,
        status: event.detail.xhr.status,
        statusText: event.detail.xhr.statusText,
    });
});

// On timeout
document.body.addEventListener('htmx:timeout', (event) => {
    console.error('htmx request timeout:', event.detail.path);
    alert('Request timed out. Please try again.');
});

/**
 * Custom event: map data updated
 */
document.body.addEventListener('mapDataUpdated', (event) => {
    console.log('Map data updated event received');
    if (typeof updateMapData === 'function') {
        updateMapData();
    }
});

/**
 * Add loading states to buttons
 */
document.body.addEventListener('htmx:beforeRequest', (event) => {
    const elt = event.detail.elt;
    if (elt.tagName === 'BUTTON') {
        elt.classList.add('loading');
        elt.disabled = true;
    }
});

document.body.addEventListener('htmx:afterRequest', (event) => {
    const elt = event.detail.elt;
    if (elt.tagName === 'BUTTON') {
        elt.classList.remove('loading');
        elt.disabled = false;
    }
});

console.log('htmx configuration loaded');
