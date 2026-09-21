# 📈 Stock Trend Tracker

An automated pipeline that tracks a stock's price every day and emails a visual weekly trend report — no dashboard, no manual checking, just a chart in your inbox.

## What it does

**Every day** at midnight (Turkey time), this project automatically:

1. Fetches the current price of a stock (default: **AAPL**) from Yahoo Finance
2. Appends the date and price to a CSV file (`prices.csv`) that lives in this repository
3. Commits that update back to the repo, so the price history builds up over time

**Every Monday** at 08:30 (Turkey time), it automatically:

1. Reads the last 7 days of recorded prices
2. Calculates the percentage change over that period
3. Draws a line chart of the price movement
4. Emails a short summary with the chart embedded

## Why

Manually checking a stock price every day (or worse, forgetting to) is a chore. This project shows a simple pattern for turning any recurring "check something, track it over time" task into a fully hands-off pipeline — the same approach works for currency rates, crypto prices, a competitor's pricing page, or any other numeric value that changes over time.

## How it works

- **Language:** Python
- **Automation:** two [GitHub Actions](https://github.com/features/actions) scheduled workflows (cron jobs) — one daily, one weekly
- **Data source:** Yahoo Finance's public chart endpoint (no API key required)
- **Data storage:** a plain CSV file, version-controlled in the repo itself — no database needed
- **Charting:** [Matplotlib](https://matplotlib.org/)
- **Email delivery:** Gmail SMTP, with the chart embedded as an image attachment
- **No server required** — runs entirely on GitHub's free infrastructure

## Architecture

```
.github/workflows/daily.yml    → Runs every day: fetch price, append to CSV, commit
.github/workflows/weekly.yml   → Runs every Monday: read CSV, build chart, send email
track_price.py                 → Fetches the current price and appends it to prices.csv
weekly_report.py               → Reads recent prices, builds the chart, sends the email
prices.csv                     → Growing history of daily prices (date, price)
requirements.txt               → Python dependencies
```

## Setup

If you want to run your own copy of this tracker:

1. Fork or clone this repository
2. Go to **Settings → Secrets and variables → Actions** and add the following repository secrets:

   | Secret | Description |
   |---|---|
   | `MAIL_FROM` | The Gmail address the report will be sent from |
   | `MAIL_PASSWORD` | A Gmail [App Password](https://myaccount.google.com/apppasswords) (not your regular password) |
   | `MAIL_TO` | The email address that should receive the report |

3. The daily tracker needs `contents: write` permission to commit price updates — this is already set in `daily.yml`.
4. That's it — both workflows run automatically on their schedule. You can also trigger either one manually from the **Actions** tab using **Run workflow**.

## Customization

- **Track a different stock:** change the `SYMBOL` variable at the top of both `track_price.py` and `weekly_report.py` (any valid Yahoo Finance ticker works, e.g. `TSLA`, `MSFT`, `GOOGL`)
- **Change the schedules:** edit the `cron` expressions in `.github/workflows/daily.yml` and `weekly.yml` ([crontab.guru](https://crontab.guru/) is helpful for this)
- **Change the reporting window:** adjust `DAYS_TO_SHOW` in `weekly_report.py` to summarize a different number of days
- **Track multiple stocks:** duplicate the pattern — a second CSV file, a second symbol, and either extend the existing scripts to loop over a list of symbols or add a second pair of workflows

## Notes

- All credentials are stored securely as GitHub Actions secrets — nothing is hardcoded in the source code.
- Yahoo Finance's chart endpoint is unofficial and could change without notice; if the daily tracker starts failing, that's the first place to check.
- If fewer than 2 data points exist yet, the weekly report still sends but explains that there isn't enough data for a trend yet, instead of failing.
