


document.addEventListener('DOMContentLoaded', function () {
    const clearFiltersBtn = document.getElementById('clearFiltersBtn');

    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function (e) {
            e.preventDefault();

            // Get the URL to clear filters from the data attribute
            const clearUrl = this.getAttribute('data-clear-url');

            // Redirect to the clear URL
            window.location.href = clearUrl;
        });
    }
});



document.addEventListener('DOMContentLoaded', function () {
    const pdfExportBtn = document.getElementById('pdfExport');
    const confirmExportBtn = document.getElementById('confirmExport');
    const exportModal = new bootstrap.Modal(document.getElementById('exportModal'));

    pdfExportBtn.addEventListener('click', function () {
        exportModal.show();
    });

    confirmExportBtn.addEventListener('click', function () {
        const exportOption = document.querySelector('input[name="exportOption"]:checked').value;
        exportToPdf(exportOption);
        exportModal.hide();
    });
});

function exportToPdf(exportOption) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(24);
    doc.text("Product List", 80, 15);
    
    if (exportOption === 'current') {
        exportCurrentPage(doc);
    } else {
        exportAllData(doc);
    }
}

function exportCurrentPage(doc) {
    const table = document.querySelector('table');
    const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
    const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr =>
        Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim())
    );

    doc.autoTable({
        head: [headers],
        body: rows,
        startY: 20,
        styles: { fontSize: 8, cellPadding: 2, overflow: 'linebreak' },
        columnStyles: { 3: { cellWidth: 30 } }
    });

    doc.save('product-list-current-page.pdf');
}
function exportAllData(doc) {
    fetch('/api/products/all')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const contentType = response.headers.get('Content-Type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Response is not JSON');
            }
            return response.json();
        })
        .then(data => {
            const headers = ['ID', 'Product Name', 'Model', 'Color', 'Price', 'Year', 'Warranty'];

            // Group products by brand
            const brandGroups = data.reduce((acc, product) => {
                const brand = product['brand__name'] || 'Unknown Brand';
                if (!acc[brand]) {
                    acc[brand] = [];
                }
                acc[brand].push(product);
                return acc;
            }, {});

            // Function to format warranty information
            function formatWarranty(product) {
                let warranty = '';
                if (product.warranty_years > 0) {
                    warranty += `${product.warranty_years} year${product.warranty_years > 1 ? 's' : ''}`;
                }
                if (product.warranty_months > 0) {
                    if (warranty) {
                        warranty += ' ';
                    }
                    warranty += `${product.warranty_months} month${product.warranty_months > 1 ? 's' : ''}`;
                }
                return warranty || 'N/A';
            }

            // Function to format price
            function formatPrice(price) {
                const numberFormatter = new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD',
                    minimumFractionDigits: 0,
                });
                return numberFormatter.format(parseFloat(price)) || 'N/A';
            }

            // Initialize Y position for the first table
            let yPosition = 20;

            // Generate a separate table for each brand
            Object.keys(brandGroups).forEach(brand => {
                // Add brand name as a header
                doc.setFontSize(14);
                doc.text(brand, 14, yPosition);
                yPosition += 10; // Add space after the brand name

                // Create rows for the table
                const rows = brandGroups[brand].map(product => [
                    product.id,
                    product.name,
                    product.model,
                    product['color__name'] || 'N/A',
                    formatPrice(product.price),
                    product.year || 'N/A',
                    formatWarranty(product)
                ]);

                // Add the table for the current brand
                doc.autoTable({
                    head: [headers],
                    body: rows,
                    startY: yPosition,
                    styles: { fontSize: 8, cellPadding: 2, overflow: 'linebreak' },
                    columnStyles: { 3: { cellWidth: 30 } }
                });

                // Update Y position for the next brand section
                yPosition = doc.autoTable.previous.finalY + 20; // Add space after the table
            });

            // Save the PDF
            doc.save('All-products.pdf');
        })
        .catch(error => {
            // console.error('Error fetching all products:', error);
            alert('Failed to fetch all products. Please try again.');
        });
}
