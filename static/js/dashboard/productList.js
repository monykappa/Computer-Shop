


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

    doc.setFontSize(16);
    doc.text("Product List", 14, 15);

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
    // We need to make an AJAX call to get all the data
    fetch('/api/products/all')  // Ensure this endpoint is correct and returns valid JSON
        .then(response => {
            // Check if the response is OK and if the content type is JSON
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
            const headers = ['ID', 'Product Name', 'Model', 'Brand', 'Color', 'Price', 'Year', 'Warranty'];
            const rows = data.map(product => {
                // Format warranty information
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

                // Format price with dollar sign and thousands separators
                const price = parseFloat(product.price);
                let formattedPrice = 'N/A';
                if (!isNaN(price)) {
                    const numberFormatter = new Intl.NumberFormat('en-US', {
                        style: 'currency',
                        currency: 'USD',
                        minimumFractionDigits: 0, // Do not show decimal places
                    });
                    formattedPrice = numberFormatter.format(price);
                }

                // Return formatted row
                return [
                    product.id,
                    product.name,
                    product.model,
                    product['brand__name'] || 'N/A',
                    product['color__name'] || 'N/A',
                    formattedPrice,
                    product.year || 'N/A',
                    warranty || 'N/A'  // Show 'N/A' if warranty is empty
                ];
            });

            doc.autoTable({
                head: [headers],
                body: rows,
                startY: 20,
                styles: { fontSize: 8, cellPadding: 2, overflow: 'linebreak' },
                columnStyles: { 3: { cellWidth: 30 } }
            });

            doc.save('product-list-all-data.pdf');
        })
        .catch(error => {
            console.error('Error fetching all products:', error);
            alert('Failed to fetch all products. Please try again.');
        });
}



function confirmDelete(url) {
    Swal.fire({
        title: 'Are you sure?',
        text: 'You will not be able to recover this product!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            // Perform AJAX request to delete the product
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json',
                },
            }).then(response => {
                if (response.ok) {
                    Swal.fire(
                        'Deleted!',
                        'The product has been deleted.',
                        'success'
                    ).then(() => {
                        // Remove the row from the table
                        const row = document.querySelector(`button[onclick="confirmDelete('${url}')"]`).closest('tr');
                        row.remove();
                    });
                } else {
                    Swal.fire(
                        'Error!',
                        'There was an issue deleting the product.',
                        'error'
                    );
                }
            }).catch(error => {
                Swal.fire(
                    'Error!',
                    'There was an issue deleting the product.',
                    'error'
                );
            });
        }
    });
}
