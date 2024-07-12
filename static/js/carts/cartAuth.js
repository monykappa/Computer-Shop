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
        },
        error: function (response) {
            console.error('Error updating cart:', response);
        }
    });
}

function removeCartItem(itemId) {
    const removeUrl = `/cart/remove/${itemId}/`;
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        url: removeUrl,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (response) {
            // Refresh the page after successfully removing the item
            location.reload();
        },
        error: function (response) {
            console.error('Error removing item from cart:', response);
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
            const spec = laptopSpecs.find(spec => spec.product.id === item.product);
            if (!spec) {
                console.warn(`No spec found for product ${item.product}`);
                return;
            }

            const imageUrl = spec.product.images.length > 0
                ? spec.product.images[0].image
                : '/static/images/placeholder.jpg';

            const gpuDetails = spec.gpu.map(gpu => `${gpu.gpu_brand.name} ${gpu.model}`).join(', ');

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
                        <p class="card-text mt-3">$<span id="subtotal-${item.id}">${item.subtotal}</span></p>
                        <button type="button" class="btn btn-danger remove-btn" data-item-id="${item.id}"><i class="fa-solid fa-trash"></i></button>
                    </div>
                </div>
            </div>
        `;
        
        });
        $('#cart-items').html(cartItemsHtml);
        $('#total-price').text(cartData.total_price);
        $('#cart-total').show();
    } else {
        $('#cart-items').html('<div class="col-12"><p>Your cart is empty.</p></div>');
        $('#cart-total').hide();
    }

    attachEventListeners();
}

$(document).ready(function () {
    fetchCart();
    attachEventListeners();
});