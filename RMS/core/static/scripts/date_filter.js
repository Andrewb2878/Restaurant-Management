function filterByDate(dateInputId, itemClass, headerSelector = null) {
    let selectedDate = document.getElementById(dateInputId).value;
    let items = document.querySelectorAll(`.${itemClass}`);

    items.forEach(function (item) {
        let itemDate = item.getAttribute("data-date");
        item.style.display = (selectedDate === itemDate || selectedDate === "") ? "block" : "none";
    });

    if (headerSelector) {
        let headers = document.querySelectorAll(headerSelector);
        headers.forEach(function (header) {
            let next = header.nextElementSibling;
            let hasVisible = false;
            if (next) {
                let children = next.querySelectorAll(`.${itemClass}`);
                children.forEach(child => {
                    if (child.style.display !== "none") hasVisible = true;
                });
            }
            header.style.display = hasVisible ? "block" : "none";
        });
    }
}

// Wrappers for page-specific use
function filterReservations() {
    filterByDate("filterDate", "reservation-item", "h2.text-yellow-400");
}

function filterSchedules() {
    filterByDate("filterDate", "shift-item");
}
