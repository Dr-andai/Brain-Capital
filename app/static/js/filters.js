// Filter interactions and utilities

/**
 * Get current filter values for htmx requests
 */
function getFilterValues() {
    const form = document.getElementById('filter-form');
    if (!form) return {};

    const formData = new FormData(form);
    const values = {
        insight_type: 'trend',
        year_start: 2020,
        year_end: 2023,
    };

    // Add form values
    for (const [key, value] of formData.entries()) {
        if (value) {
            values[key] = value;
        }
    }

    return values;
}

/**
 * Reset all filters to default
 */
function resetFilters() {
    const form = document.getElementById('filter-form');
    if (!form) return;

    // Reset form
    form.reset();

    // Reset dynamic selects
    const dimensionSelect = document.getElementById('dimension-select');
    const indicatorSelect = document.getElementById('indicator-select');

    if (dimensionSelect) {
        dimensionSelect.innerHTML = '<option value="">All Dimensions</option>';
    }

    if (indicatorSelect) {
        indicatorSelect.innerHTML = '<option value="">All Indicators</option>';
    }

    // Clear map
    if (window.markersLayer) {
        window.markersLayer.clearLayers();
    }

    // Clear insight
    const insightContent = document.getElementById('insight-content');
    if (insightContent) {
        insightContent.innerHTML = `
            <p class="insight-placeholder">
                Select filters and click "Generate Insight" to get AI-powered analysis of the selected data.
            </p>
        `;
    }

    console.log('Filters reset');
}

/**
 * Update filter statistics
 */
function updateFilterStats() {
    const form = document.getElementById('filter-form');
    const statsContent = document.getElementById('filter-stats-content');

    if (!form || !statsContent) return;

    const formData = new FormData(form);
    const stats = [];

    // Collect selected values
    for (const [key, value] of formData.entries()) {
        if (value) {
            const label = key.replace('_', ' ').replace('id', '').trim();
            const selectElement = form.querySelector(`[name="${key}"]`);
            const selectedText = selectElement?.options[selectElement.selectedIndex]?.text || value;

            if (selectedText && selectedText !== 'All Pillars' && selectedText !== 'All Dimensions' && selectedText !== 'All Indicators') {
                stats.push(`<p><strong>${label}:</strong> ${selectedText}</p>`);
            }
        }
    }

    if (stats.length > 0) {
        statsContent.innerHTML = stats.join('');
    } else {
        statsContent.innerHTML = '<p>No filters applied</p>';
    }
}

/**
 * Listen for filter changes
 */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('filter-form');
    if (form) {
        form.addEventListener('change', () => {
            setTimeout(updateFilterStats, 100);
        });
    }
});

/**
 * Listen for htmx events
 */
document.body.addEventListener('htmx:beforeRequest', (event) => {
    console.log('htmx request starting:', event.detail.path);
});

document.body.addEventListener('htmx:afterRequest', (event) => {
    console.log('htmx request completed:', event.detail.path);
    updateFilterStats();
});

document.body.addEventListener('htmx:responseError', (event) => {
    console.error('htmx error:', event.detail);
    alert('An error occurred while loading data. Please try again.');
});
