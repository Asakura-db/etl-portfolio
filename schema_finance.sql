-- Schéma pour le projet ETL Finance Crypto

CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_id TEXT NOT NULL,
    vs_currency TEXT NOT NULL,
    price NUMERIC(18,8) NOT NULL,
    market_cap NUMERIC(22,2),
    volume_24h NUMERIC(22,2),
    change_24h NUMERIC(10,4),
    last_updated_at TIMESTAMPTZ NOT NULL,
    ingestion_ts TIMESTAMPTZ NOT NULL,
    CONSTRAINT uq_crypto_point UNIQUE (coin_id, vs_currency, last_updated_at)
);

CREATE INDEX IF NOT EXISTS idx_crypto_prices_coin_ts
    ON crypto_prices (coin_id, last_updated_at);
