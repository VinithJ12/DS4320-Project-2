DS 4320 Project 2: Breathing Inequality — Houston Air Quality vs. Neighborhood Income
Name: Vinith J
NetID: jvinith2
DOI: 10.5281/zenodo.XXXXXXX ← replace after creating on Zenodo
Press Release: docs/press_release.md
Pipeline: pipeline/pipeline.ipynb
License: MIT — see LICENSE

Executive Summary
This project investigates environmental justice in Houston, TX by asking whether
low-income neighborhoods experience measurably worse air quality than higher-income
neighborhoods. Five years of daily AQI readings (2020–2024) from EPA monitoring
stations in Harris County are joined with US Census median household income data
at the ZIP code level inside a MongoDB Atlas document database. A Python-based
analysis pipeline queries the database, aggregates air quality to the ZIP-code
level, and applies linear regression and Random Forest models to test whether
income predicts AQI. The results confirm a statistically significant negative
relationship: as neighborhood income increases, AQI decreases. The lowest-income
ZIP codes — clustered around the Houston Ship Channel industrial corridor — bear
a disproportionate share of Houston's air pollution burden.

Problem Definition
General Problem
Predicting air quality.
Specific Problem Statement
Do low-income neighborhoods in Houston, TX experience worse air quality (measured
by AQI) than higher-income neighborhoods, and can neighborhood median household
income predict daily AQI readings at the ZIP code level?
Motivation
Air pollution is not distributed equally. In cities like Houston — home to one
of the largest petrochemical complexes in the world — industrial facilities,
highways, and refineries are concentrated in specific neighborhoods. Research
consistently shows these neighborhoods are more likely to be low-income and
majority-minority communities. Understanding whether income level predicts air
quality in Houston is important because it directly affects public health policy,
zoning decisions, and environmental justice advocacy. If low-income ZIP codes
consistently show higher AQI readings, that is evidence of a systemic problem
requiring targeted intervention — not just city-wide air quality improvements.
The residents of the Houston Ship Channel corridor face daily exposure to
pollutants that contribute to elevated rates of respiratory disease, asthma
hospitalization, and cardiovascular mortality. Documenting this pattern
rigorously is a prerequisite to addressing it.
Refinement Rationale
The general problem of "predicting air quality" is too broad to be actionable —
it could mean anything from global climate modeling to next-hour forecasts. We
refined it to Houston specifically because Houston has some of the worst air
quality in the US and extreme income inequality across its neighborhoods, making
it an ideal city to detect an environmental justice signal. We further refined
the outcome to AQI (rather than a specific pollutant) because AQI is the
standard public-facing measure that directly determines health advisories and
behavior — it is what matters most to residents. The income angle transforms a
pure forecasting problem into an equity analysis with real policy implications,
connecting data science to one of the most pressing issues in urban public
health. The ZIP code geographic unit was chosen because it is the finest level
at which both EPA monitoring data and Census income data are reliably joinable
without additional geospatial interpolation.
Press Release
Breathing Inequality: Houston's Poorest Neighborhoods Choke on the Worst Air

Domain Exposition
Terminology
TermDefinitionAQIAir Quality Index — a 0–500 scale where higher values indicate more pollution; above 100 is "Unhealthy for Sensitive Groups"PM2.5Fine particulate matter under 2.5 microns in diameter — most dangerous to lungs and cardiovascular systemOzone (O₃)Ground-level ozone formed by vehicle and industrial emissions reacting with sunlightEPAUS Environmental Protection Agency — collects and publishes air quality data via the AQS networkAQSEPA Air Quality System — the national network of monitoring stations and the API providing their dataZCTAZIP Code Tabulation Area — Census geographic unit approximating postal ZIP codes, used to join AQI and income dataMedian household incomeCensus measure of the midpoint income in a geographic area; used as a proxy for neighborhood wealthEnvironmental justiceThe principle that all people deserve equal protection from environmental harms regardless of race or incomeNO₂Nitrogen dioxide — a pollutant emitted by vehicles and power plants; indicator of traffic and industrial activityMOEMargin of Error — the Census uncertainty estimate for ACS survey-based statisticsACSAmerican Community Survey — the Census Bureau's annual survey providing demographic and income data by geographyHarris CountyThe Texas county encompassing Houston; used as the geographic scope for EPA data pulls
Domain Paragraph
This project lives at the intersection of environmental science and public health
equity. Houston, TX is the fourth-largest city in the United States and sits in
the Houston-Galveston-Brazoria region, which has repeatedly violated EPA ozone
standards for decades. The city's east side is home to the Houston Ship Channel,
one of the most industrially dense corridors in North America, surrounded by
low-income and minority neighborhoods that have historically borne the burden of
petrochemical production. Air quality data is collected by the EPA through a
network of fixed monitoring stations and made publicly available through the AQS
API. Census income data is available at the ZIP code level through the American
Community Survey (ACS) 5-year estimates, which pool five years of survey
responses for statistical reliability at small geographies. By storing both
datasets in MongoDB and analyzing AQI readings across income brackets, we can
quantify exactly how much worse air quality is in low-income neighborhoods and
test whether that relationship is statistically significant — providing the
evidentiary foundation for targeted environmental policy.
Background Reading
Background readings are stored in the project's OneDrive folder:
Background Readings Folder
TitleDescriptionLinkEPA AQS Data DocumentationOfficial documentation for the EPA air quality API and data formataqs.epa.govCDC — Air Quality and HealthOverview of how AQI levels affect human health across exposure rangescdc.govHouston Air Quality HistoryHouston Chronicle reporting on Houston's decades-long air quality challengeshoustonchronicle.comEnvironmental Justice in HoustonAcademic overview of environmental inequity in Houston's east-side communitiessesync.orgUS Census ACS DocumentationHow to access and interpret median household income by ZIP code from the ACScensus.gov

Data Creation
Data Acquisition Provenance
Air quality data was obtained from the EPA Air Quality System (AQS) API
(aqs.epa.gov), a publicly available government database containing daily AQI
readings collected from monitoring stations across the United States. For this
project, data was filtered to Houston, TX (Harris County, FIPS 48-201) and
pulled for the years 2020–2024, covering three key pollutants: PM2.5
(parameter code 88101), Ozone (44201), and NO₂ (42602). Each record represents
one daily AQI reading at a specific monitoring station, identified by GPS
coordinates and a site number. The EPA API requires a registered email and API
key, both of which are stored in the script configuration rather than hardcoded
in shared code.
Income data was obtained from the US Census Bureau's American Community Survey
(ACS) 5-year estimates for reference year 2022, accessed via the Census Data API
(api.census.gov). This dataset provides median household income (variable
B19013_001E) and its margin of error (B19013_001M) at the ZIP Code Tabulation
Area (ZCTA) level. The pull was filtered to Houston ZCTAs (those beginning with
"770") and ZIP codes where income was not suppressed by the Census (suppressed
values are indicated by the sentinel -666666666). Both datasets were pulled using
Python scripts and loaded into MongoDB Atlas, then joined on ZIP code in the
analysis pipeline to enable neighborhood-level comparison of income vs. air quality.
Source Code
FileDescriptionLinkdata/fetch_aqi.pyPulls daily PM2.5, Ozone, and NO₂ AQI readings for Harris County TX from the EPA AQS API (2020–2024) and loads them into MongoDBdata/fetch_aqi.pydata/fetch_income.pyPulls median household income by ZIP code from the Census ACS API and filters to Houston ZCTAsdata/fetch_income.pypipeline/pipeline.ipynbFull analysis and visualization pipelinepipeline/pipeline.ipynb
Rationale for Critical Decisions
Several judgment calls shape the dataset and introduce or mitigate uncertainty:
Choice of AQI as outcome: AQI integrates multiple pollutants into a single
public health–oriented scale that drives health advisories. It is more directly
policy-relevant than raw concentration values. The tradeoff is that AQI hides
which specific pollutant is driving a high reading, which matters for source
attribution.
Choice of ZIP code as geographic unit: ZIP codes are the finest level at
which both EPA and Census data are reliably joinable without additional
geospatial modeling. The limitation is that ZCTAs are large — a single 770xx ZIP
may span several distinct neighborhoods with very different pollution exposures.
Manual station-to-ZIP mapping: EPA monitoring stations report by GPS
coordinates, not ZIP codes. We manually mapped each Harris County station to its
approximate ZCTA using known station addresses. This introduces uncertainty for
stations near ZIP boundaries but is the only practical approach given the data.
Date range 2020–2024: Five years provides enough data to compute stable
per-ZIP averages. The 2020 COVID lockdown period depressed traffic-related
emissions, which may slightly understate the "normal" AQI for high-traffic
corridors. This uncertainty is documented but not corrected.
Bias Identification
Monitoring station placement bias: EPA monitoring stations are not evenly
distributed across Houston ZIP codes. Wealthier neighborhoods tend to have more
stations, meaning air quality in low-income areas may be underrepresented. More
critically, stations may be placed away from the worst pollution sources for
technical reasons (power access, land availability), which could underestimate
AQI in high-pollution areas.
ACS survey sampling bias: Census ACS estimates are based on survey samples,
not full counts. Lower-response communities (often low-income, non-English
speaking, or immigrant communities) may have noisier income estimates. This is
reflected in the margin-of-error (MOE) field.
COVID-19 temporal bias: 2020 AQI readings were recorded during an
unprecedented reduction in vehicle traffic and some industrial activity. Including
2020 data may produce mean AQI values that are lower than the long-run norm.
Pollutant selection bias: We include PM2.5, Ozone, and NO₂ — the three
pollutants most relevant to the Houston context — but not CO, SO₂, or lead.
Industrial facilities near the Ship Channel are known to emit compounds beyond
these three, so our AQI estimates may understate the full health burden.
Bias Mitigation
To mitigate monitoring station placement bias, only ZIP codes with at least one
active EPA monitoring station are included, and ZIP codes with fewer than 30
daily readings are flagged as low-confidence and excluded from the primary
analysis. The Census-provided margin of error values are retained in the dataset
and used to flag ZIP codes where the income estimate is statistically uncertain
(MOE > 10% of the income estimate); these ZIP codes are excluded from the
regression models. The station-to-ZIP mapping is documented explicitly in the
pipeline code so it can be reviewed, corrected, or replaced with a geospatial
join if higher-precision data becomes available.

Metadata
Implicit Schema Guidelines
aqi_readings Collection
All documents must contain these fields:
FieldTypeRequireddate_localstring (YYYY-MM-DD)YesparameterstringYesparameter_codestringYesaqiint or nullYesarithmetic_meanfloatYesfirst_max_valuefloatYeslocal_site_namestringYeslatitudefloatYeslongitudefloatYessite_numstringYescountystringYesstatestringYesfetched_atstring (ISO datetime)Yes
income_by_zip Collection
All documents must contain these fields:
FieldTypeRequiredzip_codestringYesmedian_incomeintYesmoeint or nullYespopulationintYeshigh_moe_flagboolYesyearintYesfetched_atstring (ISO datetime)Yes
Naming conventions: All field names use snake_case. No camelCase or mixed
conventions. Optional fields must use the same agreed-upon name across all
documents if present. No new field names may be added without updating this schema.
Data Summary
CollectionDocumentsDate RangeGeographic ScopeSourceaqi_readings33,930+2020–2024Harris County, TXEPA AQS APIincome_by_zip962022 (ACS)Houston ZCTAs (770xx)US Census ACS
Data Dictionary
FieldCollectionData TypeDescriptionExampleaqiaqi_readingsintAir Quality Index value (0–500); higher = more polluted73date_localaqi_readingsstringDate of AQI reading (YYYY-MM-DD)"2023-01-15"parameteraqi_readingsstringPollutant measured"PM2.5 - Local Conditions"parameter_codeaqi_readingsstringEPA numeric code for the pollutant"88101"arithmetic_meanaqi_readingsfloatMean pollutant concentration for the day20.9first_max_valueaqi_readingsfloatHighest single hourly reading of the day38.2units_of_measureaqi_readingsstringPhysical unit for arithmetic_mean"Micrograms/cubic meter"local_site_nameaqi_readingsstringName of the EPA monitoring station"Clinton"latitudeaqi_readingsfloatMonitoring station latitude (WGS84)29.733737longitudeaqi_readingsfloatMonitoring station longitude (WGS84)-95.257605site_numaqi_readingsstringEPA site identifier number"0034"countyaqi_readingsstringCounty name"Harris"stateaqi_readingsstringState name"Texas"fetched_ataqi_readingsstringUTC timestamp when the record was pulled"2024-01-15T10:23:41"zip_codeincome_by_zipstringHouston ZIP code (ZCTA)"77002"median_incomeincome_by_zipintMedian household income in USD78292moeincome_by_zipint or nullCensus margin of error for income estimate10147populationincome_by_zipintTotal ZCTA population (ACS estimate)14022high_moe_flagincome_by_zipboolTrue if MOE > 10% of median incomefalseyearincome_by_zipintACS survey reference year2022fetched_atincome_by_zipstringUTC timestamp when the record was pulled"2024-01-15T10:23:41"
Feature Uncertainty Quantification
FeatureUncertainty SourceHow QuantifiedaqiSensor calibration error; sparse station coverage per ZIPReport mean and std per ZIP; flag ZIPs with fewer than 30 readings as low-confidencearithmetic_meanSingle daily average may miss intra-day pollution spikesCompare against first_max_value to detect high-variance dayslatitude / longitudeStation GPS is precise; ZIP boundary assignment introduces ≈1 km ambiguityDocumented; not correctedmedian_incomeACS is a sample survey; response rates vary by communityUse moe field; flag ZIPs where moe > 0.10 × median_incomemoeDerived from ACS sampling design; accurate for the survey yearRetained as-is from Census APIaqi (temporal)COVID-19 suppressed 2020 traffic emissionsCompute per-year means alongside 5-year means; compare to detect anomalies

Repository Structure
houston_airquality/
├── README.md                    ← This file
├── LICENSE                      ← MIT License
├── requirements.txt             ← Python dependencies
├── data/
│   ├── fetch_aqi.py             ← EPA AQS data ingestion script
│   └── fetch_income.py          ← Census ACS income ingestion script
├── pipeline/
│   ├── pipeline.ipynb           ← Full analysis + visualization notebook
│   └── pipeline.md              ← Notebook exported as markdown
├── docs/
│   ├── press_release.md         ← Press release (separate markdown file)
│   └── houston_aqi_income_analysis.png  ← Publication-quality figure
└── logs/                        ← Log files (git-ignored)
    ├── fetch_aqi.log
    ├── fetch_income.log
    └── pipeline.log
