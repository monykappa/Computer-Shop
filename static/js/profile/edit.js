$(document).ready(function () {
    // Load forms into modals
    $('#editUsernameModal').on('show.bs.modal', function (e) {
        var url = $(e.relatedTarget).data('url');
        if (url) {
            $(this).find('.modal-body').load(url);
        } else {
            console.error("URL for username modal is undefined.");
        }
    });

    $('#editFullNameModal').on('show.bs.modal', function (e) {
        var url = $(e.relatedTarget).data('url');
        if (url) {
            $(this).find('.modal-body').load(url);
        } else {
            console.error("URL for full name modal is undefined.");
        }
    });

    $('#editAddressModal').on('show.bs.modal', function (e) {
        var url = $(e.relatedTarget).data('url');
        if (url) {
            $(this).find('.modal-body').load(url, function(response, status, xhr) {
                if (status == "error") {
                    console.error("Error loading address modal:", xhr.status, xhr.statusText);
                }
            });
        } else {
            console.error("URL for address modal is undefined.");
        }
    });


    // Handle form submissions
    $(document).on('submit', '#editAddressForm', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                if (response.error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.error,
                    });
                } else {
                    $('#editAddressModal').modal('hide');
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Address has been updated successfully!',
                    }).then(() => {
                        location.reload();
                    });
                }
            },
            error: function (xhr, status, error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred. Please try again.',
                });
            }
        });
    });

    $(document).on('submit', '#editUsernameForm', function (e) {
        e.preventDefault();
        var username = $('#id_username').val();
        if (username.includes(' ')) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Username',
                text: 'Username cannot contain spaces. Please remove any spaces.',
            });
            return;
        }
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                if (response.error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.error,
                    });
                } else {
                    $('#username').text(response.username);
                    $('#editUsernameModal').modal('hide');
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Username has been updated successfully!',
                    });
                }
            },
            error: function (xhr, status, error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred. Please try again.',
                });
            }
        });
    });

    $(document).on('submit', '#editFullNameForm', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (response) {
                $('#fullName').text(response.full_name);
                $('#editFullNameModal').modal('hide');
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Full name has been updated successfully!',
                });
            },
            error: function (xhr, status, error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred. Please try again.',
                });
            }
        });
    });
});
