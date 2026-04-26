# DS 4320 Project 2: Breathing Inequality — Houston Air Quality vs. Neighborhood Income

**Name:** Vinith J  
**NetID:** uhe5bj                                                  
**DOI:** [10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX) ← *replace with your Zenodo DOI after publishing*  
**Press Release:** [docs/press_release.md](docs/press_release.md)  
**Pipeline:** [pipeline/pipeline.ipynb](pipeline/pipeline.ipynb)  
**License:** MIT — see [LICENSE](LICENSE)                                                            
**COLAB OPTION** [COLAB_PIPELINE](https://colab.research.google.com/drive/16-y6oy4X8Zk9pa6OEwGadpMC-sSwXQss?usp=sharing)

---

## Executive Summary

This repository investigates environmental justice in Houston, TX by asking whether
low-income neighborhoods experience measurably worse air quality than higher-income
neighborhoods. Daily AQI readings (2021–2023) for three pollutants — PM2.5, Ozone,
and NO₂ — were collected from five EPA monitoring stations in Harris County via the
EPA AQS API and loaded into a MongoDB Atlas document database alongside US Census
median household income data at the ZIP code level. A Python analysis pipeline queries
both collections, joins them on ZIP code, and applies Pearson correlation and linear
regression models to test whether income predicts air quality. The key finding is
pollutant-specific: NO₂ shows the clearest environmental justice signal (r = -0.57),
with low-income eastern Houston ZIP codes bearing the highest direct industrial
emissions, while ozone — a secondary pollutant — drifts downwind to wealthier suburbs.
The database contains 134,889 AQI documents and 96 income documents across two
collections, fully establishing the secondary dataset required by this assignment.

---

## Problem Definition

### General and Specific Problem Statement

**General problem:** Predicting air quality.

**Specific problem:** Do low-income neighborhoods in Houston, TX experience worse
air quality (measured by AQI) than higher-income neighborhoods, and can neighborhood
median household income predict daily AQI readings at the ZIP code level across
PM2.5, Ozone, and NO₂ pollutants?

### Motivation

Air pollution is not distributed equally. In cities like Houston — home to one of
the largest petrochemical complexes in the world — industrial facilities, highways,
and refineries are concentrated in specific neighborhoods. Research consistently shows
these neighborhoods are more likely to be low-income and majority-minority communities.
Understanding whether income level predicts air quality in Houston is critically
important because it directly affects public health policy, zoning decisions, and
environmental justice advocacy. The residents of the Houston Ship Channel corridor
face daily exposure to pollutants that contribute to elevated rates of respiratory
disease, asthma hospitalization, and cardiovascular mortality. If low-income ZIP codes
consistently show higher pollution readings, that is evidence of a systemic problem
requiring targeted intervention — not just city-wide air quality improvements.
Documenting this pattern rigorously with government data is a prerequisite to
addressing it through policy.

### Refinement Rationale

The general problem of "predicting air quality" is too broad to be actionable — it
could mean anything from global climate modeling to next-hour pollution forecasts.
We refined it to Houston specifically because Houston has some of the worst air
quality in the United States and extreme income inequality across its neighborhoods,
making it an ideal city to detect an environmental justice signal. We further refined
the outcome to AQI (rather than raw pollutant concentrations) because AQI is the
standard public-facing measure that directly determines health advisories and resident
behavior — it is what matters most to the people affected. Breaking the analysis out
by pollutant type (PM2.5, Ozone, NO₂) rather than using a single combined AQI
transforms a potential null result into a nuanced, policy-relevant finding about
which specific pollution burdens fall disproportionately on low-income areas. The
ZIP code geographic unit was chosen because it is the finest level at which both
EPA monitoring data and Census income data are reliably joinable without additional
geospatial interpolation. This refinement connects a pure forecasting problem to
an equity analysis with real policy implications.

### Press Release Headline

**[Breathing Inequality: Houston's Poorest Neighborhoods Choke on the Worst Air](docs/press_release.md)**

---

## Domain Exposition

### Terminology

| Term | Definition |
|------|------------|
| AQI | Air Quality Index — a 0–500 scale where higher values indicate more pollution; above 100 is "Unhealthy for Sensitive Groups" |
| PM2.5 | Fine particulate matter under 2.5 microns in diameter — penetrates deep into lungs; most dangerous to cardiovascular and respiratory health |
| Ozone (O₃) | Ground-level ozone — a secondary pollutant formed when vehicle and industrial emissions react with sunlight; not directly emitted |
| NO₂ | Nitrogen dioxide — directly emitted by vehicles, power plants, and industrial facilities; indicator of proximity to emission sources |
| EPA | US Environmental Protection Agency — collects and publishes air quality data via the AQS monitoring network |
| AQS | EPA Air Quality System — the national network of fixed monitoring stations and the public API providing their data |
| ZCTA | ZIP Code Tabulation Area — Census geographic unit approximating postal ZIP codes; used to join AQI and income data |
| Median household income | Census measure of the midpoint income in a geographic area; used as a proxy for neighborhood socioeconomic status |
| Environmental justice | The principle that all people deserve equal protection from environmental and health hazards regardless of race or income |
| MOE | Margin of Error — the Census uncertainty estimate for ACS survey-based statistics |
| ACS | American Community Survey — the Census Bureau's ongoing survey providing demographic and income data by geography |
| Harris County | The Texas county encompassing Houston; the smallest EPA data unit that captures all Houston monitoring stations |
| Ozone transport | The atmospheric process by which ozone precursors drift downwind and form ozone away from the original emission source |

### Domain Paragraph

This project lives at the intersection of environmental science and public health
equity. Houston, TX is the fourth-largest city in the United States and sits in the
Houston-Galveston-Brazoria region, which has repeatedly violated EPA ozone standards
for decades. The city's east side is home to the Houston Ship Channel, one of the
most industrially dense corridors in North America, surrounded by low-income and
minority neighborhoods that have historically borne the burden of petrochemical
production. Air quality data is collected by the EPA through a network of fixed
monitoring stations and made publicly available through the AQS API — Harris County
has five active stations, which is itself a limitation that reflects the
under-monitoring of industrially impacted areas. Census income data is available
at the ZIP code level through the American Community Survey (ACS) 5-year estimates,
which pool five years of survey responses for statistical reliability at small
geographies. By storing both datasets in MongoDB Atlas and analyzing AQI readings
broken out by pollutant type across income levels, this project quantifies which
specific air quality burdens fall disproportionately on low-income Houston
neighborhoods and provides the data-driven foundation for targeted environmental
policy.

### Background Reading

Background reading copies are stored in the project's OneDrive folder:  
[📁 Background Readings Folder](https://myuva-my.sharepoint.com/:f:/g/personal/uhe5bj_virginia_edu/IgBiJU3LXW5lTZVPmsqIgTwwAYYUeS0M-9bvsMmaClC-Ves?e=WaKzGr)

| Title | Description | Link |
|-------|-------------|------|
| EPA AQS Data Documentation | Official documentation for the EPA Air Quality System API — explains data fields, parameter codes, and access methods used in this project | [aqs.epa.gov](https://aqs.epa.gov/aqsweb/documents/about_aqs_data.html) |
| CDC — Air Quality and Health | CDC overview of how each AQI level (Good, Moderate, Unhealthy) affects human health across different population groups | [cdc.gov](https://www.cdc.gov/air/default.htm) |
| Houston Air Quality History | Houston Chronicle investigative reporting on Houston's decades-long struggle with air quality and the communities most affected | [houstonchronicle.com](https://www.houstonchronicle.com) |
| Environmental Justice in Houston | Academic overview of environmental inequity in Houston's east-side communities near the Ship Channel, covering historical context and policy failures | [sesync.org](https://www.sesync.org/resources/environmental-justice-houston) |
| US Census ACS Documentation | How to access, interpret, and correctly use median household income and margin of error estimates by ZIP code from the ACS 5-year estimates | [census.gov](https://www.census.gov/programs-surveys/acs) |

---

## Data Creation

### Data Acquisition Provenance

Air quality data was obtained from the EPA Air Quality System (AQS) API
(aqs.epa.gov), a publicly available federal database containing daily AQI readings
from monitoring stations across the United States. Data was filtered to Harris County,
TX (state FIPS 48, county FIPS 201 — the county containing Houston) and pulled for
2021–2023, covering three pollutants: PM2.5 (parameter code 88101), Ozone (44201),
and NO₂ (42602). Each record in the database represents one daily AQI reading at one
specific monitoring station, identified by GPS coordinates and an EPA site number.
The final `aqi_readings` collection contains 134,889 documents across five monitoring
stations in Harris County.

Income data was obtained from the US Census Bureau's American Community Survey (ACS)
5-year estimates for reference year 2022, accessed via the Census Data API
(api.census.gov). This dataset provides median household income (variable B19013_001E)
and its margin of error (B19013_001M) at the ZIP Code Tabulation Area (ZCTA) level.
All US ZCTAs were pulled and filtered locally to Houston ZCTAs (those beginning with
"770"), excluding ZIP codes where income was suppressed by the Census (sentinel value
-666666666). The final `income_by_zip` collection contains 96 Houston ZCTA documents.

### Source Code

| File | Description | Link |
|------|-------------|------|
| `data/fetch_aqi.py` | Pulls daily PM2.5, Ozone, and NO₂ AQI readings for Harris County TX from the EPA AQS API (2021–2023) and loads them into the `aqi_readings` MongoDB collection | [data/fetch_aqi.py](data/fetch_aqi.py) |
| `data/fetch_income.py` | Pulls median household income and margin of error by ZCTA from the Census ACS API, filters to Houston 770xx ZIP codes, and loads into the `income_by_zip` MongoDB collection | [data/fetch_income.py](data/fetch_income.py) |
| `pipeline/pipeline.ipynb` | Full analysis pipeline — queries MongoDB, joins collections, runs correlation and regression models, and produces the publication-quality figure | [pipeline/pipeline.ipynb](pipeline/pipeline.ipynb) |

### Rationale for Critical Decisions

Several judgment calls shaped the dataset and are important to document:

**Choice of Harris County as geographic scope:** The EPA AQS API does not filter
by city name — it requires a state and county FIPS code. Harris County (FIPS 48-201)
is the smallest unit that captures all Houston monitoring stations and is effectively
synonymous with the Houston metro area for this analysis.

**Choice of 2021–2023 as date range:** 2020 was excluded because COVID-19 lockdowns
suppressed vehicle and industrial emissions to abnormal levels, which would bias
mean AQI values downward for high-traffic corridors. Three years (2021–2023) provides
enough readings per station for stable ZIP-level averages while keeping the data
temporally relevant.

**Choice of ZIP code as geographic unit:** ZIP codes are the finest level at which
both EPA monitoring data and Census income data are reliably joinable without
additional geospatial modeling. The limitation is that a single ZIP may span several
distinct neighborhoods with different pollution exposures.

**Manual station-to-ZIP mapping:** EPA stations report by GPS coordinates, not ZIP
codes. We manually mapped each Harris County station to its verified ZCTA using EPA
AQS station metadata cross-referenced with Google Maps. This introduces uncertainty
for stations near ZIP boundaries but is the only practical approach given the data.

**Pollutant-level analysis instead of combined AQI:** Aggregating PM2.5, Ozone, and
NO₂ into a single mean AQI masks their different spatial distributions. Ozone is a
secondary pollutant that drifts downwind; NO₂ is a direct emission that stays near
its source. Separating them reveals the true environmental justice signal that a
combined AQI would hide.

### Bias Identification

**Monitoring station placement bias:** EPA monitoring stations are not evenly
distributed across Houston ZIP codes. All five Harris County stations are in areas
with reliable power and land access, not necessarily in the highest-pollution zones.
Wealthier neighborhoods may have more stations, meaning air quality in low-income
areas is underrepresented and potentially underestimated.

**ACS survey sampling bias:** Census ACS estimates are based on survey samples, not
full counts. Lower-response communities — often low-income, non-English speaking,
or immigrant communities — may have noisier income estimates with higher margins
of error.

**COVID-19 temporal bias:** Even excluding 2020, residual behavioral changes in 2021
(reduced commuting, partial industrial slowdown) may have suppressed normal emission
levels, slightly underestimating typical AQI in high-traffic corridors.

**Pollutant selection bias:** We include PM2.5, Ozone, and NO₂ but not CO, SO₂, or
hazardous air pollutants (HAPs). Industrial facilities near the Ship Channel emit
compounds beyond these three, so our analysis understates the full pollution burden
on adjacent low-income communities.

### Bias Mitigation

ZIP codes with fewer than 30 daily AQI readings are flagged as low-confidence and
excluded from the regression models — this prevents unreliable ZIP-level means from
distorting the analysis. Census margin of error values are retained in the database
and used to flag ZIP codes where the income estimate is statistically uncertain
(MOE > 10% of the income estimate); these are also excluded from regression. The
station-to-ZIP mapping is documented explicitly in the pipeline code so it can be
reviewed, corrected, or replaced with a geospatial join if higher-precision data
becomes available. All bias sources and their likely direction of effect are
documented here so readers can assess the robustness of the findings.

---

## Metadata

### Implicit Schema Guidelines

#### `aqi_readings` Collection

All documents must contain the following fields with the specified types:

| Field | Type | Required |
|-------|------|----------|
| `date_local` | string (YYYY-MM-DD) | Yes |
| `parameter` | string | Yes |
| `parameter_code` | string | Yes |
| `aqi` | int or null | Yes |
| `arithmetic_mean` | float | Yes |
| `first_max_value` | float | Yes |
| `local_site_name` | string | Yes |
| `latitude` | float | Yes |
| `longitude` | float | Yes |
| `site_num` | string | Yes |
| `county` | string | Yes |
| `state` | string | Yes |

#### `income_by_zip` Collection

All documents must contain the following fields with the specified types:

| Field | Type | Required |
|-------|------|----------|
| `zip_code` | string | Yes |
| `median_income` | int | Yes |
| `moe` | int or null | Yes |
| `population` | int | Yes |
| `high_moe_flag` | bool | Yes |
| `year` | int | Yes |
| `fetched_at` | string (ISO datetime) | Yes |

**Naming conventions:** All field names use `snake_case` throughout — no camelCase
or mixed conventions permitted. Optional fields must use the same agreed-upon name
across all documents if present. No new field names may be added without updating
these guidelines.

### Data Summary

| Collection | Documents | Date Range | Geographic Scope | Source |
|------------|-----------|------------|-----------------|--------|
| `aqi_readings` | 134,889 | 2021–2023 | Harris County, TX (5 stations) | EPA AQS API |
| `income_by_zip` | 96 | 2022 (ACS 5-yr) | Houston ZCTAs (770xx) | US Census ACS |

### Data Dictionary

| Field | Collection | Data Type | Description | Example |
|-------|------------|-----------|-------------|---------|
| `aqi` | aqi_readings | int | Air Quality Index value (0–500); higher = more polluted | 73 |
| `date_local` | aqi_readings | string | Date of AQI reading (YYYY-MM-DD) | "2023-01-15" |
| `parameter` | aqi_readings | string | Full pollutant name as returned by EPA | "PM2.5 - Local Conditions" |
| `parameter_code` | aqi_readings | string | EPA numeric parameter code | "88101" |
| `arithmetic_mean` | aqi_readings | float | Mean pollutant concentration for the day | 20.9 |
| `first_max_value` | aqi_readings | float | Highest single hourly reading of the day | 38.2 |
| `units_of_measure` | aqi_readings | string | Physical unit for arithmetic_mean | "Micrograms/cubic meter" |
| `local_site_name` | aqi_readings | string | Name of the EPA monitoring station | "Clinton" |
| `latitude` | aqi_readings | float | Monitoring station latitude (WGS84 decimal degrees) | 29.733737 |
| `longitude` | aqi_readings | float | Monitoring station longitude (WGS84 decimal degrees) | -95.257605 |
| `site_num` | aqi_readings | string | EPA site identifier number | "0034" |
| `county` | aqi_readings | string | County name | "Harris" |
| `state` | aqi_readings | string | State name | "Texas" |
| `zip_code` | income_by_zip | string | Houston ZIP code (ZCTA 5-digit) | "77020" |
| `median_income` | income_by_zip | int | Median household income in USD | 46606 |
| `moe` | income_by_zip | int or null | Census margin of error for the income estimate in USD | 3200 |
| `population` | income_by_zip | int | Total ZCTA population from ACS estimate | 14022 |
| `high_moe_flag` | income_by_zip | bool | True if MOE exceeds 10% of median income — statistically uncertain estimate | false |
| `year` | income_by_zip | int | ACS 5-year estimates reference year | 2022 |
| `fetched_at` | income_by_zip | string | UTC timestamp when the record was inserted | "2024-01-15T10:23:41" |

### Feature Uncertainty Quantification

| Feature | Uncertainty Source | How Quantified |
|---------|-------------------|----------------|
| `aqi` | Sensor calibration drift; sparse station coverage means some ZIP codes have no nearby monitor | Report mean and std per ZIP; flag ZIPs with fewer than 30 readings as low-confidence and exclude from models |
| `arithmetic_mean` | Single daily average may miss intra-day pollution spikes, especially near industrial facilities | Compare against `first_max_value`; large gaps indicate high-variance days where the mean understates peak exposure |
| `latitude` / `longitude` | Station GPS coordinates are precise; the manual ZIP boundary assignment introduces approximately 1 km ambiguity | Documented and accepted; could be improved with a geospatial ZCTA polygon join |
| `median_income` | ACS is a sample survey; response rates vary by community type, particularly for low-income and immigrant households | Use `moe` field; flag and exclude ZIPs where `moe > 0.10 × median_income` |
| `moe` | Derived from ACS sampling design — reliable for the reference year but not updated annually | Retained as-is from Census API; note that 2022 estimates are used for 2021–2023 AQI comparisons |
| `aqi` (temporal) | Residual COVID-19 behavioral changes in 2021 may suppress emission levels below long-run norms | Compare 2021 vs. 2022–2023 annual means per station; flag stations with >10% inter-year AQI variance |

---

## Repository Structure

```
ds4320-project2/
├── README.md                        ← This file — all project documentation
├── LICENSE                          ← MIT License
├── requirements.txt                 ← Python dependencies
├── .gitignore                       ← Excludes credentials, logs, checkpoints
├── data/
│   ├── fetch_aqi.py                 ← EPA AQS data ingestion script
│   └── fetch_income.py              ← Census ACS income ingestion script
├── pipeline/
│   ├── pipeline.ipynb               ← Full analysis + visualization notebook (File 1)
│   └── pipeline.md                  ← Notebook exported as markdown (File 2)
└── docs/
    ├── press_release.md             ← Press release (separate markdown file)
    └── houston_aqi_by_pollutant.png ← Publication-quality figure (300 DPI)
```

> **MongoDB credentials** for grader access via mongosh are posted in the Canvas
> assignment comment — they are not stored in this repository.

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ds4320-project2.git
cd ds4320-project2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your credentials to the data scripts
#    In fetch_aqi.py:    replace PASSWORD and YOUR_EPA_KEY
#    In fetch_income.py: replace PASSWORD and YOUR_CENSUS_KEY

# 4. Pull data into MongoDB (run once — data is already loaded for graders)
python data/fetch_aqi.py
python data/fetch_income.py

# 5. Open and run the analysis pipeline
jupyter notebook pipeline/pipeline.ipynb
```
