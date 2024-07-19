async function fetchData() {
    const loadingAnimation = document.getElementById('loading-animation');
    const productsContainer = document.getElementById('products-container');

    if (!productsContainer) {
        console.error('Products container not found');
        return;
    }

    loadingAnimation.style.display = 'block';
    productsContainer.style.display = 'none';

    try {
        let brandsResponse = await fetch('/api/public-brands/');
        let laptopSpecsResponse = await fetch('/api/public-laptop-specs/');

        if (!brandsResponse.ok || !laptopSpecsResponse.ok) {
            throw new Error('Network response was not ok');
        }

        let brands = await brandsResponse.json();
        let laptopSpecs = await laptopSpecsResponse.json();

        // Create brand filter if the function exists
        if (typeof createBrandFilter === 'function') {
            createBrandFilter(brands, laptopSpecs);
        }

        productsContainer.innerHTML = '';

        brands.forEach(brand => {
            let brandSection = document.createElement('div');
            brandSection.id = brand.slug;
            brandSection.innerHTML = `
                    <div class="text-center mt-5 mb-3 bg-light p-3 border rounded brand-ctn">
                        <img src="${brand.logo}" width="120" class="img-fluid" alt="${brand.name} logo" />
                    </div>
                    <div class="row" id="${brand.slug}-products" data-brand-id="${brand.id}"></div>
                `;
            productsContainer.appendChild(brandSection);

            let brandProducts = laptopSpecs.filter(spec => spec.product.brand.id === brand.id);

            let brandProductsContainer = document.getElementById(`${brand.slug}-products`);
            if (brandProducts.length === 0) {
                console.warn(`No products found for brand ${brand.name}`);
                brandProductsContainer.innerHTML = '<p>No products available for this brand.</p>';
            } else {
                brandProducts.forEach((spec, index) => {
                    let productImage = spec.product.images.length > 0 ? spec.product.images[0].image : '/static/placeholder_image.jpg';
                    let gpuDetails = spec.gpu.map(gpu => `${gpu.gpu_brand.name} ${gpu.model}`).join(', ');
                    let productCard = document.createElement('div');
                    productCard.className = 'col-6 col-md-4 col-lg-3 mb-4';
                    productCard.innerHTML = `
                            <div class="product-card">
                                <div class="warranty-badge">
                                    ${spec.product.warranty_years > 0
                            ? `${spec.product.warranty_years} ${spec.product.warranty_years === 1 ? 'year' : 'years'} warranty`
                            : spec.product.warranty_months > 0
                                ? `${spec.product.warranty_months} ${spec.product.warranty_months === 1 ? 'month' : 'months'} warranty`
                                : 'No warranty'
                        }
                                </div>
                                <div class="product-image-container">
                                    <img class="product-image" src="${productImage}" alt="${spec.product.name}">
                                </div>
                                <div class="product-info">
                                    <h4 class="product-title">${spec.product.name} ${spec.product.model} ${spec.product.year}</h4>
                                    <p class="product-specs">${spec.cpu.cpu_brand.name} ${spec.cpu.model} | ${gpuDetails} | ${spec.storage.capacity}${spec.storage.capacity_type} ${spec.memory.capacity}GB | ${spec.product.color.name}</p>
                                    <div class="product-footer">
                                        <h3 class="product-price">$${formatPrice(spec.product.price)}</h3>
                                        <a href="/products/${spec.slug}/" class="btn see-more-btn" style="background-color: var(--fourth-color);"><i class="fa-solid fa-eye text-light"></i></a>
                                    </div>
                                </div>
                            </div>
                        `;
                    brandProductsContainer.appendChild(productCard);

                    // Apply transition with a delay based on the index
                    setTimeout(() => {
                        productCard.querySelector('.product-card').classList.add('show');
                    }, 50 * index);
                });
            }
        });

        loadingAnimation.style.display = 'none';
        productsContainer.style.display = 'block';
    } catch (error) {
        console.error('Error fetching data:', error);
        loadingAnimation.style.display = 'none';
        productsContainer.innerHTML = `
                <p class="text-danger">Error loading products: ${error.message}</p>
                <p>Please check the console for more details and try again later.</p>
            `;
        productsContainer.style.display = 'block';
    }
}

function formatPrice(price) {
    // Convert to number if it's a string
    const numPrice = typeof price === 'string' ? parseFloat(price) : price;

    // Check if it's a valid number
    if (isNaN(numPrice)) {
        console.error('Invalid price:', price);
        return 'N/A';
    }

    // Format the price
    return numPrice.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

document.addEventListener('DOMContentLoaded', fetchData);