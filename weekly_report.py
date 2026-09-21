import csv
import os
import smtplib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SYMBOL = "AAPL"
CSV_PATH = "prices.csv"
CHART_PATH = "chart.png"
DAYS_TO_SHOW = 7


def read_recent_prices(limit=DAYS_TO_SHOW):
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    return rows[-limit:]


def make_chart(rows):
    dates = [r["date"] for r in rows]
    prices = [float(r["price"]) for r in rows]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, prices, marker="o")
    plt.title(f"{SYMBOL} - Last {len(rows)} days")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()


def build_summary(rows):
    if len(rows) < 2:
        return "Not enough data yet to calculate a trend. Check back next week!"

    first_price = float(rows[0]["price"])
    last_price = float(rows[-1]["price"])
    change = last_price - first_price
    change_pct = (change / first_price) * 100

    direction = "up" if change >= 0 else "down"
    return (
        f"{SYMBOL} went {direction} {abs(change_pct):.2f}% this period.\n"
        f"From ${first_price:.2f} ({rows[0]['date']}) to ${last_price:.2f} ({rows[-1]['date']})."
    )


def send_email_with_chart(subject, body_text, chart_path):
    sender = os.environ["MAIL_FROM"]
    password = os.environ["MAIL_PASSWORD"]
    receiver = os.environ["MAIL_TO"]

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    with open(chart_path, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<chart>")
        img.add_header("Content-Disposition", "attachment", filename="chart.png")
        msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def main():
    rows = read_recent_prices()

    if not rows:
        send_email_with_chart(
            f"{SYMBOL} Weekly Trend Report",
            "No price data collected yet. The daily tracker may not have run yet.",
            None,
        )
        return

    summary = build_summary(rows)
    make_chart(rows)
    send_email_with_chart(f"{SYMBOL} Weekly Trend Report", summary, CHART_PATH)


if __name__ == "__main__":
    main()
