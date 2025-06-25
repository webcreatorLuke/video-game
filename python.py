from flask import Flask, request, jsonify, redirect
import stripe
import os

app = Flask(__name__)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY") # Store your secret key securely in environment variables

@app.route("/checkout", methods=["POST"])
def create_checkout_session():
    cart = request.json  # Get cart data from the frontend

    line_items = []
    for item in cart:
        line_items.append({
            "price_data": {
                "currency": "usd", # Or your preferred currency
                "product_data": {
                    "name": item["name"]
                },
                "unit_amount": int(item["price"] * 100) # Convert price to cents
            },
            "quantity": item["quantity"]
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url="YOUR_SUCCESS_URL", # Replace with your success URL
            cancel_url="YOUR_CANCEL_URL" # Replace with your cancel URL
        )
        return jsonify({"id": checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

# You'll also need to set up routes for success and cancel URLs and implement Stripe webhooks
