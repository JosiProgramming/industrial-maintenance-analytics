from pathlib import Path
import pandas as pd


# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILE_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "industrial_maintenance_data.xlsx"
)


# Load data
equipment = pd.read_excel(
    FILE_PATH,
    sheet_name="equipment_master"
)

maintenance = pd.read_excel(
    FILE_PATH,
    sheet_name="maintenance_orders"
)

operating = pd.read_excel(
    FILE_PATH,
    sheet_name="operating_history"
)


print("--- Data Loaded ---")
print(f"Equipment: {len(equipment)}")
print(f"Maintenance orders: {len(maintenance)}")
print(f"Operating history records: {len(operating)}")

# Aggregate operating data by equipment
operating_summary = (
    operating
    .groupby("equipment_id")
    .agg(
        planned_hours=("planned_hours", "sum"),
        downtime_hours=("downtime_hours", "sum"),
        operating_hours=("operating_hours", "sum")
    )
    .reset_index()
)


# Calculate Availability
operating_summary["availability"] = (
    operating_summary["operating_hours"]
    / operating_summary["planned_hours"]
)


# Convert to percentage
operating_summary["availability_pct"] = (
    operating_summary["availability"] * 100
).round(2)


print("\n--- Availability by Equipment ---")

print(
    operating_summary[
        [
            "equipment_id",
            "planned_hours",
            "downtime_hours",
            "operating_hours",
            "availability_pct"
        ]
    ]
)

# Aggregate maintenance data by equipment
maintenance_summary = (
    maintenance
    .groupby("equipment_id")
    .agg(
        failure_count=("work_order_id", "count"),
        corrective_downtime=("downtime_hours", "sum"),
        total_maintenance_cost=("total_cost", "sum")
    )
    .reset_index()
)


# Merge operating and maintenance data
kpi_summary = operating_summary.merge(
    maintenance_summary,
    on="equipment_id",
    how="left"
)


# Calculate MTTR
kpi_summary["mttr_hours"] = (
    kpi_summary["corrective_downtime"]
    / kpi_summary["failure_count"]
).round(2)


# Calculate MTBF
kpi_summary["mtbf_hours"] = (
    kpi_summary["operating_hours"]
    / kpi_summary["failure_count"]
).round(2)


# Round maintenance cost
kpi_summary["total_maintenance_cost"] = (
    kpi_summary["total_maintenance_cost"].round(2)
)


print("\n--- Maintenance KPIs by Equipment ---")

print(
    kpi_summary[
        [
            "equipment_id",
            "failure_count",
            "availability_pct",
            "mtbf_hours",
            "mttr_hours",
            "corrective_downtime",
            "total_maintenance_cost"
        ]
    ]
)

# Add equipment information to KPI summary
kpi_summary = equipment[
    [
        "equipment_id",
        "equipment_name",
        "area",
        "equipment_type",
        "criticality"
    ]
].merge(
    kpi_summary,
    on="equipment_id",
    how="left"
)


print("\n--- Final Equipment KPI Summary ---")

print(
    kpi_summary[
        [
            "equipment_id",
            "equipment_name",
            "criticality",
            "failure_count",
            "availability_pct",
            "mtbf_hours",
            "mttr_hours",
            "corrective_downtime",
            "total_maintenance_cost"
        ]
    ].to_string(index=False)
)

print("\n--- Asset Performance Rankings ---")

print("\nTop 3 - Most Failures:")
print(
    kpi_summary.nlargest(3, "failure_count")[
        ["equipment_id", "equipment_name", "failure_count"]
    ].to_string(index=False)
)

print("\nTop 3 - Highest Downtime:")
print(
    kpi_summary.nlargest(3, "corrective_downtime")[
        ["equipment_id", "equipment_name", "corrective_downtime"]
    ].to_string(index=False)
)

print("\nTop 3 - Highest Maintenance Cost:")
print(
    kpi_summary.nlargest(3, "total_maintenance_cost")[
        ["equipment_id", "equipment_name", "total_maintenance_cost"]
    ].to_string(index=False)
)

print("\nTop 3 - Lowest Availability:")
print(
    kpi_summary.nsmallest(3, "availability_pct")[
        ["equipment_id", "equipment_name", "availability_pct"]
    ].to_string(index=False)
)

print("\nTop 3 - Lowest MTBF:")
print(
    kpi_summary.nsmallest(3, "mtbf_hours")[
        ["equipment_id", "equipment_name", "mtbf_hours"]
    ].to_string(index=False)
)
# --------------------------------------------------
# Asset Risk Score
# --------------------------------------------------

def normalize_higher_is_worse(series):
    """
    Normalize values from 0 to 100.
    Higher original values represent higher risk.
    """
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(0, index=series.index)

    return (
        (series - min_value)
        / (max_value - min_value)
        * 100
    )


def normalize_lower_is_worse(series):
    """
    Normalize values from 0 to 100.
    Lower original values represent higher risk.
    """
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(0, index=series.index)

    return (
        (max_value - series)
        / (max_value - min_value)
        * 100
    )

# Normalize KPI risk components

kpi_summary["risk_failures"] = normalize_higher_is_worse(
    kpi_summary["failure_count"]
)

kpi_summary["risk_downtime"] = normalize_higher_is_worse(
    kpi_summary["corrective_downtime"]
)

kpi_summary["risk_cost"] = normalize_higher_is_worse(
    kpi_summary["total_maintenance_cost"]
)

kpi_summary["risk_mttr"] = normalize_higher_is_worse(
    kpi_summary["mttr_hours"]
)

kpi_summary["risk_availability"] = normalize_lower_is_worse(
    kpi_summary["availability_pct"]
)

kpi_summary["risk_mtbf"] = normalize_lower_is_worse(
    kpi_summary["mtbf_hours"]
)

# Calculate weighted Asset Risk Score

kpi_summary["asset_risk_score"] = (
    kpi_summary["risk_downtime"] * 0.25
    + kpi_summary["risk_failures"] * 0.20
    + kpi_summary["risk_availability"] * 0.20
    + kpi_summary["risk_mtbf"] * 0.15
    + kpi_summary["risk_mttr"] * 0.10
    + kpi_summary["risk_cost"] * 0.10
).round(2)

# Create asset risk ranking

risk_ranking = (
    kpi_summary
    .sort_values(
        by="asset_risk_score",
        ascending=False
    )
    .reset_index(drop=True)
)

risk_ranking["risk_rank"] = risk_ranking.index + 1


print("\n--- Asset Risk Ranking ---")

print(
    risk_ranking[
        [
            "risk_rank",
            "equipment_id",
            "equipment_name",
            "criticality",
            "asset_risk_score",
            "failure_count",
            "availability_pct",
            "mtbf_hours",
            "mttr_hours",
            "corrective_downtime",
            "total_maintenance_cost"
        ]
    ].to_string(index=False)
)

# --------------------------------------------------
# Export processed analytical datasets
# --------------------------------------------------

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

PROCESSED_PATH.mkdir(
    parents=True,
    exist_ok=True
)

# Export KPI summary
kpi_summary.to_csv(
    PROCESSED_PATH / "equipment_kpis.csv",
    index=False
)

# Export risk ranking
risk_ranking.to_csv(
    PROCESSED_PATH / "asset_risk_ranking.csv",
    index=False
)

print("\nProcessed datasets exported successfully.")