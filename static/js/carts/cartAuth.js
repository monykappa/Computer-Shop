$(document).ready(function () {
    function updateQuantity(itemId, quantityChange) {
        var button = $('.increase-btn, .decrease-btn').filter(function() {
            return $(this).data('item-id') == itemId;
        });
        var newQuantity = parseInt($('input[data-item-id="' + itemId + '"]').val()) + quantityChange;

        // Retrieve the URL from the data-url attribute
        var updateUrl = button.data('url');

        // Retrieve the CSRF token from the cookies
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: updateUrl,
            type: 'POST',
            data: {
                'quantity': newQuantity,
                'csrfmiddlewaretoken': csrftoken,
            },
            success: function (response) {
                $('#subtotal-' + response.item_id).text('$' + response.subtotal.toFixed(2));
                $('#total-price').text(response.total_price.toFixed(2));
                $('input[data-item-id="' + response.item_id + '"]').val(response.quantity);
                $('#item-count').text(response.item_count);  // Update item count
            },
            error: function (response) {
                console.error('Error updating cart:', response);
            }
        });
    }

    // Event listener for increase button
    $('.increase-btn').on('click', function () {
        var itemId = $(this).data('item-id');
        updateQuantity(itemId, 1); // Increase quantity by 1
    });

    // Event listener for decrease button
    $('.decrease-btn').on('click', function () {
        var itemId = $(this).data('item-id');
        updateQuantity(itemId, -1); // Decrease quantity by 1
    });

    function debounce(func, delay) {
        let debounceTimer;
        return function () {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    }

    // Event listener for input change with debounce
    $('.quantity-input').on('input', debounce(function () {
        var itemId = $(this).data('item-id');
        var newQuantity = parseInt($(this).val());
        if (newQuantity > 0) {
            updateQuantity(itemId, newQuantity);
        } else {
            $(this).val(1); // Reset to 1 if the input is invalid
            updateQuantity(itemId, 1);
        }
    }, 500)); // Adjust the delay as needed

    // Event listener for remove button
    $('.remove-btn').on('click', function () {
        var itemId = $(this).data('item-id');
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, remove it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $('#remove-form-' + itemId).submit();
            }
        });
    });
});
