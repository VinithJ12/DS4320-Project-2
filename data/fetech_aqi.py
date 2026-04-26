"""
fetch_aqi.py

Pulls daily AQI readings for Harris County (Houston), TX from the
EPA Air Quality System (AQS) API and loads them into MongoDB Atlas.

Collections populated : houston_airquality.aqi_readings
Pollutants pulled     : PM2.5 (88101), Ozone (44201), NO2 (42602)
Date range            : 2021 - 2023
Geographic scope      : Harris County, TX (state=48, county=201)

Usage:
    python fetch_aqi.py

Author : Vinith J (jvinith2) — DS 4320 Spring 2026
"""

import requests
import logging
import sys
import os
from datetime import datetime
from pymongo import MongoClient, errors

# Logging
# Logs go to both the console and a local file for auditing
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler("fetch_aqi.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Configuration 
# Replace PASSWORD with your MongoDB Atlas password before running
MONGO_URI = "mongodb+srv://USER:PASSWORD@cluster0.yyvifrz.mongodb.net/"

# EPA AQS credentials — register free at https://aqs.epa.gov/data/api/signup
EPA_EMAIL = "YOU_EPA_EMAIL"
EPA_KEY   = "YOUR_EPA_KEY"

# Harris County FIPS: state 48 (Texas), county 201 (Harris)
STATE_FIPS  = "48"
COUNTY_FIPS = "201"

# Pollutants to pull — chosen because they are the three most relevant
# to the Houston Ship Channel industrial corridor and vehicle traffic
PARAM_CODES = {
    "88101": "PM2.5",   # Fine particulate matter — most dangerous to lungs
    "44201": "Ozone",   # Ground-level ozone — Houston's primary EPA violation
    "42602": "NO2",     # Nitrogen dioxide — direct industrial/vehicle emission
}

# Year range — 2021-2023 gives three full years of comparable data
# 2020 was excluded due to COVID-19 lockdown suppressing normal emission levels
YEARS = ["2021", "2022", "2023"]

EPA_BASE_URL = "https://aqs.epa.gov/data/api/dailyData/byCounty"


def connect_mongo(uri: str):
    """
    Connect to MongoDB Atlas and verify with a ping.
    Raises ConnectionFailure immediately if the URI or credentials are wrong.
    """
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=10_000)
        client.admin.command("ping")
        logger.info("Connected to MongoDB Atlas successfully.")
        return client
    except errors.ConnectionFailure as exc:
        logger.error("Could not connect to MongoDB: %s", exc)
        raise


def fetch_aqi_for_param(param_code: str, year: str) -> list:
    """
    Call the EPA AQS dailyData/byCounty endpoint for one parameter and year.
    Returns a list of raw record dicts, or an empty list on any failure.

    Parameters
    ----------
    param_code : str  EPA parameter code (e.g. '88101' for PM2.5)
    year       : str  Four-digit year string (e.g. '2023')
    """
    params = {
        "email":  EPA_EMAIL,
        "key":    EPA_KEY,
        "param":  param_code,
        "bdate":  f"{year}0101",   # Begin date: January 1st of the year
        "edate":  f"{year}1231",   # End date: December 31st of the year
        "state":  STATE_FIPS,
        "county": COUNTY_FIPS,
    }

    try:
        logger.info("Fetching param=%s  year=%s ...", param_code, year)
        response = requests.get(EPA_BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()

        # EPA wraps results in a 'Data' key — warn if it's missing
        if "Data" not in payload or not payload["Data"]:
            logger.warning("No data returned for param %s year %s.", param_code, year)
            return []

        records = payload["Data"]
        logger.info("  → Retrieved %d records", len(records))
        return records

    except requests.exceptions.Timeout:
        logger.error("Request timed out for param %s year %s.", param_code, year)
        return []
    except requests.exceptions.HTTPError as exc:
        logger.error("HTTP error for param %s: %s", param_code, exc)
        return []
    except Exception as exc:
        logger.error("Unexpected error for param %s: %s", param_code, exc)
        return []


def insert_records(collection, records: list) -> int:
    """
    Insert a list of raw EPA records into MongoDB.
    Uses ordered=False so a duplicate key error doesn't abort the entire batch.
    Returns the number of documents successfully inserted.

    Parameters
    ----------
    collection : pymongo collection object
    records    : list of raw record dicts from the EPA API
    """
    if not records:
        return 0

    try:
        result   = collection.insert_many(records, ordered=False)
        inserted = len(result.inserted_ids)
        logger.info("  Inserted %d documents.", inserted)
        return inserted
    except errors.BulkWriteError as bwe:
        # Some records inserted before the error — log partial success
        inserted = bwe.details.get("nInserted", 0)
        logger.warning("  BulkWriteError: %d inserted before error.", inserted)
        return inserted


def main():
    """
    Main entry point:
      1. Connect to MongoDB
      2. For each pollutant and each year, fetch → insert into aqi_readings
      3. Log final totals
    """
    logger.info("=== fetch_aqi.py starting ===")

    client     = connect_mongo(MONGO_URI)
    db         = client["houston_airquality"]
    collection = db["aqi_readings"]

    # Unique index prevents duplicate inserts if the script is re-run
    collection.create_index(
        [("date_local", 1), ("site_num", 1), ("parameter_code", 1)],
        unique=True,
        background=True
    )

    total_inserted = 0

    # Loop over every pollutant and every year
    for param_code, param_name in PARAM_CODES.items():
        logger.info("--- Pollutant: %s (%s) ---", param_name, param_code)
        for year in YEARS:
            records        = fetch_aqi_for_param(param_code, year)
            inserted       = insert_records(collection, records)
            total_inserted += inserted

    # Final summary
    final_count = collection.count_documents({})
    logger.info(
        "=== Done. Inserted this run: %d | Collection total: %d ===",
        total_inserted, final_count
    )
    client.close()


if __name__ == "__main__":
    main()
