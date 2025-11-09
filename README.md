# Projet 3 - Pipeline ETL Offres d'emploi (Web Scraping)

## Objectif

Mettre en place un pipeline ETL qui va :

1. **Scraper** une page d'offres d'emploi (site de démonstration pédagogique)
2. **Nettoyer et enrichir** les données (type de job, dates)
3. **Charger** les offres dans une table PostgreSQL `job_offers`

## Stack technique

- Langages : **Python**, **SQL**
- Base : **PostgreSQL**
- Librairies : `requests`, `beautifulsoup4`, `lxml`, `psycopg2-binary`

## Architecture

1. **Extract** : requête HTTP sur `https://realpython.github.io/fake-jobs/`
2. **Transform** :
   - Parsing HTML avec BeautifulSoup
   - Détection job `remote` vs `on-site`
   - Conversion de la date de publication
3. **Load** :
   - Insertion dans la table `job_offers`

## Création du schéma

```sql
\i projects/project3_jobs_scraping/schema_jobs.sql
```

## Exécution

```bash
python projects/project3_jobs_scraping/etl_jobs.py
```