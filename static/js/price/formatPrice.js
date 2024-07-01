function formatPrice(price) {
    // Convert the price to a number with two decimal places
    let formattedPrice = parseFloat(price).toFixed(2);
    // Remove trailing zeros and the decimal point if there are no non-zero digits after it
    formattedPrice = parseFloat(formattedPrice).toString();
    return formattedPrice;
}
