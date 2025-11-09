"""
ETL Offres d'emploi (Web Scraping)
----------------------------------
Scraping d'une page d'offres d'emploi (site de démonstration), transformation
des données et chargement dans PostgreSQL.

Technos : Python, requests, BeautifulSoup, psycopg2, PostgreSQL.
"""

import os
from typing import List
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import execute_values
import datetime as dt

JOBS_URL = "https://realpython.github.io/fake-jobs/" 


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="etl_portfolio",
        user="etl_user",
        password="etl_password",
    )
    conn.autocommit = False
    return conn


def extract_jobs(url: str = JOBS_URL) -> List[dict]:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select("div.card-content")

    jobs = []
    for card in cards:
        title_el = card.select_one("h2.title")
        company_el = card.select_one("h3.subtitle")
        location_el = card.select_one("p.location")
        date_el = card.select_one("time")
        link_el = card.select_one("a")

        job = {
            "title": title_el.get_text(strip=True) if title_el else None,
            "company": company_el.get_text(strip=True) if company_el else None,
            "location": location_el.get_text(strip=True) if location_el else None,
            "date_posted": date_el["datetime"] if date_el and date_el.has_attr("datetime") else None,
            "detail_url": link_el["href"] if link_el and link_el.has_attr("href") else None,
        }
        jobs.append(job)

    return jobs


def transform(jobs: List[dict]):
    transformed = []
    for job in jobs:
        if not job.get("title"):
            continue

        raw_loc = (job.get("location") or "").lower()
        if "remote" in raw_loc or "télétravail" in raw_loc:
            job_type = "remote"
        else:
            job_type = "on-site"

        date_posted = job.get("date_posted")
        if date_posted:
            try:
                date_posted = dt.date.fromisoformat(date_posted)
            except ValueError:
                date_posted = None

        transformed.append(
            {
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "job_type": job_type,
                "date_posted": date_posted,
                "detail_url": job.get("detail_url"),
                "scraped_at": dt.datetime.utcnow(),
            }
        )

    return transformed


def load(jobs: List[dict], conn):
    if not jobs:
        print("No jobs to load.")
        return

    rows = [
        (
            j["title"],
            j["company"],
            j["location"],
            j["job_type"],
            j["date_posted"],
            j["detail_url"],
            j["scraped_at"],
        )
        for j in jobs
    ]

    with conn.cursor() as cur:
        sql = """
        INSERT INTO job_offers (
            title,
            company,
            location,
            job_type,
            date_posted,
            detail_url,
            scraped_at
        ) VALUES %s;
        """
        execute_values(cur, sql, rows)

    conn.commit()
    print(f"Loaded {len(jobs)} job offers into job_offers.")

def run_etl():
    raw_jobs = extract_jobs()
    jobs = transform(raw_jobs)
    conn = get_db_connection()
    try:
        load(jobs, conn)
    finally:
        conn.close()

if __name__ == "__main__":
    run_etl()
