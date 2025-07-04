function updateConfirmBookingButtonState() {
    // Always use window.selectedDates to ensure global access
    const hasSelection = window.selectedDates && window.selectedDates.length > 0;
    // Make sure confirmBookingBtn is defined
    const confirmBookingBtn = document.getElementById('confirm-booking-btn');
    if (confirmBookingBtn) {
        confirmBookingBtn.disabled = !hasSelection;
        confirmBookingBtn.textContent = hasSelection ? 'Confirm Booking' : 'Select a Date First';
        console.log('updateConfirmBookingButtonState: hasSelection =', hasSelection);
    }
}

// Call the function on initial load
updateConfirmBookingButtonState();