document.addEventListener('DOMContentLoaded', function () {
    // Loops through each feedback card
    const feedbackCards = document.querySelectorAll('.feedback-card');
    
    feedbackCards.forEach(card => {
        const toggleButton = card.querySelector('.toggle-read-btn');
const isRead = card.dataset.read === 'true';  // Check if feedback is read

// Set the initial tooltip text based on the read status
if (isRead) {
    toggleButton.title = 'Mark as unread';
        } else {
    toggleButton.title = 'Mark as read';
        }
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
    // Resetting button and appereance
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

                // Update tooltip text
                if (isRead) {
                    toggleButton.title = "Mark as unread";
                } else {
                    toggleButton.title = "Mark as read";
                }

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