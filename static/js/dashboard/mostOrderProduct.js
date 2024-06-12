var ctx = document.getElementById('orderProductChart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: {{ labels|safe }},
        datasets: [{
            label: 'Total Quantity Ordered',
            data: {{ quantities|safe }},
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});