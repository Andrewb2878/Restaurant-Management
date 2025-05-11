function handleReservationAction(id, action) {
    const message = action === 'cancel'
        ? "Are you sure you want to cancel this reservation? An email will be sent to the customer."
        : "Are you sure you want to delete this past reservation?";

    if (confirm(message)) {
        fetch(`/reservation/${action}/${id}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`reservation-${id}`).remove();
                    location.reload();
                } else {
                    alert("Action failed.");
                }
            });
    }
}
