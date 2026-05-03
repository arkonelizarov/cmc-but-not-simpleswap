import requests
from flask import Blueprint, Response, abort, redirect, render_template, url_for

from app.clients import fetch_cmc_icon
from app.services import get_cmc_only_coins


bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    return redirect(url_for("dashboard.cmc_but_not_simpleswap"))


@bp.route("/health")
def health():
    return {"status": "ok"}


@bp.route("/cmc-but-not-simpleswap")
def cmc_but_not_simpleswap():
    coins = get_cmc_only_coins()
    return render_template(
        "dashboard.html",
        coins=coins,
        total_coins=len(coins),
        total_volume=sum(coin["volume_24h"] for coin in coins),
        top_coin=coins[0] if coins else None,
    )


@bp.route("/icons/cmc/<int:coin_id>.png")
def cmc_icon(coin_id):
    try:
        content, content_type = fetch_cmc_icon(coin_id)
    except requests.RequestException:
        abort(404)

    return Response(
        content,
        content_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )
