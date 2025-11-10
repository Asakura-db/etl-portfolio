# Projet 2 - Pipeline ETL Météo (API Open-Meteo)

## Objectif

Construire un pipeline ETL qui récupère les prévisions météo horaires via l'API
**open-meteo.com**, agrège ces données au niveau **journalier** et les charge
dans une table PostgreSQL pour exploitation (dashboards, analyses temporelles).

## Stack technique

- Langages : **Python**, **SQL**
- Base : **PostgreSQL**
- Librairies : `requests`, `pandas`, `psycopg2-binary`

## Architecture

1. **Extract** : appel à `https://api.open-meteo.com/v1/forecast` avec latitude/longitude
2. **Transform** :
   - Agrégation par date (min, max, moyenne, somme des précipitations)
   - Création d'un flag `is_rainy`
3. **Load** :
   - Upsert dans la table `daily_weather` (clé primaire `date, latitude, longitude`)

## Pré-requis

- DB PostgreSQL disponible (même base que les autres projets possible : `etl_portfolio`)
- Variables d'environnement DB configurées (voir projet Finance)

## Création du schéma

```sql
\i projects/project2_weather_api/schema_weather.sql
```

## Exécution

Par défaut, le script utilise les coordonnées de **Paris** :

```bash
python projects/project2_weather_api/etl_weather.py
```

Pour changer la ville, passer des variables :

```bash
export CITY_LATITUDE=43.6047
export CITY_LONGITUDE=1.4442
python projects/project2_weather_api/etl_weather.py
```

Vous pouvez ensuite interroger la table `daily_weather` pour visualiser l'historique.
