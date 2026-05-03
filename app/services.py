from app.clients import fetch_cmc_coins, fetch_simpleswap_currencies


def get_cmc_only_coins():
    cmc_coins = fetch_cmc_coins()
    simpleswap_symbols = get_simpleswap_symbols()

    result = []
    for coin in cmc_coins:
        symbol = coin["symbol"].upper()
        symbol_without_dollar = strip_leading_dollar(symbol)

        if symbol in simpleswap_symbols or symbol_without_dollar in simpleswap_symbols:
            continue

        result.append(
            {
                "symbol": symbol,
                "volume_24h": get_usd_volume_24h(coin),
                "url": f"https://coinmarketcap.com/currencies/{coin['slug']}/",
                "icon_id": coin.get("id"),
            }
        )

    return sorted(result, key=lambda coin: coin["volume_24h"], reverse=True)


def get_simpleswap_symbols():
    symbols = set()

    for currency in fetch_simpleswap_currencies():
        for key in ("cmcTicker", "symbolFront", "symbol"):
            symbol = currency.get(key)
            if not symbol:
                continue

            symbol = symbol.upper()
            symbols.add(symbol)
            symbols.add(strip_leading_dollar(symbol))

    return symbols


def get_usd_volume_24h(coin):
    for quote in coin.get("quotes", []):
        if quote.get("name") == "USD":
            return quote.get("volume24h", 0)
    return 0


def strip_leading_dollar(symbol):
    return symbol[1:] if symbol.startswith("$") else symbol
