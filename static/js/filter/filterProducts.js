// brandFilter.js

function createBrandFilter(brands, laptopSpecs) {
    // Create a container for the filter button
    const filterButtonContainer = document.createElement('div');
    filterButtonContainer.className = 'filter-button-container mb-3';
    

    // Create the modal
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'filterModal';
    modal.setAttribute('tabindex', '-1');
    modal.setAttribute('aria-labelledby', 'filterModalLabel');
    modal.setAttribute('aria-hidden', 'true');
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="filterModalLabel">Filters</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-12 mb-3">
                            <label class="form-label">Brand</label>
                            <div id="brand-checkboxes" class="d-flex flex-wrap">
                                <div class="form-check form-switch me-3">
                                    <input class="form-check-input" type="checkbox" role="switch" value="all" id="brand-all" checked>
                                    <label class="form-check-label" for="brand-all">
                                        All Brands
                                    </label>
                                </div>
                                ${brands.map(brand => `
                                    <div class="form-check form-switch me-3">
                                        <input class="form-check-input brand-checkbox ml-4 " type="checkbox" role="switch" value="${brand.id}" id="brand-${brand.id}">
                                        <label class="form-check-label d-flex align-items-center" for="brand-${brand.id}">
                                            <img src="${brand.logo}" width="40" class="ml-5" alt="${brand.name} logo"> ${brand.name}
                                        </label>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div class="col-12 col-md-6 mb-3">
                            <label for="price-sort" class="form-label">Price</label>
                            <select id="price-sort" class="form-select form-control">
                                <option value="">No sorting</option>
                                <option value="low-to-high">Low to High</option>
                                <option value="high-to-low">High to Low</option>
                            </select>
                        </div>
                        <div class="col-12 col-md-6 mb-3">
                            <label for="year-select" class="form-label">Year</label>
                            <select id="year-select" class="form-select form-control">
                                <option value="all">All Years</option>
                                ${getUniqueYears(laptopSpecs).map(year => `
                                    <option value="${year}">${year}</option>
                                `).join('')}
                            </select>
                        </div>
                        <div class="col-12 col-md-6 mb-3">
                            <label for="cpu-select" class="form-label">CPU</label>
                            <select id="cpu-select" class="form-select form-control">
                                <option value="all">All CPUs</option>
                                ${getUniqueCPUs(laptopSpecs).map(cpu => `
                                    <option value="${cpu}">${cpu}</option>
                                `).join('')}
                            </select>
                        </div>
                        <div class="col-12 col-md-6 mb-3">
                            <label for="gpu-select" class="form-label">GPU</label>
                            <select id="gpu-select" class="form-select form-control">
                                <option value="all">All GPUs</option>
                                ${getUniqueGPUs(laptopSpecs).map(gpu => `
                                    <option value="${gpu}">${gpu}</option>
                                `).join('')}
                            </select>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" id="apply-filter">Apply Filters</button>
                </div>
            </div>
        </div>
    `;

    // Insert the filter button and modal into the DOM
    const productsContainer = document.getElementById('products-container');
    productsContainer.parentNode.insertBefore(filterButtonContainer, productsContainer);
    document.body.appendChild(modal);

    // Add event listeners
    document.getElementById('apply-filter').addEventListener('click', () => {
        filterProducts(brands, laptopSpecs);
        bootstrap.Modal.getInstance(document.getElementById('filterModal')).hide();
    });
    document.getElementById('brand-all').addEventListener('change', handleAllBrandsCheckbox);
    document.querySelectorAll('.brand-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleBrandCheckboxChange);
    });

    function getUniqueCPUs(laptopSpecs) {
        const cpus = new Set(laptopSpecs.map(spec => `${spec.cpu.cpu_brand.name} ${spec.cpu.model}`));
        return Array.from(cpus).sort();
    }

    function getUniqueGPUs(laptopSpecs) {
        const gpus = new Set(laptopSpecs.flatMap(spec =>
            spec.gpu.map(gpu => `${gpu.gpu_brand.name} ${gpu.model}`)
        ));
        return Array.from(gpus).sort();
    }

    function handleAllBrandsCheckbox() {
        const isChecked = document.getElementById('brand-all').checked;
        const checkboxes = document.querySelectorAll('.brand-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
            checkbox.disabled = isChecked;
        });
    }

    function handleBrandCheckboxChange() {
        const brandCheckboxes = document.querySelectorAll('.brand-checkbox');
        const allChecked = Array.from(brandCheckboxes).every(checkbox => !checkbox.checked);
        document.getElementById('brand-all').checked = allChecked;
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
    const cpuSelect = document.getElementById('cpu-select').value;
    const gpuSelect = document.getElementById('gpu-select').value;

    const selectedBrands = Array.from(brandCheckboxes)
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);
    const showAllBrands = document.getElementById('brand-all').checked || selectedBrands.length === 0;

    let filteredSpecs = laptopSpecs.filter(spec => {
        const brandMatch = showAllBrands || selectedBrands.includes(spec.product.brand.id.toString());
        const yearMatch = yearSelect === 'all' || spec.product.year.toString() === yearSelect;
        const cpuMatch = cpuSelect === 'all' || `${spec.cpu.cpu_brand.name} ${spec.cpu.model}` === cpuSelect;
        const gpuMatch = gpuSelect === 'all' || spec.gpu.some(gpu => `${gpu.gpu_brand.name} ${gpu.model}` === gpuSelect);
        return brandMatch && yearMatch && cpuMatch && gpuMatch;
    });

    // Sort by price
    if (priceSort === 'low-to-high') {
        filteredSpecs.sort((a, b) => a.product.price - b.product.price);
    } else if (priceSort === 'high-to-low') {
        filteredSpecs.sort((a, b) => b.product.price - a.product.price);
    }

    displayFilteredProducts(filteredSpecs, brands);
}

function displayFilteredProducts(filteredSpecs, brands) {
    const productsContainer = document.getElementById('products-container');
    productsContainer.innerHTML = '';

    const brandMap = new Map(brands.map(brand => [brand.id, brand]));
    const brandSections = {};

    if (filteredSpecs.length === 0) {
        productsContainer.innerHTML = '<p class="text-center">No products match the selected filters.</p>';
        return;
    }

    filteredSpecs.forEach((spec, index) => {
        const brand = brandMap.get(spec.product.brand.id);

        if (!brandSections[brand.id]) {
            let brandSection = document.createElement('div');
            brandSection.id = brand.slug;
            brandSection.className = 'brand-section';
            brandSection.innerHTML = `
                <div class="text-center mt-4 mb-3 bg-light p-3 border rounded">
                    <img src="${brand.logo}" width="120" class="img-fluid" alt="${brand.name} logo" />
                </div>
                <div class="row g-3" id="${brand.slug}-products" data-brand-id="${brand.id}"></div>
            `;
            productsContainer.appendChild(brandSection);
            brandSections[brand.id] = document.getElementById(`${brand.slug}-products`);
        }

        let productCard = createProductCard(spec);
        brandSections[brand.id].appendChild(productCard);

        setTimeout(() => {
            productCard.querySelector('.product-card').classList.add('show');
        }, 50 * index);
    });
}

function createProductCard(spec) {
    let productImage = spec.product.images.length > 0 ? spec.product.images[0].image : '/static/placeholder_image.jpg';
    let gpuDetails = spec.gpu.map(gpu => `${gpu.gpu_brand.name} ${gpu.model}`).join(', ');
    let productCard = document.createElement('div');
    productCard.className = 'col-6 col-md-4 col-lg-3';
    productCard.innerHTML = `
        <div class="product-card card h-100 border-0 shadow-sm">
            <div class="warranty-badge position-absolute top-0 end-0 bg-primary text-white p-1 rounded-start small">
                ${spec.product.warranty_years > 0
                    ? `${spec.product.warranty_years} ${spec.product.warranty_years === 1 ? 'year' : 'years'} warranty`
                    : spec.product.warranty_months > 0
                        ? `${spec.product.warranty_months} ${spec.product.warranty_months === 1 ? 'month' : 'months'} warranty`
                        : 'No warranty'
                }
            </div>
            <div class="product-image-container">
                <img class="product-image card-img-top" src="${productImage}" alt="${spec.product.name}">
            </div>
            <div class="product-info card-body d-flex flex-column">
                <h5 class="product-title card-title mb-2">${spec.product.name} ${spec.product.model} ${spec.product.year}</h5>
                <p class="product-specs card-text small mb-2">${spec.cpu.cpu_brand.name} ${spec.cpu.model} | ${gpuDetails} | ${spec.storage.capacity}${spec.storage.capacity_type} ${spec.memory.capacity}GB | ${spec.product.color.name}</p>
                <div class="product-footer mt-auto d-flex justify-content-between align-items-center">
                    <h4 class="product-price card-title mb-0">$${formatPrice(spec.product.price)}</h4>
                    <a href="/products/${spec.slug}/" class="btn btn-primary btn-sm see-more-btn"><i class="fa-solid fa-eye"></i> Details</a>
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