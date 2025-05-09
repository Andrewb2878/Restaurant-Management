document.addEventListener('DOMContentLoaded', function () {
    // Loops through each feedback card
    const feedbackCards = document.querySelectorAll('.feedback-card');

    feedbackCards.forEach(card => {
        const toggleButton = card.querySelector('.toggle-read-btn');
        const isRead = card.dataset.read === 'true';  // Check if feedback is read

        // Set the initial tooltip text and icon based on the read status
        updateToggleButtonIcon(toggleButton, isRead);
    });
});

let showUnreadOnly = false;  // Initial filter state

function toggleUnreadFilter() {
    showUnreadOnly = !showUnreadOnly;
    const button = document.getElementById("filterToggle");
    const feedbackList = document.getElementById("feedbackList");

    // Toggle button text and appearance
    if (showUnreadOnly) {
        button.textContent = "Show All Feedback";
        button.classList.add("bg-yellow-600");
        button.classList.remove("hover:bg-yellow-600");
    } else {
        // Resetting button and appearance
        button.textContent = "Show Unread Only";
        button.classList.remove("bg-yellow-600");
        button.classList.add("hover:bg-yellow-600");
    }

    // Filter feedback
    const feedbackItems = feedbackList.querySelectorAll(".feedback-card");
    feedbackItems.forEach(card => {
        const isRead = card.dataset.read === "true";
        if (showUnreadOnly && isRead) {
            card.style.display = "none";  // Hide read feedback
        } else {
            card.style.display = "block"; // Show all feedback
        }
    });
}

function markAsRead(id) {
    fetch(`/core/feedback/toggle-read/${id}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const card = document.getElementById(`feedback-${id}`);
                const toggleButton = card.querySelector(".toggle-read-btn");
                const isRead = data.read;

                // Toggle dimming for text and background
                card.classList.toggle('opacity-50');  // Dim the text
                card.classList.toggle('bg-opacity-50');  // Dim the background
                card.dataset.read = isRead ? "true" : "false";

                // Update tooltip text and icon
                toggleButton.title = isRead ? "Mark as unread" : "Mark as read";
                updateToggleButtonIcon(toggleButton, isRead);

                // If currently filtering unread, hide the card if now marked as read
                if (showUnreadOnly && isRead) {
                    card.style.display = "none";
                } else {
                    card.style.display = "block";
                }
            }
        });
}

function deleteFeedback(id) {
    if (confirm("Are you sure you want to delete this feedback?")) {
        fetch(`/core/feedback/delete/${id}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`feedback-${id}`).remove();
                }
            });
    }
}

// Helper function to update the toggle button icon based on the read status
function updateToggleButtonIcon(button, isRead) {
    if (isRead) {
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
            </svg>
        `;
    } else {
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
            </svg>
        `;
    }
}
