# Industrial Maintenance Analytics

End-to-end data analytics project focused on **industrial maintenance, equipment reliability, and asset risk analysis**.

The project simulates an industrial maintenance environment and demonstrates a complete analytics workflow using **Python, SQL, SQLite, Power BI, and DAX**.

## Project Overview

Industrial maintenance generates large volumes of operational and maintenance data. This project explores how these data can be transformed into actionable information for reliability and maintenance decision-making.

The analysis focuses on:

- Equipment availability
- Failure frequency
- Maintenance downtime
- Maintenance costs
- MTBF (Mean Time Between Failures)
- MTTR (Mean Time To Repair)
- Asset risk prioritization

## Technologies

| Technology | Application |
|---|---|
| Python | Data generation, validation, transformation and KPI calculation |
| Pandas | Data manipulation and aggregation |
| NumPy | Synthetic failure generation |
| Excel | Raw industrial dataset |
| SQLite | Relational maintenance database |
| SQL | Maintenance and reliability analysis |
| Power BI | Data modeling and dashboard development |
| DAX | Interactive maintenance KPIs |
| Git / GitHub | Version control and project documentation |

## Asset Risk Score

A custom analytical **Asset Risk Score** was developed to prioritize equipment requiring greater maintenance attention.

The score combines:

- Corrective downtime — 25%
- Failure frequency — 20%
- Availability — 20%
- MTBF — 15%
- MTTR — 10%
- Maintenance cost — 10%

Each component is normalized to a 0–100 scale before weighting.

> The weighting model is a project-defined analytical methodology and is not intended to represent a universal maintenance standard.


## Power BI Dashboard

The Power BI report is divided into three analytical views.

### Maintenance Overview

Provides an executive overview of maintenance performance, including failures, downtime, maintenance costs and availability.

![Maintenance Overview](dashboard/screenshots/maintenance_overview.jpg)

### Equipment Reliability

Focuses on equipment reliability through MTBF, MTTR, failure categories and monthly downtime behavior.

![Equipment Reliability](dashboard/screenshots/equipment_reliability.jpg)

### Asset Risk Analysis

Prioritizes industrial assets according to their calculated risk score and supporting reliability indicators.

![Asset Risk Analysis](dashboard/screenshots/asset_risk_analysis.jpg)


## Dataset

The synthetic industrial environment contains:

- **10 industrial assets**
- **253 corrective maintenance work orders**
- **120 monthly operating records**
- Equipment criticality classification
- Failure categories
- Labor and material maintenance costs
- Equipment operating and downtime hours

## Author

**Joseane Oliveira**

Industrial Data & Maintenance Analytics# industrial-maintenance-analytics
Maintenance data analysis project focused on reliability, downtime, costs and maintenance KPIs.
