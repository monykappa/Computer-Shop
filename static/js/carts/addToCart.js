$(document).ready(function () {
    $('#add-to-cart-form').on('submit', function (event) {
        event.preventDefault();
        console.log('Form submitted');

        var $form = $(this);
        var url = $form.attr('action');
        var data = $form.serialize();

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
                }
            }
        });

        // Check if the user is logged in
        $.ajax({
            type: 'GET',
            url: '/check-login-status/',
            success: function (response) {
                console.log('Login status checked', response);
                if (response.logged_in) {
                    // User is logged in, proceed to add to cart
                    $.ajax({
                        type: 'POST',
                        url: url,
                        data: data,
                        success: function (response) {
                            console.log('Add to cart success', response);
                            // Show success message with SweetAlert
                            Swal.fire({
                                title: 'Success',
                                text: 'Product added to cart successfully!',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            });
                        },
                        error: function (response) {
                            console.log('Add to cart error', response);
                            // Show error message with SweetAlert
                            Swal.fire({
                                title: 'Error',
                                text: 'There was a problem adding the product to the cart.',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    });
                } else {
                    console.log('User not logged in');
                    // User is not logged in, show error message with SweetAlert
                    Swal.fire({
                        title: 'Error',
                        text: 'You need to log in to add items to the cart.',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            },
            error: function () {
                console.log('Login status check failed');
                // Show error message if unable to check login status with SweetAlert
                Swal.fire({
                    title: 'Error',
                    text: 'Unable to check login status. Please try again later.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});
