$(document).ready(function(){
    $(".clickable-row").click(function(){
        window.location = $(this).data("href");
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.clickable-row');
    rows.forEach(row => {
        row.addEventListener('click', function() {
            window.location.href = this.dataset.href;
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const clickableCells = document.querySelectorAll('.clickable-cell');
    const cancelForms = document.querySelectorAll('.cancel-order-form');
    const completeForms = document.querySelectorAll('.complete-order-form');

    clickableCells.forEach(cell => {
        cell.addEventListener('click', function() {
            window.location.href = this.dataset.href;
        });
    });

    cancelForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            Swal.fire({
                title: 'Are you sure?',
                text: "You are about to cancel this order. This action cannot be undone!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, cancel it!',
                cancelButtonText: 'No, keep it'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    });

    completeForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            Swal.fire({
                title: 'Mark as Completed?',
                text: "Are you sure you want to mark this order as completed?",
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#28a745',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, complete it!',
                cancelButtonText: 'No, not yet'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    });
});

function printTable() {
    // Open a new window
    var printWindow = window.open('', '', 'height=600,width=800');
    
    // Get the HTML content of the table
    var tableHtml = document.querySelector('.table-responsive').innerHTML;
    
    // Create a temporary DOM element to manipulate the table HTML
    var tempDiv = document.createElement('div');
    tempDiv.innerHTML = tableHtml;
    
    // Remove the "Action" column
    var actionColumnHeader = tempDiv.querySelector('th.action-column');
    var actionColumnCells = tempDiv.querySelectorAll('td.action-column');
    
    if (actionColumnHeader) {
        actionColumnHeader.remove();
    }
    actionColumnCells.forEach(function(cell) {
        cell.remove();
    });
    
    // Write the modified HTML content into the new window
    printWindow.document.write('<html><head><title>Print Table</title>');
    printWindow.document.write('<style>');
    printWindow.document.write('body { font-family: Arial, sans-serif; }');
    printWindow.document.write('.table { width: 100%; border-collapse: collapse; }');
    printWindow.document.write('.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }');
    printWindow.document.write('.table th { background-color: #f2f2f2; }');
    printWindow.document.write('</style>');
    printWindow.document.write('</head><body>');
    printWindow.document.write('<div style="text-align: center;">');
    printWindow.document.write(tempDiv.innerHTML);
    printWindow.document.write('</div>');
    printWindow.document.write('</body></html>');
    
    // Close the document to finish writing
    printWindow.document.close();
    
    // Print the document
    printWindow.print();
}


function exportTableToExcel() {
if (typeof XLSX === 'undefined') {
console.error('XLSX library is not loaded.');
return;
}

// Get the HTML content of the table
var tableHtml = document.querySelector('.table-responsive').innerHTML;

// Create a temporary DOM element to manipulate the table HTML
var tempDiv = document.createElement('div');
tempDiv.innerHTML = tableHtml;

// Remove the "Action" column
var actionColumnHeader = tempDiv.querySelector('th.action-column');
var actionColumnCells = tempDiv.querySelectorAll('td.action-column');

if (actionColumnHeader) {
actionColumnHeader.remove();
}
actionColumnCells.forEach(function(cell) {
cell.remove();
});

// Create a new workbook and worksheet
var wb = XLSX.utils.book_new();
var ws = XLSX.utils.table_to_sheet(tempDiv.querySelector('table'));

// Define border styles and alignment
const borderStyle = {
top: { style: 'thin' },
left: { style: 'thin' },
bottom: { style: 'thin' },
right: { style: 'thin' }
};
const centerAlignment = { horizontal: 'center', vertical: 'center' };

// Add borders and center-align text for each cell
for (const cellAddress in ws) {
if (ws[cellAddress].v) {
    ws[cellAddress].s = {
        border: borderStyle,
        alignment: centerAlignment
    };
}
}

// Adjust column widths for specific columns
ws['!cols'] = [
{ width: 5 }, // Width for Order ID
{ width: 15 }, // Width for Ordered Date
{ width: 10 }, // Width for Total Price
{ width: 10 }, // Width for Customer
{ width: 80 }, // Width for Address
{ width: 10 }, // Width for Status
];

// Add the worksheet to the workbook
XLSX.utils.book_append_sheet(wb, ws, 'Orders');

// Save the workbook
XLSX.writeFile(wb, 'orders.xlsx');
}


function exportTableToPDF() {
// Clone the table so we don't modify the original
var originalTable = document.querySelector('.table');
var table = originalTable.cloneNode(true);

// Remove action column if it exists
var actionColumnIndex = -1;
table.querySelectorAll('th').forEach((th, index) => {
if (th.textContent.trim() === 'Action') {
    actionColumnIndex = index;
}
});

if (actionColumnIndex !== -1) {
table.querySelectorAll('tr').forEach(row => {
    if (row.cells[actionColumnIndex]) {
        row.removeChild(row.cells[actionColumnIndex]);
    }
});
}

// Ensure status badges are visible and styled correctly
table.querySelectorAll('.status-badge').forEach(badge => {
badge.style.display = 'inline-block';
badge.style.padding = '2px 5px';
badge.style.borderRadius = '3px';
badge.style.color = '#ffffff';
badge.style.fontWeight = 'bold';
});

// Create a new div to hold our table
var container = document.createElement('div');
container.appendChild(table);

// Define PDF options
var opt = {
margin: 10,
filename: 'orders.pdf',
image: { type: 'jpeg', quality: 0.98 },
html2canvas: { scale: 2, useCORS: true },
jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' }
};

// Generate PDF
html2pdf().from(container).set(opt).save();
}
