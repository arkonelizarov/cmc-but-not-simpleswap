from functools import lru_cache

import requests


CMC_LISTING_URL = (
    "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing"
)
CMC_ICON_URL = "https://s2.coinmarketcap.com/static/img/coins/64x64/{coin_id}.png"
SIMPLESWAP_CURRENCIES_URL = "https://simpleswap.io/api/v3/currencies"
REQUEST_TIMEOUT = 20
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
JSON_HEADERS = {
    "Accept": "application/json",
    "User-Agent": USER_AGENT,
}
IMAGE_HEADERS = {
    "Accept": "image/png,image/*,*/*;q=0.8",
    "User-Agent": USER_AGENT,
}


def get_json(url, params=None):
    response = requests.get(
        url,
        params=params,
        headers=JSON_HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


@lru_cache(maxsize=1024)
def fetch_cmc_icon(coin_id):
    response = requests.get(
        CMC_ICON_URL.format(coin_id=coin_id),
        headers=IMAGE_HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.content, response.headers.get("Content-Type", "image/png")


def fetch_cmc_coins(limit=1500):
    params = {
        "start": 1,
        "limit": limit,
        "sortBy": "market_cap",
        "sortType": "desc",
        "convert": "USD,BTC,ETH",
        "cryptoType": "all",
        "tagType": "all",
        "audited": "false",
        "aux": (
            "ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,"
            "max_supply,circulating_supply,total_supply,volume_7d,volume_30d,"
            "self_reported_circulating_supply,self_reported_market_cap"
        ),
    }
    data = get_json(CMC_LISTING_URL, params=params)
    return data["data"]["cryptoCurrencyList"]


def fetch_simpleswap_currencies():
    params = {
        "fixed": "false",
        "includeDisabled": "false",
    }
    return get_json(SIMPLESWAP_CURRENCIES_URL, params=params)
