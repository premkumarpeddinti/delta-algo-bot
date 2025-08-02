import time, hmac, hashlib, requests, json
from config import API_KEY, API_SECRET, BASE_URL, PRODUCT_SYMBOL, POSITION_SIZE, TAKE_PROFIT, STOP_LOSS

def sign_request(endpoint, body=""):
    timestamp = str(int(time.time()))
    message = timestamp + endpoint + (json.dumps(body) if body else "")
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return timestamp, signature

def get_positions():
    endpoint = "/v2/positions"
    url = BASE_URL + endpoint
    timestamp, signature = sign_request(endpoint)
    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "User-Agent": "trading-bot"
    }
    r = requests.get(url, headers=headers)
    return r.json()

def close_position(position_id, side):
    endpoint = "/v2/orders"
    url = BASE_URL + endpoint
    opposite = "sell" if side == "buy" else "buy"
    body = {
        "product_symbol": PRODUCT_SYMBOL,
        "size": POSITION_SIZE,
        "side": opposite,
        "order_type": "market_order"
    }
    timestamp, signature = sign_request(endpoint, body)
    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "User-Agent": "trading-bot",
        "Content-Type": "application/json"
    }
    r = requests.post(url, headers=headers, json=body)
    print("Close Response:", r.status_code, r.json())

def monitor_and_exit():
    pos = get_positions()
    for p in pos.get("result", []):
        entry_price = float(p["entry_price"])
        mark_price = float(p["mark_price"])
        side = p["side"]
        pnl = mark_price - entry_price if side == "buy" else entry_price - mark_price
        pnl *= 100  # assuming 1x leverage
        if pnl >= TAKE_PROFIT or pnl <= -STOP_LOSS:
            close_position(p["id"], side)
