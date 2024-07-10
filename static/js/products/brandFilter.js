// brandFilter.js

function createBrandFilter(brands, laptopSpecs) {
    const filterContainer = document.createElement('div');
    filterContainer.className = 'filter-container mb-4 container';
    filterContainer.innerHTML = `
        <div class="d-flex flex-wrap align-items-center">
            <div class="form-group mr-3 mb-0">
                <label class="mr-2">Brand:</label>
                <div id="brand-checkboxes" class="d-flex flex-wrap">
                    <div class="form-check mr-2 mb-1">
                        <input class="form-check-input" type="checkbox" value="all" id="brand-all" checked>
                        <label class="form-check-label d-flex align-items-center" for="brand-all">
                            All Brands
                        </label>
                    </div>
                    ${brands.map(brand => `
                        <div class="form-check mr-2 mb-1">
                            <input class="form-check-input brand-checkbox" type="checkbox" value="${brand.id}" id="brand-${brand.id}">
                            <label class="form-check-label d-flex align-items-center" for="brand-${brand.id}">
                                <img src="${brand.logo}" width="30" class="mr-1" alt="${brand.name} logo"> ${brand.name}
                            </label>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="form-group mr-3 mb-0">
                <label for="price-sort" class="mr-2">Price:</label>
                <select id="price-sort" class="form-control form-control-sm">
                    <option value="">No sorting</option>
                    <option value="low-to-high">Low to High</option>
                    <option value="high-to-low">High to Low</option>
                </select>
            </div>
            <div class="form-group mr-3 mb-0">
                <label for="year-select" class="mr-2">Year:</label>
                <select id="year-select" class="form-control form-control-sm">
                    <option value="all">All Years</option>
                    ${getUniqueYears(laptopSpecs).map(year => `
                        <option value="${year}">${year}</option>
                    `).join('')}
                </select>
            </div>
            <div class="form-check mr-3 mb-0">
                <input class="form-check-input" type="checkbox" id="newest-products">
                <label class="form-check-label" for="newest-products">
                    Show Newest Products First
                </label>
            </div>
            <button id="apply-filter" class="btn btn-primary btn-sm" style="width: auto;">Apply Filters</button>
        </div>
    `;

    const productsContainer = document.getElementById('products-container');
    productsContainer.parentNode.insertBefore(filterContainer, productsContainer);          

    // Add event listener for the filter button
    document.getElementById('apply-filter').addEventListener('click', () => filterProducts(brands, laptopSpecs));

    // Add event listener for the "All Brands" checkbox
    document.getElementById('brand-all').addEventListener('change', handleAllBrandsCheckbox);

    // Add event listeners for the brand checkboxes
    document.querySelectorAll('.brand-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleBrandCheckboxChange);
    });

    function handleAllBrandsCheckbox() {
        const isChecked = document.getElementById('brand-all').checked;
        const checkboxes = document.querySelectorAll('.brand-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        if (isChecked) {
            checkboxes.forEach(checkbox => {
                checkbox.disabled = true;
            });
        } else {
            checkboxes.forEach(checkbox => {
                checkbox.disabled = false;
            });
        }
    }

    function handleBrandCheckboxChange() {
        const brandCheckboxes = document.querySelectorAll('.brand-checkbox');
        const allChecked = Array.from(brandCheckboxes).every(checkbox => !checkbox.checked);
        if (!allChecked) {
            document.getElementById('brand-all').checked = false;
            document.getElementById('brand-all').disabled = false;
        } else {
            document.getElementById('brand-all').checked = true;
        }
    }
}

function getUniqueYears(laptopSpecs) {
    const years = new Set(laptopSpecs.map(spec => spec.product.year));
    return Array.from(years).sort((a, b) => b - a);
}

function filterProducts(brands, laptopSpecs) {
    const brandCheckboxes = document.querySelectorAll('.brand-checkbox');
    const priceSort = document.getElementById('price-sort').value;
    const yearSelect = document.getElementById('year-select').value;
    const newestFirst = document.getElementById('newest-products').checked;

    const selectedBrands = Array.from(brandCheckboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);
    const showAllBrands = document.getElementById('brand-all').checked || selectedBrands.length === 0;

    let filteredSpecs = laptopSpecs.filter(spec => {
        const brandMatch = showAllBrands || selectedBrands.includes(spec.product.brand.id.toString());
        const yearMatch = yearSelect === 'all' || spec.product.year.toString() === yearSelect;
        return brandMatch && yearMatch;
    });

    // Sort by price
    if (priceSort === 'low-to-high') {
        filteredSpecs.sort((a, b) => a.product.price - b.product.price);
    } else if (priceSort === 'high-to-low') {
        filteredSpecs.sort((a, b) => b.product.price - a.product.price);
    }

    // Sort by newest
    if (newestFirst) {
        filteredSpecs.sort((a, b) => new Date(b.product.created_at) - new Date(a.product.created_at));
    }

    displayFilteredProducts(filteredSpecs, brands);
}

function displayFilteredProducts(filteredSpecs, brands) {
    const productsContainer = document.getElementById('products-container');
    productsContainer.innerHTML = '';

    const brandMap = new Map();
    brands.forEach(brand => {
        brandMap.set(brand.id, brand);
    });

    const brandSections = {};

    if (filteredSpecs.length === 0) {
        productsContainer.innerHTML = '<p>No products match the selected filters.</p>';
        return;
    }

    filteredSpecs.forEach((spec, index) => {
        const brand = brandMap.get(spec.product.brand.id);

        if (!brandSections[brand.id]) {
            let brandSection = document.createElement('div');
            brandSection.id = brand.slug;
            brandSection.className = 'brand-section'; // Add a class for styling if needed
            brandSection.innerHTML = `
                <div class="text-center mt-5 mb-3 bg-light p-3 border rounded">
                    <img src="${brand.logo}" width="120" class="img-fluid" alt="${brand.name} logo" />
                </div>
                <div class="row" id="${brand.slug}-products" data-brand-id="${brand.id}"></div>
            `;
            productsContainer.appendChild(brandSection);
            brandSections[brand.id] = document.getElementById(`${brand.slug}-products`);
        }

        let productCard = createProductCard(spec);
        brandSections[brand.id].appendChild(productCard);

        // Apply transition with a delay based on the index
        setTimeout(() => {
            productCard.querySelector('.product-card').classList.add('show');
        }, 50 * index);
    });
}

function createProductCard(spec) {
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
                    <a href="/products/${spec.slug}/" class="btn btn-primary see-more-btn"><i class="fa-solid fa-eye"></i></a>
                </div>
            </div>
        </div>
    `;
    return productCard;
}

function formatPrice(price) {
    return price.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

// Export the createBrandFilter function so it can be used in other files
window.createBrandFilter = createBrandFilter;
