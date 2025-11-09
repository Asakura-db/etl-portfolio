"""
ETL Météo (Open-Meteo)
----------------------
Extraction des prévisions météo horaires via l'API open-meteo.com,
agrégation journalière et chargement dans PostgreSQL.

Technos : Python, requests, pandas, psycopg2, PostgreSQL.
"""

import os
from typing import Dict, Any
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"


def get_db_connection():
    # ✅ Même logique que dans ton script finance qui fonctionne
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="etl_portfolio",
        user="etl_user",
        password="etl_password",
    )
    conn.autocommit = False
    return conn


def extract_weather(latitude: float, longitude: float, timezone: str = "Europe/Paris") -> pd.DataFrame:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "timezone": timezone,
    }
    resp = requests.get(OPEN_METEO_API, params=params, timeout=30)
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    precipitation = hourly.get("precipitation", [])

    df = pd.DataFrame(
        {
            "time": pd.to_datetime(times),
            "temperature_2m": temps,
            "precipitation": precipitation,
        }
    )
    df["latitude"] = latitude
    df["longitude"] = longitude
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df["date"] = df["time"].dt.date
    agg = (
        df.groupby(["date", "latitude", "longitude"])
        .agg(
            temp_min=("temperature_2m", "min"),
            temp_max=("temperature_2m", "max"),
            temp_avg=("temperature_2m", "mean"),
            precipitation_sum=("precipitation", "sum"),
        )
        .reset_index()
    )

    agg["is_rainy"] = agg["precipitation_sum"] > 0.5
    agg["created_at"] = pd.Timestamp.utcnow()
    return agg


def load(df: pd.DataFrame, conn):
    if df.empty:
        print("No data to load.")
        return

    # ✅ Correction : on évite to_records() pour ne pas avoir de np.float64 dans le SQL
    records = list(
        df[
            [
                "date",
                "latitude",
                "longitude",
                "temp_min",
                "temp_max",
                "temp_avg",
                "precipitation_sum",
                "is_rainy",
                "created_at",
            ]
        ].itertuples(index=False, name=None)
    )

    with conn.cursor() as cur:
        sql = """
        INSERT INTO daily_weather (
            date,
            latitude,
            longitude,
            temp_min,
            temp_max,
            temp_avg,
            precipitation_sum,
            is_rainy,
            created_at
        )
        VALUES %s
        ON CONFLICT (date, latitude, longitude)
        DO UPDATE SET
            temp_min = EXCLUDED.temp_min,
            temp_max = EXCLUDED.temp_max,
            temp_avg = EXCLUDED.temp_avg,
            precipitation_sum = EXCLUDED.precipitation_sum,
            is_rainy = EXCLUDED.is_rainy,
            created_at = EXCLUDED.created_at;
        """
        execute_values(cur, sql, records)
    conn.commit()
    print(f"Loaded {len(df)} rows into daily_weather.")


def run_etl_for_city(latitude: float, longitude: float):
    raw = extract_weather(latitude, longitude)
    df = transform(raw)
    conn = get_db_connection()
    try:
        load(df, conn)
    finally:
        conn.close()


if __name__ == "__main__":
    lat = float(os.getenv("CITY_LATITUDE", "48.8566"))   # Paris par défaut
    lon = float(os.getenv("CITY_LONGITUDE", "2.3522"))
    run_etl_for_city(lat, lon)
