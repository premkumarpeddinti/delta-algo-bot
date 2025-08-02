import time, json, hmac, hashlib, requests
from config import API_KEY, API_SECRET, BASE_URL, PRODUCT_SYMBOL, POSITION_SIZE

def sign_request(endpoint, body):
    timestamp = str(int(time.time()))
    message = timestamp + endpoint + json.dumps(body)
    signature = hmac.new(
        API_SECRET.encode(), message.encode(), hashlib.sha256
    ).hexdigest()
    return timestamp, signature

def place_market_order(side):
    endpoint = "/v2/orders"
    url = BASE_URL + endpoint
    body = {
        "product_symbol": PRODUCT_SYMBOL,
        "size": POSITION_SIZE,
        "side": side,
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
    print("Order Response:", r.status_code, r.json())
    return r.json()
