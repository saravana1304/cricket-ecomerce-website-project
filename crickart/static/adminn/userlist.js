// adminn/static/adminn/userlist.js
document.addEventListener("DOMContentLoaded", function() {
    var statusDropdowns = document.querySelectorAll(".user-status");

    statusDropdowns.forEach(function(dropdown) {
        dropdown.addEventListener("change", function() {
            var userId = this.getAttribute("data-user-id");
            var selectedStatus = this.value;
            updateUserStatus(userId, selectedStatus);
        });
    });

    function updateUserStatus(userId, status) {
        fetch(`/adminn/toggle_user_status/${userId}/${status}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response:", data);
            if (data.success) {
                updateRowStyle(userId, status);
            } else {
                console.error(`Error: ${data.error}`);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function updateRowStyle(userId, status) {
        var row = document.querySelector(`.user-table tr[data-user-id="${userId}"]`);
        if (row) {
            row.classList.remove("blocked", "active");
            row.classList.add(status);
        }
    }

    function getCookie(name) {
        var value = `; ${document.cookie}`;
        var parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});
