-- Schéma pour le projet ETL Offres d'emploi (Web Scraping)

CREATE TABLE IF NOT EXISTS job_offers (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    job_type TEXT,
    date_posted DATE,
    detail_url TEXT,
    scraped_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_job_offers_company
    ON job_offers (company);

CREATE INDEX IF NOT EXISTS idx_job_offers_date_posted
    ON job_offers (date_posted);
