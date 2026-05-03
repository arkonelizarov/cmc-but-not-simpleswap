# CMC but not SimpleSwap

CMC but not SimpleSwap is a small Flask dashboard that highlights crypto assets
listed on CoinMarketCap but not currently available on SimpleSwap. The list is
sorted by 24-hour trading volume, making it easier to spot high-volume listing
gaps.

## Features

- Fetches the top CoinMarketCap assets by market cap.
- Fetches the active SimpleSwap currency list.
- Compares symbols across both sources, including `$TICKER` variants.
- Sorts missing SimpleSwap assets by 24-hour USD volume.
- Displays CoinMarketCap token icons through a local cached proxy.
- Includes a clean Coinbase-inspired dashboard UI with client-side search.

## Project Structure

```text
.
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── clients.py               # External HTTP clients
│   ├── routes.py                # Web routes and icon proxy
│   ├── services.py              # Comparison and sorting logic
│   ├── static/
│   │   ├── app.js               # Table filtering
│   │   └── styles.css           # UI styling
│   └── templates/
│       └── evercodelab.html     # Dashboard template
├── main.py                      # Local development entrypoint
├── wsgi.py                      # Production WSGI entrypoint
├── Procfile                     # Gunicorn process definition
└── requirements.txt
```

## Requirements

- Python 3.9+
- Network access to:
  - `api.coinmarketcap.com`
  - `simpleswap.io`
  - `s2.coinmarketcap.com`

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open http://localhost:5001/evercodelab.

The root route also redirects to the dashboard:

```text
http://localhost:5001/
```

Health check:

```text
http://localhost:5001/health
```

## Production

Run with Gunicorn:

```bash
gunicorn wsgi:app
```

For platforms that support a `Procfile`, the app is ready to run with:

```text
web: gunicorn wsgi:app
```

## Notes

- CoinMarketCap and SimpleSwap endpoints used here are public web endpoints and
  can change behavior or rate limits over time.
- Coin icons are proxied through the Flask app and cached in memory per process,
  so the browser does not need to hotlink the CoinMarketCap CDN directly.
- The dashboard performs live API requests on each page render. Add a scheduled
  cache or background refresh if this grows beyond a small internal tool.
