"""
ETL Finance Crypto
-------------------
Extraction des prix de cryptomonnaies via l'API publique CoinGecko,
transformation des données puis chargement dans PostgreSQL.

Technos : Python, requests, pandas, psycopg2, PostgreSQL.
"""

import os
import time
from typing import List
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="etl_portfolio",   # nom de base SANS accent
        user="etl_user",          # utilisateur SANS accent
        password="etl_password",  # mot de passe SANS accent
    )
    conn.autocommit = False
    return conn



def extract_crypto_prices(coins: List[str], vs_currency: str = "usd") -> pd.DataFrame:
    params = {
        "ids": ",".join(coins),
        "vs_currencies": vs_currency,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true",
    }
    resp = requests.get(COINGECKO_API, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    rows = []
    for coin_id, payload in data.items():
        rows.append(
            {
                "coin_id": coin_id,
                "vs_currency": vs_currency,
                "price": payload.get(vs_currency),
                "market_cap": payload.get(f"{vs_currency}_market_cap"),
                "volume_24h": payload.get(f"{vs_currency}_24h_vol"),
                "change_24h": payload.get(f"{vs_currency}_24h_change"),
                "last_updated_at": payload.get("last_updated_at"),
            }
        )

    df = pd.DataFrame(rows)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df["last_updated_at"] = pd.to_datetime(df["last_updated_at"], unit="s", utc=True)
    df["ingestion_ts"] = pd.Timestamp.utcnow()
    df["change_24h"] = df["change_24h"].astype(float)
    df["price"] = df["price"].astype(float)

    return df


def load(df: pd.DataFrame, conn):
    if df.empty:
        print("No data to load.")
        return

    records = list(
        df[
            [
                "coin_id",
                "vs_currency",
                "price",
                "market_cap",
                "volume_24h",
                "change_24h",
                "last_updated_at",
                "ingestion_ts",
            ]
        ].itertuples(index=False, name=None)
    )

    with conn.cursor() as cur:
        sql = """
        INSERT INTO crypto_prices (
            coin_id,
            vs_currency,
            price,
            market_cap,
            volume_24h,
            change_24h,
            last_updated_at,
            ingestion_ts
        )
        VALUES %s
        ON CONFLICT (coin_id, vs_currency, last_updated_at)
        DO UPDATE SET
            price = EXCLUDED.price,
            market_cap = EXCLUDED.market_cap,
            volume_24h = EXCLUDED.volume_24h,
            change_24h = EXCLUDED.change_24h,
            ingestion_ts = EXCLUDED.ingestion_ts;
        """
        execute_values(cur, sql, records)
        
    conn.commit()
    print(f"Loaded {len(df)} rows into crypto_prices.")


def run_etl_once():
    coins = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]
    raw_df = extract_crypto_prices(coins)
    df = transform(raw_df)
    conn = get_db_connection()
    try:
        load(df, conn)
    finally:
        conn.close()


if __name__ == "__main__":
    interval_seconds = int(os.getenv("ETL_INTERVAL_SECONDS", "0"))

    if interval_seconds <= 0:
        run_etl_once()
    else:
        print(f"Starting scheduled ETL every {interval_seconds} seconds...")
        while True:
            run_etl_once()
            time.sleep(interval_seconds)
