# Projet 1 - Pipeline ETL Finance Crypto (API CoinGecko)

## Objectif

Construire un pipeline ETL complet qui récupère les prix de plusieurs cryptomonnaies
via l'API publique de **CoinGecko**, transforme les données (typage, timestamp, variation)
et les charge dans une base **PostgreSQL** pour analyse.

## Stack technique

- Langages : **Python**, **SQL**
- Base de données : **PostgreSQL**
- Librairies Python : `requests`, `pandas`, `psycopg2-binary`
- Outils possibles : VS Code, DBeaver, pgAdmin

## Architecture

1. **Extract** : appel HTTP à l'API `https://api.coingecko.com/api/v3/simple/price`
2. **Transform** :
   - Conversion des timestamps en `TIMESTAMPTZ`
   - Conversion des types numériques
   - Ajout d'un champ `ingestion_ts`
3. **Load** :
   - Insertion dans la table `crypto_prices`
   - Upsert via `ON CONFLICT` sur `(coin_id, vs_currency, last_updated_at)`

## Pré-requis

- PostgreSQL installé
- Base de données créée, par exemple `etl_portfolio`
- Un utilisateur avec droits d'écriture, par exemple `etl_user`

## Installation

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Configurer les variables d'environnement (adapter selon votre setup) :

```bash
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="etl_portfolio"
export DB_USER="etl_user"
export DB_PASSWORD="etl_password"
```

## Création du schéma

Depuis `psql` ou un client SQL :

```sql
\i projects/project1_finance_api/schema_finance.sql
```

## Exécution du pipeline

### Exécution simple (une fois)

```bash
python projects/project1_finance_api/etl_finance.py
```

### Exécution planifiée (boucle simple)

Vous pouvez activer une exécution périodique en définissant la variable :

```bash
export ETL_INTERVAL_SECONDS=600
python projects/project1_finance_api/etl_finance.py
```

Tu peux la reformuler comme ça :

Pour une vraie orchestration, il est possible d’automatiser ce script avec un outil comme **Airflow** ou via un **cron** système.

