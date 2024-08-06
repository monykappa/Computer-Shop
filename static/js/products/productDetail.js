// Zoom functionality
const zoomWrapper = document.querySelector('.zoom-wrapper');
const img = zoomWrapper.querySelector('img');

zoomWrapper.addEventListener('mousemove', (e) => {
    const rect = zoomWrapper.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const xPercent = (x / rect.width) * 100;
    const yPercent = (y / rect.height) * 100;
    img.style.transformOrigin = `${xPercent}% ${yPercent}%`;
});

zoomWrapper.addEventListener('mouseleave', () => {
    img.style.transformOrigin = 'center center';
});

// Full-screen preview functionality
const modal = document.getElementById('imageModal');
const modalImg = document.getElementById('modalImage');
const closeBtn = document.getElementsByClassName('close')[0];

function openModal(imgSrc) {
    modal.style.display = "block";
    modalImg.src = imgSrc;
}

img.onclick = function () {
    openModal(this.src);
}

const smallImages = document.querySelectorAll('.small-image');
smallImages.forEach(smallImg => {
    smallImg.onclick = function () {
        openModal(this.src);
    }
});

closeBtn.onclick = function () {
    modal.style.display = "none";
}

modal.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

// Ensure this script is included after the above script
document.getElementById('add-to-cart-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const form = this;
    const url = form.action;
    const data = new FormData(form);

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Configure AJAX settings for CSRF token
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // Check if the user is logged in
    $.ajax({
        type: 'GET',
        url: '/check-login-status/',
        success: function (response) {
            if (response.logged_in) {
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function (response) {
                        Swal.fire({
                            title: 'Success',
                            text: 'Product added to cart successfully!',
                            icon: 'success',
                            confirmButtonText: 'OK'
                        });
                    },
                    error: function (xhr) {
                        let errorMsg = 'There was a problem adding the product to the cart.';
                        if (xhr.status === 400) {
                            const response = JSON.parse(xhr.responseText);
                            errorMsg = response.error || errorMsg;
                        }
                        Swal.fire({
                            title: 'Error',
                            text: errorMsg,
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    }
                });
            } else {
                Swal.fire({
                    title: 'Error',
                    text: 'You need to log in to add items to the cart.',
                    icon: 'error',
                    showCancelButton: true,
                    confirmButtonText: 'Sign In',
                    cancelButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = signInUrl;   
                    }
                });
            }
        },
        error: function () {
            Swal.fire({
                title: 'Error',
                text: 'Unable to check login status. Please try again later.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const scrollLeftBtn = document.querySelector('.scroll-left');
    const scrollRightBtn = document.querySelector('.scroll-right');
    const scrollContainer = document.querySelector('.top-selling-items');

    scrollLeftBtn.addEventListener('click', () => {
        scrollContainer.scrollBy({ left: -200, behavior: 'smooth' });
    });

    scrollRightBtn.addEventListener('click', () => {
        scrollContainer.scrollBy({ left: 200, behavior: 'smooth' });
    });
});
