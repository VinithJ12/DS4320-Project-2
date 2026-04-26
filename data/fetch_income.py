"""
fetch_income.py
Pulls median household income by ZIP Code Tabulation Area (ZCTA)
for the Houston, TX area from the US Census Bureau's American
Community Survey (ACS) 5-year estimates, then loads them into
MongoDB Atlas.

Collection populated : houston_airquality.income_by_zip
Geographic scope     : Houston ZCTAs beginning with '770'
ACS reference year   : 2022 (most recent 5-year estimates available)

Usage:
    python fetch_income.py

Author : Vinith J (uhe5bj) — DS 4320 Spring 2026
"""

import requests
import logging
import sys
from datetime import datetime
from pymongo import MongoClient, errors

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler("fetch_income.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Configuration 
# Replace PASSWORD with your MongoDB Atlas password before running
MONGO_URI = "mongodb+srv://USER:PASSWORD@cluster0.yyvifrz.mongodb.net/"

# Census API key — register free at https://api.census.gov/data/key_signup.html
CENSUS_KEY = "YOUR_CENSUS_KEY"

# ACS endpoint for 2022 5-year estimates
CENSUS_URL = "https://api.census.gov/data/2022/acs/acs5"

# Variables to pull:
#   B19013_001E = Median household income estimate (dollars)
#   B19013_001M = Margin of error for that estimate
#   B01003_001E = Total population
ACS_VARS = "NAME,B19013_001E,B19013_001M,B01003_001E"

# Houston ZCTAs all begin with '770'
HOUSTON_PREFIX = "770"

# Census sentinel value for suppressed / unavailable data
CENSUS_NULL = "-666666666"


def connect_mongo(uri: str):
    """
    Connect to MongoDB Atlas and verify with a ping.
    Raises ConnectionFailure immediately if credentials are wrong.
    """
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=10_000)
        client.admin.command("ping")
        logger.info("Connected to MongoDB Atlas successfully.")
        return client
    except errors.ConnectionFailure as exc:
        logger.error("MongoDB connection failed: %s", exc)
        raise


def fetch_all_zcta_income() -> list:
    """
    Query the Census ACS API for median household income across all US ZCTAs.
    We pull all ZCTAs and filter to Houston locally because the Census API
    does not support prefix-based filtering on ZCTAs directly.

    Returns a list of raw row dicts with Census-style keys.
    """
    params = {
        "get": ACS_VARS,
        "for": "zip code tabulation area:*",  # All US ZCTAs
        "key": CENSUS_KEY,
    }

    try:
        logger.info("Fetching Census ACS income data (all US ZCTAs)...")
        response = requests.get(CENSUS_URL, params=params, timeout=90)
        response.raise_for_status()

        # Census returns JSON as a list of lists — first row is headers
        rows    = response.json()
        headers = rows[0]
        records = [dict(zip(headers, row)) for row in rows[1:]]

        logger.info("Retrieved %d total ZCTA records from Census.", len(records))
        return records

    except requests.exceptions.Timeout:
        logger.error("Census API request timed out.")
        return []
    except requests.exceptions.HTTPError as exc:
        logger.error("Census API HTTP error: %s", exc)
        return []
    except Exception as exc:
        logger.error("Unexpected error fetching Census data: %s", exc)
        return []


def clean_and_filter(raw_records: list) -> list:
    """
    Filter to Houston ZCTAs (770xx) and clean each record.
    Skips ZCTAs where income is suppressed by the Census.
    Flags ZCTAs where the margin of error exceeds 10% of the estimate
    as statistically uncertain.

    Parameters
    
    raw_records : list of raw Census ZCTA dicts
    """
    cleaned = []

    for r in raw_records:
        zcta = r.get("zip code tabulation area", "")

        # Keep only Houston ZCTAs
        if not zcta.startswith(HOUSTON_PREFIX):
            continue

        income_str = r.get("B19013_001E", CENSUS_NULL)
        moe_str    = r.get("B19013_001M", CENSUS_NULL)
        pop_str    = r.get("B01003_001E", "0")

        # Skip ZCTAs where income data is suppressed
        if income_str in (CENSUS_NULL, None, ""):
            logger.debug("Skipping ZCTA %s — income suppressed.", zcta)
            continue

        try:
            income = int(income_str)
            moe    = int(moe_str) if moe_str not in (CENSUS_NULL, None) else None
            pop    = int(pop_str) if pop_str else 0
        except ValueError as exc:
            logger.warning("Could not parse ZCTA %s: %s. Skipping.", zcta, exc)
            continue

        # Flag ZCTAs where MOE > 10% of income — statistically uncertain estimates
        # These are excluded from the regression analysis but kept in the database
        high_moe = (
            moe is not None and income > 0 and (moe / income) > 0.10
        )

        cleaned.append({
            "zip_code":      zcta,
            "median_income": income,
            "moe":           moe,
            "population":    pop,
            "high_moe_flag": high_moe,  # True = income estimate is statistically uncertain
            "year":          2022,       # ACS 5-year estimates reference year
            "fetched_at":    datetime.utcnow().isoformat(),
        })

    logger.info("%d Houston ZCTAs after filtering.", len(cleaned))
    return cleaned


def insert_records(collection, records: list) -> int:
    """
    Insert cleaned income records into MongoDB.
    Uses ordered=False so a duplicate key error doesn't abort the batch.
    Returns the number of documents successfully inserted.

    Parameters
    
    collection : pymongo collection object
    records    : list of cleaned income dicts
    """
    if not records:
        logger.info("No records to insert.")
        return 0

    try:
        result   = collection.insert_many(records, ordered=False)
        inserted = len(result.inserted_ids)
        logger.info("Inserted %d income records.", inserted)
        return inserted
    except errors.BulkWriteError as bwe:
        inserted = bwe.details.get("nInserted", 0)
        logger.warning("BulkWriteError: %d inserted before error.", inserted)
        return inserted


def main():
    """
    Main entry point:
      1. Connect to MongoDB
      2. Fetch all US ZCTA income data from Census ACS API
      3. Filter to Houston (770xx) and clean
      4. Insert into income_by_zip collection
    """
    logger.info("fetch_income.py starting...")

    client     = connect_mongo(MONGO_URI)
    db         = client["houston_airquality"]
    collection = db["income_by_zip"]

    # Unique index on zip_code + year prevents duplicate inserts
    collection.create_index(
        [("zip_code", 1), ("year", 1)],
        unique=True,
        background=True
    )

    # Fetch → filter → insert
    raw     = fetch_all_zcta_income()
    cleaned = clean_and_filter(raw)
    insert_records(collection, cleaned)

    final_count = collection.count_documents({})
    logger.info("=== Done. income_by_zip collection total: %d ===", final_count)
    client.close()


if __name__ == "__main__":
    main()
