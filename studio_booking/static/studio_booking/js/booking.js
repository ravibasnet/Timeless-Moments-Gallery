// booking.js is now disabled to avoid conflicts with calendar.js
// All logic is commented out.

/*
// Simplified Booking Form Handler
class BookingManager {
    constructor() {
        this.selectedDates = [];
        this.isSubmitting = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateUI();
        console.log('BookingManager initialized');
    }

    bindEvents() {
        // Confirm booking button
        const confirmBtn = document.getElementById('confirm-booking-btn');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.showBookingForm();
            });
        }

        // Close popup button
        const closeBtn = document.getElementById('close-booking-popup');
        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.hideBookingForm();
            });
        }

        // Form submission
        const form = document.getElementById('booking-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitBooking();
            });
        }

        // Test API button
        const testBtn = document.getElementById('test-api-btn');
        if (testBtn) {
            testBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.testAPI();
            });
        }

        // Validate form button
        const validateBtn = document.getElementById('validate-form-btn');
        if (validateBtn) {
            validateBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.validateForm();
            });
        }

        // Listen for date selection events from calendar
        document.addEventListener('dateSelected', (e) => {
            this.handleDateSelection(e.detail);
        });

        // Close popup on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideBookingForm();
            }
        });

        // Close popup on backdrop click
        const popup = document.getElementById('booking-form-popup');
        if (popup) {
            popup.addEventListener('click', (e) => {
                if (e.target === popup) {
                    this.hideBookingForm();
                }
            });
        }
    }

    handleDateSelection(dateInfo) {
        const { date, selected } = dateInfo;
        
        if (selected) {
            if (!this.selectedDates.includes(date)) {
                this.selectedDates.push(date);
            }
        } else {
            this.selectedDates = this.selectedDates.filter(d => d !== date);
        }
        
        this.updateUI();
        console.log('Selected dates:', this.selectedDates);
    }

    updateUI() {
        this.updateConfirmButton();
        this.updateSelectedDatesDisplay();
    }

    updateConfirmButton() {
        const confirmBtn = document.getElementById('confirm-booking-btn');
        if (confirmBtn) {
            const hasSelection = this.selectedDates.length > 0;
            confirmBtn.disabled = !hasSelection;
            confirmBtn.textContent = hasSelection ? 'Confirm Booking' : 'Select a Date First';
            
            if (hasSelection) {
                confirmBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                confirmBtn.classList.add('hover:bg-primary-700');
            } else {
                confirmBtn.classList.add('opacity-50', 'cursor-not-allowed');
                confirmBtn.classList.remove('hover:bg-primary-700');
            }
        }
    }

    updateSelectedDatesDisplay() {
        const container = document.getElementById('selected-dates-chips');
        if (!container) return;

        container.innerHTML = '';

        if (this.selectedDates.length === 0) {
            container.innerHTML = '<div class="text-gray-500 italic text-sm">No dates selected</div>';
            return;
        }

        this.selectedDates.forEach(dateStr => {
            const date = new Date(dateStr);
            const formattedDate = date.toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });

            const chip = document.createElement('div');
            chip.className = 'bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm flex items-center gap-2';
            chip.innerHTML = `
                <span>${formattedDate}</span>
                <button type="button" class="text-primary-600 hover:text-primary-800 font-bold" data-date="${dateStr}">
                    ×
                </button>
            `;

            // Add remove functionality
            const removeBtn = chip.querySelector('button');
            removeBtn.addEventListener('click', () => {
                this.removeDate(dateStr);
            });

            container.appendChild(chip);
        });
    }

    removeDate(dateStr) {
        this.selectedDates = this.selectedDates.filter(d => d !== dateStr);
        this.updateUI();
        
        // Update calendar UI
        const dateCell = document.querySelector(`[data-date="${dateStr}"]`);
        if (dateCell) {
            dateCell.classList.remove('bg-yellow-200', 'border-yellow-400');
        }

        // Dispatch event for calendar
        document.dispatchEvent(new CustomEvent('dateRemoved', {
            detail: { date: dateStr }
        }));
    }

    showBookingForm() {
        if (this.selectedDates.length === 0) {
            this.showToast('Please select at least one date for your booking.', 'warning');
            return;
        }

        const popup = document.getElementById('booking-form-popup');
        const content = document.getElementById('popup-content');
        
        if (popup && content) {
            popup.classList.remove('hidden');
            popup.classList.add('flex');
            
            // Trigger animation
            setTimeout(() => {
                content.classList.remove('scale-95', 'opacity-0');
                content.classList.add('scale-100', 'opacity-100');
            }, 10);

            // Prevent body scroll
            document.body.style.overflow = 'hidden';
            
            // Update selected dates display
            this.updateSelectedDatesDisplay();
            
            // Focus first input
            const firstInput = popup.querySelector('input[type="text"], input[type="email"]');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }

    hideBookingForm() {
        const popup = document.getElementById('booking-form-popup');
        const content = document.getElementById('popup-content');
        
        if (popup && content) {
            // Trigger animation
            content.classList.remove('scale-100', 'opacity-100');
            content.classList.add('scale-95', 'opacity-0');
            
            setTimeout(() => {
                popup.classList.add('hidden');
                popup.classList.remove('flex');
                document.body.style.overflow = '';
            }, 300);
        }
    }

    getCSRFToken() {
        // Try meta tag first
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag && metaTag.content) {
            return metaTag.content;
        }
        
        // Try cookie
        const value = `; ${document.cookie}`;
        const parts = value.split(`; csrftoken=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        
        // Try Django's default CSRF token from template
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfInput) {
            return csrfInput.value;
        }
        
        console.error('CSRF token not found');
        return null;
    }

    validateForm() {
        const form = document.getElementById('booking-form');
        if (!form) return false;

        const formData = new FormData(form);
        const formDataObj = {};
        
        // Convert FormData to object
        for (const [key, value] of formData.entries()) {
            formDataObj[key] = value;
        }
        
        // Add selected dates
        formDataObj.dates = this.selectedDates;
        
        // Check required fields
        const requiredFields = [
            'client_name', 'client_email', 'client_phone', 
            'session_type', 'start_time', 'duration', 'location'
        ];
        
        const missingFields = requiredFields.filter(field => !formDataObj[field]);
        
        if (missingFields.length > 0) {
            this.showToast(`Missing required fields: ${missingFields.join(', ')}`, 'error');
            return false;
        }
        
        // Check dates
        if (this.selectedDates.length === 0) {
            this.showToast('Please select at least one date', 'error');
            return false;
        }
        
        return true;
    }

    testAPI() {
        const form = document.getElementById('booking-form');
        if (!form) {
            this.showToast('Form not found', 'error');
            return;
        }

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.dates = this.selectedDates;
        data.client = 1; // Default client ID

        console.log('Test API Data:', data);
        this.showToast('Test data logged to console. Check developer tools.', 'info');
    }

    async submitBooking() {
        if (this.isSubmitting) return;
        if (!this.validateForm()) return;

        this.isSubmitting = true;
        this.setSubmitButtonLoading(true);

        const form = document.getElementById('booking-form');
        const formData = new FormData(form);
        
        // Add selected dates
        formData.append('dates', JSON.stringify(this.selectedDates));

        try {
            const response = await fetch('/booking/api/create/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                this.showToast('Booking created successfully!', 'success');
                this.resetForm();
                
                // Refresh calendar if function exists
                if (typeof window.refreshCalendar === 'function') {
                    window.refreshCalendar();
                }
            } else {
                const data = await response.json();
                throw new Error(data.message || 'Failed to create booking');
            }
        } catch (error) {
            console.error('Error creating booking:', error);
            this.showToast(error.message || 'Error creating booking', 'error');
        } finally {
            this.isSubmitting = false;
            this.setSubmitButtonLoading(false);
        }
    }

    setSubmitButtonLoading(loading) {
        const submitBtn = document.getElementById('submit-booking-btn');
        const spinner = document.getElementById('booking-spinner');
        
        if (submitBtn) {
            submitBtn.disabled = loading;
            submitBtn.classList.toggle('opacity-75', loading);
        }
        
        if (spinner) {
            spinner.classList.toggle('hidden', !loading);
        }
    }

    resetForm() {
        const form = document.getElementById('booking-form');
        if (form) {
            form.reset();
        }
        
        // Clear selected dates
        this.selectedDates = [];
        this.updateUI();
        
        // Clear calendar selections
        document.querySelectorAll('[data-date]').forEach(cell => {
            cell.classList.remove('bg-yellow-200', 'border-yellow-400');
        });
    }

    showToast(message, type = 'info') {
        // Remove existing toasts
        document.querySelectorAll('.booking-toast').forEach(toast => toast.remove());

        const toast = document.createElement('div');
        toast.className = `booking-toast fixed top-4 right-4 px-4 py-3 rounded-lg shadow-lg z-50 max-w-sm`;
        
        switch (type) {
            case 'success':
                toast.classList.add('bg-green-500', 'text-white');
                break;
            case 'error':
                toast.classList.add('bg-red-500', 'text-white');
                break;
            case 'warning':
                toast.classList.add('bg-yellow-500', 'text-white');
                break;
            default:
                toast.classList.add('bg-blue-500', 'text-white');
        }

        toast.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button class="ml-2 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        document.body.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.bookingManager = new BookingManager();
    console.log('Booking system initialized');
});

// Export for global access
window.BookingManager = BookingManager;
*/

