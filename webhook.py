from flask import Flask, request
from trade import place_market_order

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    side = data.get("side")  # "buy" or "sell"
    if side in ["buy", "sell"]:
        place_market_order(side)
        return {"status": "Order placed"}, 200
    return {"error": "Invalid payload"}, 400

if __name__ == "__main__":
    app.run(port=8000)
