let cart = []; // Array to store cart items

function addToCart(product) {
    // Check if product is already in cart
    const existingItem = cart.find(item => item.id === product.id);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    updateCartDisplay();
}

function updateCartDisplay() {
    const cartItemsElement = document.getElementById("cart-items");
    cartItemsElement.innerHTML = ""; // Clear existing cart items

    let total = 0;

    cart.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.name}</td>
            <td>
                <input type="number" value="${item.quantity}" min="1" onchange="updateCartItemQuantity(${item.id}, this.value)">
            </td>
            <td>$${item.price.toFixed(2)}</td>
            <td>$${(item.price * item.quantity).toFixed(2)}</td>
        `;
        cartItemsElement.appendChild(row);
        total += item.price * item.quantity;
    });

    document.getElementById("total-price").textContent = total.toFixed(2);
}

function updateCartItemQuantity(productId, quantity) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity = parseInt(quantity);
        updateCartDisplay();
    }
}

// Add event listener to checkout button
document.getElementById("checkout-button").addEventListener("click", () => {
    // Send cart data to backend for processing
    fetch("/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cart)
    })
    .then(response => response.json())
    .then(data => {
        // Redirect to Stripe checkout or handle payment response
    })
    .catch(error => console.error("Error during checkout:", error));
});
