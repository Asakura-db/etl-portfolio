-- Schéma pour le projet ETL Météo

CREATE TABLE IF NOT EXISTS daily_weather (
    date DATE NOT NULL,
    latitude NUMERIC(8,4) NOT NULL,
    longitude NUMERIC(8,4) NOT NULL,
    temp_min NUMERIC(5,2),
    temp_max NUMERIC(5,2),
    temp_avg NUMERIC(5,2),
    precipitation_sum NUMERIC(6,2),
    is_rainy BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (date, latitude, longitude)
);

CREATE INDEX IF NOT EXISTS idx_daily_weather_date
    ON daily_weather (date);
