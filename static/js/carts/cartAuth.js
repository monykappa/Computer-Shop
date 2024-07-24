function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleLoadingScreen(show) {
    if (show) {
        $('body').append(`
            <div id="loading-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 9999;">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: black; background: white; padding: 20px; border-radius: 5px;">
                    <div class="spinner"></div>
                </div>
            </div>
        `);
    } else {
        // Add a delay before hiding the loading screen
        setTimeout(function () {
            $('#loading-overlay').remove();
        }, 100); // Delay of 100 milliseconds
    }
}


function debounce(func, delay) {
    let debounceTimer;
    return function () {
        const context = this;
        const args = arguments;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(context, args), delay);
    };
}
function updateQuantity(itemId, newQuantity) {
    const updateUrl = `/cart/update_cart_quantity/${itemId}/`;
    const csrftoken = getCookie('csrftoken');

    toggleLoadingScreen(true); // Show loading screen

    $.ajax({
        url: updateUrl,
        type: 'POST',
        data: {
            'quantity': newQuantity,
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (response) {
            // Update the subtotal with the correct format
            $('#subtotal-' + response.item_id).text(response.subtotal.toFixed(2));
            // Update the total price
            $('#total-price').text(response.total_price.toFixed(2));
            // Update the quantity input value
            $('input[data-item-id="' + response.item_id + '"]').val(response.quantity);
            // Update the item count
            $('#item-count').text('(' + response.item_count + ')');
            toggleLoadingScreen(false); // Hide loading screen
        },
        error: function (xhr) {
            try {
                // Extract error message from response
                let errorMessage = 'An unexpected error occurred.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }

                // Show SweetAlert message
                Swal.fire({
                    icon: 'warning',
                    title: 'Quantity Error',
                    text: errorMessage,
                });
            } catch (e) {
                // Handle any additional errors
                Swal.fire({
                    icon: 'warning',
                    title: 'Quantity Error',
                    text: 'An unexpected error occurred.',
                });
            } finally {
                toggleLoadingScreen(false); // Hide loading screen even if there's an error
            }
        }
    });
}
function removeCartItem(itemId) {
    const removeUrl = `/cart/remove/${itemId}/`;
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        url: removeUrl,
        type: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (response) {
            // Show success notification
            Swal.fire({
                icon: 'success',
                title: 'Removed!',
                text: 'The item has been successfully removed from the cart.',
                timer: 2000, // Timer for 2 seconds
                timerProgressBar: true,
                willClose: () => {
                    // Refresh the page after the timer ends
                    location.reload();
                }
            });
        },
        error: function (response) {
            console.error('Error removing item from cart:', response);
            // Show error notification
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'There was an error removing the item from the cart.',
                timer: 2000, // Timer for 2 seconds
                timerProgressBar: true,
            });
        }
    });
}



function attachEventListeners() {
    $('#cart-items').on('click', '.increase-btn', function () {
        const itemId = $(this).data('item-id');
        const currentQuantity = parseInt($('input[data-item-id="' + itemId + '"]').val());
        updateQuantity(itemId, currentQuantity + 1);
    });

    $('#cart-items').on('click', '.decrease-btn', function () {
        const itemId = $(this).data('item-id');
        const currentQuantity = parseInt($('input[data-item-id="' + itemId + '"]').val());
        if (currentQuantity > 1) {
            updateQuantity(itemId, currentQuantity - 1);
        }
    });

    $('#cart-items').on('input', '.quantity-input', debounce(function () {
        const itemId = $(this).data('item-id');
        const newQuantity = parseInt($(this).val());
        if (newQuantity > 0) {
            updateQuantity(itemId, newQuantity);
        } else {
            $(this).val(1);
            updateQuantity(itemId, 1);
        }
    }, 500));

    $('#cart-items').on('click', '.remove-btn', function () {
        const itemId = $(this).data('item-id');
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
                removeCartItem(itemId);
            }
        });
    });
}


$(document).ready(function () {
    attachEventListeners();
    fetchCart();
});

async function fetchCart() {
    try {
        const [cartResponse, laptopSpecsResponse] = await Promise.all([
            fetch('/api/public-cart/'),
            fetch('/api/public-laptop-specs/')
        ]);

        const cartData = await cartResponse.json();
        const laptopSpecs = await laptopSpecsResponse.json();

        displayCart(cartData, laptopSpecs);
    } catch (error) {
        console.error('Error fetching data:', error);
        $('#cart-message').html('<p class="text-danger">Error loading cart. Please try again later.</p>');
    }
}


function displayCart(cartData, laptopSpecs) {
    let cartItemsHtml = '';
    if (cartData.cart_items.length > 0) {
        cartData.cart_items.forEach(function (item) {
            // Find the spec for the product
            const spec = laptopSpecs.find(spec => spec.product.id === item.product);
            if (!spec) {
                console.warn(`No spec found for product ${item.product}`);
                return;
            }

            // Set image URL
            const imageUrl = spec.product.images.length > 0
                ? spec.product.images[0].image
                : '/static/images/placeholder.jpg';

            // Set GPU details
            const gpuDetails = spec.gpu.map(gpu => `${gpu.gpu_brand.name} ${gpu.model}`).join(', ');

            // Ensure subtotal and total price are numbers and format them
            const subtotal = parseFloat(item.subtotal);
            const formattedSubtotal = subtotal.toFixed(2);

            // Append the cart item HTML
            cartItemsHtml += `
            <div class="cart-item col-md-4 col-sm-6" id="cart-item-${item.id}">
                <div class="card">
                    <img src="${imageUrl}" alt="${spec.product.name}" class="card-img-top" onerror="this.src='/static/images/placeholder.jpg';">
                    <div class="card-body">
                        <h5 class="card-title">${spec.product.name} ${spec.product.model} ${spec.product.year}</h5>
                        <p><strong>Specs:</strong> ${spec.cpu.cpu_brand.name} ${spec.cpu.model} | ${gpuDetails} | ${spec.storage.capacity}${spec.storage.capacity_type} ${spec.memory.capacity}GB</p>
                        <div class="quantity-control mt-3">
                            <button class="btn border decrease-btn mr-1" data-item-id="${item.id}" data-url="/orders/update_cart_quantity/${item.id}/">-</button>
                            <input type="number" class="quantity-input form-control" data-item-id="${item.id}" value="${item.quantity}" min="1">
                            <button class="btn border increase-btn mr-1" data-item-id="${item.id}" data-url="/orders/update_cart_quantity/${item.id}/">+</button>
                        </div>
                        <p class="card-text mt-3">$<span id="subtotal-${item.id}">${formattedSubtotal}</span></p>
                        <button type="button" class="btn btn-danger remove-btn" data-item-id="${item.id}"><i class="fa-solid fa-trash"></i></button>
                    </div>
                </div>
            </div>
        `;
        });
        $('#cart-items').html(cartItemsHtml);
        $('#total-price').text(parseFloat(cartData.total_price).toFixed(2));
        $('#cart-total').show();
    } else {
        $('#cart-items').html('<div class="col-12"><p>Your cart is empty.</p></div>');
        $('#cart-total').hide();
    }

    attachEventListeners();
}
document.addEventListener('DOMContentLoaded', function() {
    const checkoutButton = document.getElementById('checkout-button');
    if (checkoutButton) {
        checkoutButton.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Fetch cart items from server
            fetch('/api/cart-items/')
                .then(response => response.json())
                .then(cartItems => {
                    checkStockAvailability(cartItems);
                });
        });
    } else {
        console.error('Checkout button not found.');
    }
});

function checkStockAvailability(cartItems) {
    let outOfStockItems = [];
    let checksRemaining = cartItems.length;

    cartItems.forEach(item => {
        fetch(`/api/stock/${item.productId}/`)
            .then(response => response.json())
            .then(stockData => {
                if (item.quantity > stockData.quantity) {
                    outOfStockItems.push(item.productName, item.productModel);
                    // Mark item in red (assumes items are marked with a unique ID)
                    const itemElement = document.getElementById(`cart-item-${item.productId}`);
                    if (itemElement) {
                        itemElement.style.backgroundColor = 'red';
                        itemElement.style.color = 'white';
                    }
                } else {
                    // Ensure item is not marked red if it's in stock
                    const itemElement = document.getElementById(`cart-item-${item.productId}`);
                    if (itemElement) {
                        itemElement.style.backgroundColor = '';
                        itemElement.style.color = '';
                    }
                }

                checksRemaining--;
                if (checksRemaining === 0) {
                    if (outOfStockItems.length > 0) {
                        showOutOfStockAlert(outOfStockItems);
                    } else {
                        // Proceed to checkout if no items are out of stock
                        window.location.href = checkoutUrl;
                    }
                }
            });
    });
}

function showOutOfStockAlert(outOfStockItems) {
    Swal.fire({
        title: 'Out of Stock!',
        text: `The following items are out of stock: ${outOfStockItems.join(', ')}. Please remove them from your cart.`,
        icon: 'warning',
        confirmButtonText: 'Okay'
    });
}



$(document).ready(function () {
    fetchCart();
    attachEventListeners();
});