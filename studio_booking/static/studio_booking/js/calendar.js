// Modern Calendar Manager
class CalendarManager {
    constructor() {
        this.currentDate = new Date();
        this.selectedDates = [];
        this.availableDates = [];
        this.bookedDates = [];
        this.completedEventsByDate = {}; // { 'YYYY-MM-DD': [booking, ...] }
        this.init();
    }

    init() {
        this.bindEvents();
        this.renderCalendar();
        this.fetchAvailability();
        this.fetchCompletedEvents(); // New
        console.log('CalendarManager initialized');
    }

    bindEvents() {
        // Navigation buttons
        document.querySelectorAll('.calendar-nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const direction = btn.dataset.direction;
                this.navigateMonth(direction);
            });
        });

        // Today button
        const todayBtn = document.getElementById('today-btn');
        if (todayBtn) {
            todayBtn.addEventListener('click', () => {
                this.goToToday();
            });
        }

        // Continue button
        const continueBtn = document.querySelector('.continue-btn');
        if (continueBtn) {
            continueBtn.addEventListener('click', () => {
                this.handleContinue();
            });
        }

        // Close popup button
        const closePopupBtn = document.getElementById('close-popup');
        if (closePopupBtn) {
            closePopupBtn.addEventListener('click', () => {
                this.closeBookingPopup();
            });
        }

        // Booking form submission
        const bookingForm = document.getElementById('booking-form');
        if (bookingForm) {
            bookingForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleBookingSubmit(e);
            });
        }

        // Close popup on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeBookingPopup();
            }
        });

        // Close popup on backdrop click
        const popup = document.getElementById('booking-popup');
        if (popup) {
            popup.addEventListener('click', (e) => {
                if (e.target === popup) {
                    this.closeBookingPopup();
                }
            });
        }

        // Listen for date removal from booking manager
        document.addEventListener('dateRemoved', (e) => {
            this.handleDateRemoval(e.detail.date);
        });
    }

    navigateMonth(direction) {
        if (direction === 'next') {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
        } else {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
        }
        this.renderCalendar();
    }

    goToToday() {
        this.currentDate = new Date();
        this.renderCalendar();
    }

    renderCalendar() {
        const calendarGrid = document.querySelector('.calendar-grid');
        if (!calendarGrid) return;

        // Clear existing content
        calendarGrid.innerHTML = '';
        
        // Add day headers
        ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].forEach(day => {
            const dayEl = document.createElement('div');
            dayEl.className = 'calendar-day-header modern-calendar-header';
            dayEl.textContent = day;
            calendarGrid.appendChild(dayEl);
        });

        // Update month display
        const monthEl = document.getElementById('current-month');
        if (monthEl) {
            monthEl.textContent = this.currentDate.toLocaleDateString('en-US', {
                month: 'long',
                year: 'numeric'
            });
        }

        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        // Add empty cells for days before month starts
        for (let i = 0; i < firstDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'calendar-date modern-calendar-date empty-cell';
            emptyCell.dataset.disabled = 'true';
            calendarGrid.appendChild(emptyCell);
        }

        // Add days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const dateCell = document.createElement('div');
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const cellDate = new Date(year, month, day);
            cellDate.setHours(0, 0, 0, 0);
            
            dateCell.className = 'calendar-date modern-calendar-date';
            dateCell.textContent = day;
            dateCell.dataset.date = dateStr;

            // Style based on date status
            if (this.isToday(cellDate, today)) {
                dateCell.classList.add('today');
            }

            if (this.isPastDate(cellDate, today)) {
                dateCell.dataset.disabled = 'true';
                dateCell.classList.add('disabled');
            } else {
                // Only allow selection for future dates
                dateCell.addEventListener('click', () => {
                    this.toggleDateSelection(dateStr, dateCell);
                });

                // Add available class if date is available
                if (this.availableDates.includes(dateStr)) {
                    dateCell.classList.add('available');
                }

                // Add selected class if date is selected
                if (this.selectedDates.includes(dateStr)) {
                    dateCell.classList.add('selected');
                }

                // Add booked class if date is booked
                if (this.bookedDates.includes(dateStr)) {
                    dateCell.classList.add('booked');
                    dateCell.dataset.disabled = 'true';
                }
            }

            // --- Add camera icon for completed events ---
            if (this.completedEventsByDate[dateStr]) {
                dateCell.classList.add('has-event');
                // Add camera SVG icon
                const icon = document.createElement('span');
                icon.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h3l2-3h6l2 3h3a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>`;
                icon.className = 'calendar-event-icon';
                icon.style.position = 'absolute';
                icon.style.right = '15px';
                icon.style.bottom = '8px';
                icon.style.margin = '0';
                icon.style.pointerEvents = 'none';
                dateCell.style.position = 'relative';
                dateCell.appendChild(icon);
                // Add click handler for popup
                dateCell.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.showEventPopup(dateStr);
                });
            }

            calendarGrid.appendChild(dateCell);
        }

        // Update continue button state
        this.updateContinueButton();
        // Update selected dates display
        this.updateSelectedDatesDisplay();
    }

    isToday(date, today) {
        return date.getTime() === today.getTime();
    }

    isPastDate(date, today) {
        return date < today;
    }

    toggleDateSelection(dateStr, dateCell) {
        if (dateCell.dataset.disabled === 'true') return;

        if (this.selectedDates.includes(dateStr)) {
            // Remove selection
            this.selectedDates = this.selectedDates.filter(d => d !== dateStr);
            dateCell.classList.remove('selected');
        } else {
            // Add selection
            this.selectedDates.push(dateStr);
            dateCell.classList.add('selected');
        }

        // Debug log
        console.log('[DEBUG] Selected dates:', this.selectedDates);

        // Update continue button state
        this.updateContinueButton();
        
        // Update selected dates display
        this.updateSelectedDatesDisplay();
    }

    handleDateRemoval(dateStr) {
        this.selectedDates = this.selectedDates.filter(d => d !== dateStr);
        
        // Update UI
        const dateCell = document.querySelector(`[data-date="${dateStr}"]`);
        if (dateCell) {
            dateCell.classList.remove('selected');
        }

        // Update continue button state
        this.updateContinueButton();
        
        // Update selected dates display
        this.updateSelectedDatesDisplay();
    }

    updateContinueButton() {
        const continueBtn = document.querySelector('.continue-btn');
        if (continueBtn) {
            continueBtn.disabled = this.selectedDates.length === 0;
            // Debug log
            console.log('[DEBUG] Continue button state:', continueBtn.disabled ? 'disabled' : 'enabled');
        }
    }

    updateSelectedDatesDisplay() {
        const selectedDatesContainer = document.querySelector('.selected-dates');
        if (!selectedDatesContainer) return;

        if (this.selectedDates.length === 0) {
            selectedDatesContainer.innerHTML = '<div class="text-gray-500 text-sm italic">No dates selected yet</div>';
            return;
        }

        selectedDatesContainer.innerHTML = this.selectedDates
            .sort()
            .map(date => {
                const formattedDate = new Date(date).toLocaleDateString('en-US', {
                    weekday: 'short',
                    month: 'short',
                    day: 'numeric'
                });
                return `
                    <div class="selected-date-item">
                        <span>${formattedDate}</span>
                        <button class="remove-date" data-date="${date}">×</button>
                    </div>
                `;
            })
            .join('');

        // Add event listeners to remove buttons
        selectedDatesContainer.querySelectorAll('.remove-date').forEach(btn => {
            btn.addEventListener('click', () => {
                this.handleDateRemoval(btn.dataset.date);
            });
        });
    }

    handleContinue() {
        console.log('[DEBUG] Continue button clicked. Selected dates:', this.selectedDates);
        if (this.selectedDates.length === 0) return;

        // Validate selected dates
        const invalidDates = this.selectedDates.filter(date => {
            const dateObj = new Date(date);
            return this.isPastDate(dateObj, new Date()) || 
                   this.bookedDates.includes(date) || 
                   !this.availableDates.includes(date);
        });

        if (invalidDates.length > 0) {
            console.error('[DEBUG] Invalid dates selected:', invalidDates);
            return;
        }

        // Show booking popup
        this.showBookingPopup();
    }

    showBookingPopup() {
        const popup = document.getElementById('booking-popup');
        if (popup) {
            popup.classList.add('show');
            document.body.style.overflow = 'hidden';

            // Focus first input
            const firstInput = popup.querySelector('input[type="text"], input[type="email"]');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }

    closeBookingPopup() {
        const popup = document.getElementById('booking-popup');
        if (popup) {
            popup.classList.remove('show');
            document.body.style.overflow = '';
        }
    }

    async handleBookingSubmit(e) {
        e.preventDefault();
        const form = e.target;
        // Collect form data as an object
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        // Add selected dates as an array
        data['dates'] = this.selectedDates;

        try {
            const response = await fetch('/booking/api/book/', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            if (response.ok) {
                // Clear selections and close popup
                this.clearSelections();
                this.closeBookingPopup();
                // Show success message
                this.showToast('Booking successful! We will contact you shortly.', 'success');
                // Refresh calendar
                this.refreshCalendar();
            } else {
                let errorMsg = 'Booking failed';
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.message || errorMsg;
                    if (errorData.errors) {
                        errorMsg += ': ' + Object.entries(errorData.errors).map(([k, v]) => `${k}: ${v.join(', ')}`).join('; ');
                    }
                } catch (e) {}
                throw new Error(errorMsg);
            }
        } catch (error) {
            console.error('Error submitting booking:', error);
            this.showToast(error.message || 'Sorry, there was an error processing your booking. Please try again.', 'error');
        }
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500';
        
        toast.className = `fixed bottom-4 right-4 ${bgColor} text-white px-4 py-2 rounded-lg shadow-lg z-50`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    async fetchAvailability() {
        try {
            const response = await fetch('/booking/api/slots/');
            if (response.ok) {
                const slots = await response.json();
                this.availableDates = slots.map(slot => slot.date);
                this.renderCalendar(); // Re-render to show availability
            }
        } catch (error) {
            console.error('Failed to fetch availability:', error);
        }
    }

    async fetchBookings() {
        try {
            const response = await fetch('/booking/api/bookings/');
            if (response.ok) {
                const bookings = await response.json();
                this.bookedDates = bookings.flatMap(booking => booking.dates || []);
                this.renderCalendar(); // Re-render to show bookings
            }
        } catch (error) {
            console.error('Failed to fetch bookings:', error);
        }
    }

    async fetchCompletedEvents() {
        try {
            const response = await fetch('/booking/api/bookings/?status=completed');
            if (response.ok) {
                const bookings = await response.json();
                // Map: { 'YYYY-MM-DD': [booking, ...] }
                this.completedEventsByDate = {};
                bookings.forEach(booking => {
                    (booking.dates || []).forEach(date => {
                        if (!this.completedEventsByDate[date]) this.completedEventsByDate[date] = [];
                        this.completedEventsByDate[date].push(booking);
                    });
                });
                this.renderCalendar(); // Re-render to show icons
            }
        } catch (error) {
            console.error('Failed to fetch completed events:', error);
        }
    }

    refreshCalendar() {
        this.fetchAvailability();
        this.fetchBookings();
        this.fetchCompletedEvents(); // Refresh completed events
    }

    clearSelections() {
        this.selectedDates = [];
        document.querySelectorAll('.calendar-date').forEach(cell => {
            cell.classList.remove('selected');
        });
        this.updateContinueButton();
        this.updateSelectedDatesDisplay();
    }

    showEventPopup(dateStr) {
        const events = this.completedEventsByDate[dateStr] || [];
        if (events.length === 0) return;
        // Build popup HTML (modern card style)
        let html = '';
        events.forEach(event => {
            html += `
            <div class="calendar-event-modal-card" style="background:#fff;border-radius:1.2rem;box-shadow:0 8px 32px rgba(0,0,0,0.10);max-width:700px;margin:2rem auto;overflow:hidden;">
                <div class="calendar-event-modal-header" style="display:flex;align-items:center;justify-content:space-between;padding:1.2rem 1.5rem 0.5rem 1.5rem;">
                    <div style="display:flex;align-items:center;gap:0.7rem;">
                        <span style="font-size:1.6rem;display:inline-flex;align-items:center;justify-content:center;background:#f3f4f6;border-radius:8px;padding:0.4rem;">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h3l2-3h6l2 3h3a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                        </span>
                        <div>
                            <div style="font-size:1.2rem;font-weight:700;">${event.session_type ? capitalize(event.session_type.replace('_',' ')) : 'Event'}</div>
                            <div style="font-size:0.98rem;color:#64748b;">${dateStr}</div>
                        </div>
                    </div>
                    <button onclick="document.getElementById('calendar-event-modal').style.display='none'" style="background:none;border:none;font-size:2rem;color:#64748b;cursor:pointer;line-height:1;">&times;</button>
                </div>
                <div class="calendar-event-modal-details" style="padding:0 1.5rem 1.2rem 1.5rem;">
                    <div style="display:flex;flex-wrap:wrap;gap:2.5rem 2.5rem;margin-bottom:1.2rem;">
                        <div style="min-width:180px;">
                            <div style="font-size:0.97rem;color:#64748b;">Client</div>
                            <div style="font-weight:600;">${event.client_name || ''}</div>
                        </div>
                        <div style="min-width:180px;">
                            <div style="font-size:0.97rem;color:#64748b;">Location</div>
                            <div style="font-weight:600;">${event.location || '-'}</div>
                        </div>
                        <div style="min-width:120px;">
                            <div style="font-size:0.97rem;color:#64748b;">Duration</div>
                            <div style="font-weight:600;">${event.duration ? event.duration + ' hour' + (event.duration > 1 ? 's' : '') : '-'}</div>
                        </div>
                    </div>
                    <div style="margin-bottom:1.2rem;">
                        <div style="font-size:0.97rem;color:#64748b;margin-bottom:0.3rem;">Work Gallery</div>
                        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:0.7rem;">
                            ${(event.gallery_images || []).map(img => `<img src="${img}" style="width:100%;max-width:120px;max-height:90px;object-fit:cover;border-radius:8px;box-shadow:0 2px 8px #0001;">`).join('')}
                        </div>
                    </div>
                    ${event.testimonial ? `<div style=\"margin-top:1.2rem;padding:1rem 1.2rem;background:#f8fafc;border-radius:0.8rem;border:1.5px solid #e5e7eb;\">
                        <div style=\"font-size:0.97rem;color:#64748b;margin-bottom:0.3rem;\"><strong>Client Testimonial:</strong></div>
                        <div style=\"font-style:italic;\">\"${event.testimonial}\"</div>
                    </div>` : ''}
                </div>
            </div>
            `;
        });
        const modal = document.getElementById('calendar-event-modal');
        const modalContent = document.getElementById('calendar-event-modal-content');
        modalContent.innerHTML = html;
        modal.style.display = 'flex';
    }
}

// Helper function for capitalization
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.calendarManager = new CalendarManager();
    
    // Make refresh function globally available
    window.refreshCalendar = () => {
        if (window.calendarManager) {
            window.calendarManager.refreshCalendar();
        }
    };
    
    console.log('Calendar system initialized');
});

// Export for global access
window.CalendarManager = CalendarManager;

