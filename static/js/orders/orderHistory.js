function showTable(status) {
    document.getElementById('pending').style.display = 'none';
    document.getElementById('completed').style.display = 'none';
    document.getElementById('cancelled').style.display = 'none';

    document.getElementById(status).style.display = 'block';
}