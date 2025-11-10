# Portfolio ETL – Python & PostgreSQL

Ce dépôt regroupe **trois pipelines ETL complets** développés en Python, avec
chargement des données dans une base **PostgreSQL** :

1. **ETL Finance Crypto** – Récupération de prix de cryptomonnaies via API CoinGecko  
2. **ETL Météo** – Agrégation de prévisions météo via l’API Open-Meteo  
3. **ETL Offres d’emploi** – Web scraping d’annonces de jobs (site de démo + variante France)

L’objectif est de montrer une capacité à :

- Consommer des **APIs REST**
- Faire du **web scraping** en Python
- Appliquer des **transformations de données** (nettoyage, agrégation, feature engineering)
- Charger les données dans **PostgreSQL** via `psycopg2`
- Organiser plusieurs projets ETL dans une même base de code.

---

## 📁 Structure du dépôt

```text
etl_portfolio/
├─ README.md
├─ etl_finance.py
├─ schema_finance.sql
├─ README_Finance.md          
├─ etl_weather.py
├─ schema_weather.sql
├─ README_meteo.md
├─ etl_jobs.py
├─ etl_jobs_france.py   
├─ schema_jobs.sql
└─ README_Emploi.md
