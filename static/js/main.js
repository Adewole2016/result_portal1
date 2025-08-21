// Main JavaScript for Result Computation Portal

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // File upload drag and drop
    var fileUploadAreas = document.querySelectorAll('.file-upload-area');
    fileUploadAreas.forEach(function(area) {
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            area.classList.add('dragover');
        });

        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
        });

        area.addEventListener('drop', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
            
            var files = e.dataTransfer.files;
            var fileInput = area.querySelector('input[type="file"]');
            if (fileInput && files.length > 0) {
                fileInput.files = files;
                updateFileUploadText(area, files[0].name);
            }
        });
    });

    // File input change handler
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            var area = input.closest('.file-upload-area');
            if (area && e.target.files.length > 0) {
                updateFileUploadText(area, e.target.files[0].name);
            }
        });
    });

    // Confirmation dialogs
    var confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            var message = button.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Loading states for forms
    var submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var form = button.closest('form');
            if (form && form.checkValidity()) {
                button.disabled = true;
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(function() {
                    button.disabled = false;
                    button.innerHTML = button.getAttribute('data-original-text') || 'Submit';
                }, 10000);
            }
        });
    });

    // Store original button text
    submitButtons.forEach(function(button) {
        button.setAttribute('data-original-text', button.innerHTML);
    });

    // Search functionality
    var searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var searchTerm = input.value.toLowerCase();
            var targetSelector = input.getAttribute('data-target');
            var targets = document.querySelectorAll(targetSelector);
            
            targets.forEach(function(target) {
                var text = target.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    target.style.display = '';
                } else {
                    target.style.display = 'none';
                }
            });
        });
    });

    // Table sorting
    var sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(function(header) {
        header.addEventListener('click', function() {
            var table = header.closest('table');
            var tbody = table.querySelector('tbody');
            var rows = Array.from(tbody.querySelectorAll('tr'));
            var column = Array.from(header.parentNode.children).indexOf(header);
            var isAscending = header.classList.contains('asc');
            
            // Remove sorting classes from all headers
            sortableHeaders.forEach(function(h) {
                h.classList.remove('asc', 'desc');
            });
            
            // Add appropriate class to current header
            header.classList.add(isAscending ? 'desc' : 'asc');
            
            // Sort rows
            rows.sort(function(a, b) {
                var aValue = a.children[column].textContent.trim();
                var bValue = b.children[column].textContent.trim();
                
                // Try to parse as numbers
                var aNum = parseFloat(aValue);
                var bNum = parseFloat(bValue);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return isAscending ? bNum - aNum : aNum - bNum;
                } else {
                    return isAscending ? 
                        bValue.localeCompare(aValue) : 
                        aValue.localeCompare(bValue);
                }
            });
            
            // Reorder rows in DOM
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        });
    });

    // Print functionality
    var printButtons = document.querySelectorAll('.print-btn');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Export functionality
    var exportButtons = document.querySelectorAll('.export-btn');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var format = button.getAttribute('data-format');
            var url = button.getAttribute('data-url');
            
            if (url) {
                window.location.href = url + '?format=' + format;
            }
        });
    });
});

// Utility functions
function updateFileUploadText(area, filename) {
    var textElement = area.querySelector('.upload-text');
    if (textElement) {
        textElement.textContent = 'Selected: ' + filename;
    }
}

function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

function showAlert(message, type = 'info') {
    var alertContainer = document.querySelector('.alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'alert-container';
        document.querySelector('.container').prepend(alertContainer);
    }
    
    var alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, 5000);
}

// AJAX helper function
function makeAjaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
    });
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

