DS 4320 Project 2
Breathing Inequality — Houston Air Quality vs. Neighborhood Income

Name: Vinith J
NetID: jvinith2
DOI: 10.5281/zenodo.XXXXXXX (replace after Zenodo upload)

Press Release: docs/press_release.md
Pipeline: pipeline/pipeline.ipynb
License: MIT (see LICENSE)
Executive Summary

This project investigates environmental justice in Houston, TX by asking whether low-income neighborhoods experience measurably worse air quality than higher-income neighborhoods.

Five years of daily AQI readings (2020–2024) from EPA monitoring stations in Harris County are joined with U.S. Census median household income data at the ZIP code level using a MongoDB Atlas database. A Python-based pipeline aggregates air quality by ZIP code and applies linear regression and Random Forest models to test whether income predicts AQI.

Key finding: There is a statistically significant negative relationship between income and AQI — as neighborhood income increases, AQI decreases.

The lowest-income ZIP codes — concentrated near the Houston Ship Channel industrial corridor — experience disproportionately high pollution exposure.

Problem Definition
General Problem

Predicting air quality.

Specific Problem Statement

Do low-income neighborhoods in Houston, TX experience worse air quality (AQI) than higher-income neighborhoods, and can median household income predict AQI at the ZIP code level?

Motivation

Air pollution is unevenly distributed. In Houston — home to one of the largest petrochemical hubs in the world — industrial activity is concentrated in specific neighborhoods, which are often low-income and majority-minority communities.

Understanding this relationship is critical for:

Public health policy
Urban zoning decisions
Environmental justice advocacy

If low-income areas consistently show higher AQI, it indicates a systemic inequity requiring targeted intervention.

Refinement Rationale

The broad problem of “predicting air quality” was refined to:

Houston (high pollution + income inequality)
AQI (policy-relevant metric)
ZIP code level (joinable geography)

This transforms a forecasting task into an equity-driven data science problem with direct real-world implications.

Press Release

Breathing Inequality: Houston's Poorest Neighborhoods Choke on the Worst Air
See: docs/press_release.md

Domain Exposition
Key Terminology
Term	Definition
AQI	Air Quality Index (0–500 scale; higher = worse pollution)
PM2.5	Fine particulate matter (<2.5 microns)
Ozone (O₃)	Pollutant formed by sunlight + emissions
EPA	U.S. Environmental Protection Agency
AQS	EPA Air Quality System (monitoring + API)
ZCTA	ZIP Code Tabulation Area (Census geography)
Median Household Income	Proxy for neighborhood wealth
Environmental Justice	Equal protection from environmental harm
NO₂	Traffic/industrial pollutant
MOE	Margin of Error (ACS uncertainty measure)
ACS	American Community Survey
Harris County	County containing Houston
Domain Context

This project sits at the intersection of environmental science and public health equity.

Houston’s east side, near the Ship Channel, is one of the most industrialized regions in North America and has historically exposed nearby low-income communities to elevated pollution levels.

By combining:

EPA AQI data (AQS API)
Census income data (ACS)

we quantify how pollution varies across income levels and test statistical significance.

Background Reading
Title	Description
EPA AQS Documentation	Air quality API + structure
CDC — Air Quality & Health	Health impacts of AQI
Houston Air Quality History	Long-term pollution trends
Environmental Justice in Houston	Academic context
Census ACS Documentation	Income data methodology
Data Creation
Data Sources

Air Quality Data

Source: EPA AQS API
Scope: Harris County, TX
Years: 2020–2024
Pollutants: PM2.5, Ozone, NO₂

Income Data

Source: U.S. Census ACS (2022, 5-year estimates)
Variable: Median household income
Geography: Houston ZCTAs (770xx ZIP codes)
Data Integration
Stored in MongoDB Atlas
Joined on ZIP code
Queried via Python pipeline
Source Code
File	Description
data/fetch_aqi.py	Pulls AQI data from EPA
data/fetch_income.py	Pulls Census income data
pipeline/pipeline.ipynb	Full analysis pipeline
Rationale for Key Decisions
AQI as outcome: Policy-relevant, but hides pollutant-level detail
ZIP code geography: Joinable but coarse
Manual station mapping: Necessary but introduces spatial error
2020–2024 range: Stable averages, but COVID impacts included
Bias Identification
Monitoring station placement bias
ACS sampling bias
COVID-era temporal bias
Pollutant selection bias
Bias Mitigation
Exclude ZIP codes with <30 readings
Flag high MOE income estimates (>10%)
Document station-to-ZIP mapping
Retain uncertainty fields
Metadata
Collections
aqi_readings

Required fields:

date_local (string)
parameter (string)
aqi (int)
latitude, longitude (float)
site_num (string)
fetched_at (datetime)
income_by_zip

Required fields:

zip_code (string)
median_income (int)
moe (int)
population (int)
high_moe_flag (bool)

Convention: snake_case only

Data Summary
Collection	Documents	Date Range	Scope	Source
aqi_readings	33,930+	2020–2024	Harris County	EPA
income_by_zip	96	2022	Houston ZIPs	Census
Data Dictionary (Selected Fields)
Field	Type	Description
aqi	int	Air Quality Index
date_local	string	Date (YYYY-MM-DD)
parameter	string	Pollutant type
arithmetic_mean	float	Daily average
first_max_value	float	Peak reading
zip_code	string	ZIP code
median_income	int	Income (USD)
moe	int	Margin of error
Feature Uncertainty
Feature	Uncertainty	Handling
aqi	Sensor + sparse coverage	Mean/std per ZIP
arithmetic_mean	Misses spikes	Compare with max
location	ZIP mapping error	Documented
median_income	Survey-based	Use MOE
temporal	COVID effects	Compare yearly
Repository Structure
houston_airquality/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── fetch_aqi.py
│   └── fetch_income.py
├── pipeline/
│   ├── pipeline.ipynb
│   └── pipeline.md
├── docs/
│   ├── press_release.md
│   └── houston_aqi_income_analysis.png
└── logs/
    ├── fetch_aqi.log
    ├── fetch_income.log
    └── pipeline.log
