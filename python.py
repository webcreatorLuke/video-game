from flask import Flask, request, jsonify, redirect
import stripe
import os

app = Flask(__name__)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@app.route("/checkout", methods=["POST"])
def create_checkout_session():
    cart = request.json

    line_items = []
    for item in cart:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item["name"]
                },
                "unit_amount": int(item["price"] * 100)
            },
            "quantity": item["quantity"]
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url="YOUR_SUCCESS_URL",
            cancel_url="YOUR_CANCEL_URL"
        )
        return jsonify({"id": checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

# Handle Stripe webhooks
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", None)
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get("STRIPE_WEBHOOK_SECRET") # Get webhook secret from environment variables
        )
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Fulfill the purchase...
        fulfill_order(session)

    # Return a 200 response to acknowledge receipt of the event
    return "Success", 200

def fulfill_order(session):
    # TODO: Fulfill the order, e.g. update your database
    print("Fulfilling order:", session)

# You'll also need to define routes for your success and cancel URLs
