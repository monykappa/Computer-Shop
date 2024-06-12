// Function to check if username is available
function checkUsernameAvailability() {
    const username = document.getElementById("username").value;
    fetch("/check-username/?username=" + encodeURIComponent(username))
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const errorDiv = document.getElementById("username-error");
            if (data.is_taken) {
                errorDiv.textContent = data.message;
                errorDiv.style.display = "block";
            } else {
                errorDiv.style.display = "none";
            }
        })
        .catch(error => {
            console.error("Error checking username availability:", error);
        });
}

// Function to check if email is available
function checkEmailAvailability() {
    const email = document.getElementById("email").value;
    fetch("/check-email/?email=" + encodeURIComponent(email))
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const errorDiv = document.getElementById("email-error");
            if (data.is_taken) {
                errorDiv.textContent = data.message;
                errorDiv.style.display = "block";
            } else {
                errorDiv.style.display = "none";
            }
        })
        .catch(error => {
            console.error("Error checking email availability:", error);
        });
}



document.getElementById("username").addEventListener("input", checkUsernameAvailability);
document.getElementById("email").addEventListener("input", checkEmailAvailability);
