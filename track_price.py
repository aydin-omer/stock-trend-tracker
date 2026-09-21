import requests
import datetime
import csv
import os

SYMBOL = "AAPL"
CSV_PATH = "prices.csv"


def get_current_price(symbol=SYMBOL):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"range": "1d", "interval": "1d"}

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    result = data["chart"]["result"][0]
    price = result["meta"]["regularMarketPrice"]
    return price


def append_price(price):
    today = datetime.date.today().isoformat()

    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "price"])
        writer.writerow([today, price])


def main():
    price = get_current_price()
    append_price(price)
    print(f"Recorded {SYMBOL} price: {price} on {datetime.date.today().isoformat()}")


if __name__ == "__main__":
    main()
