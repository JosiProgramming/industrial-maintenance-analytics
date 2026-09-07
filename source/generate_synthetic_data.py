from pathlib import Path
import pandas as pd
import numpy as np
import random 

# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILE_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "industrial_maintenance_data.xlsx"
)

# Reproducibility
SEED = 42

random.seed(SEED)
np.random.seed(SEED)

# Load equipment master data
equipment = pd.read_excel(
    FILE_PATH,
    sheet_name="equipment_master"
)

print("Equipment master loaded successfully.")
print(f"Number of equipment: {len(equipment)}")

# Reliability profile by criticality
reliability_profiles = {
    "High": {
        "monthly_failure_rate": 2.5,
        "downtime_range": (2.0, 12.0)
    },
    "Medium": {
        "monthly_failure_rate": 1.5,
        "downtime_range": (1.0, 8.0)
    },
    "Low": {
        "monthly_failure_rate": 0.8,
        "downtime_range": (0.5, 4.0)
    }
}

print("\n--- Equipment Reliability Profiles ---")

for _, row in equipment.iterrows():
    equipment_id = row["equipment_id"]
    criticality = row["criticality"]

    profile = reliability_profiles[criticality]

    print(
        f"{equipment_id} | "
        f"Criticality: {criticality} | "
        f"Failure rate: {profile['monthly_failure_rate']} | "
        f"Downtime range: {profile['downtime_range']}"
    )

    # Failure categories by equipment type
failure_profiles = {
    "Hydraulic Press": {
        "Hydraulic": 0.40,
        "Mechanical": 0.30,
        "Electrical": 0.20,
        "Lubrication": 0.10
    },

    "Mechanical Press": {
        "Mechanical": 0.45,
        "Lubrication": 0.25,
        "Electrical": 0.20,
        "Other": 0.10
    },

    "CNC Machine": {
    "Electrical": 0.30,
    "Mechanical": 0.25,
    "Automation": 0.25,
    "Lubrication": 0.20
},

    "CNC Lathe": {
    "Mechanical": 0.30,
    "Electrical": 0.30,
    "Automation": 0.25,
    "Lubrication": 0.15
},

    "Assembly Line": {
        "Automation": 0.40,
        "Electrical": 0.30,
        "Mechanical": 0.20,
        "Other": 0.10
    },

   "Screw Compressor": {
    "Mechanical": 0.35,
    "Electrical": 0.20,
    "Lubrication": 0.30,
    "Other": 0.15
}
}

print("\n--- Failure Profile Test ---")

for _, row in equipment.iterrows():
    equipment_id = row["equipment_id"]
    equipment_type = row["equipment_type"]

    if equipment_type in failure_profiles:
        categories = failure_profiles[equipment_type]

        selected_failure = random.choices(
            population=list(categories.keys()),
            weights=list(categories.values()),
            k=1
        )[0]

        print(
            f"{equipment_id} | "
            f"{equipment_type} | "
            f"Selected failure: {selected_failure}"
        )

    else:
        print(
            f"{equipment_id} | "
            f"{equipment_type} | "
            f"No failure profile found"
        )

        # Generate synthetic corrective maintenance orders

maintenance_orders = []

work_order_counter = 1

for _, row in equipment.iterrows():

    equipment_id = row["equipment_id"]
    equipment_type = row["equipment_type"]
    criticality = row["criticality"]

    profile = reliability_profiles[criticality]
    failure_profile = failure_profiles[equipment_type]

    # Generate failures for each month of 2026
    for month in range(1, 13):

        number_of_failures = np.random.poisson(
            profile["monthly_failure_rate"]
        )

        for _ in range(number_of_failures):

            # Select failure category
            failure_category = random.choices(
                population=list(failure_profile.keys()),
                weights=list(failure_profile.values()),
                k=1
            )[0]

            # Generate random opening date
            start_of_month = pd.Timestamp(
                year=2026,
                month=month,
                day=1
            )

            end_of_month = start_of_month + pd.offsets.MonthEnd(0)

            random_day = random.randint(
                0,
                (end_of_month - start_of_month).days
            )

            opening_datetime = (
                start_of_month
                + pd.Timedelta(days=random_day)
                + pd.Timedelta(
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
            )

            # Generate downtime
            downtime_min, downtime_max = profile["downtime_range"]

            downtime_hours = round(
                random.uniform(downtime_min, downtime_max),
                2
            )

            closing_datetime = (
                opening_datetime
                + pd.Timedelta(hours=downtime_hours)
            )

            # Labor
            labor_hours = round(
                downtime_hours * random.uniform(0.8, 1.8),
                2
            )

            hourly_rate = random.uniform(55, 95)

            labor_cost = round(
                labor_hours * hourly_rate,
                2
            )

            # Material cost
            material_cost = round(
                random.uniform(50, 2500),
                2
            )

            total_cost = round(
                labor_cost + material_cost,
                2
            )

            # Priority based on criticality
            if criticality == "High":
                priority = random.choices(
                    ["High", "Medium", "Low"],
                    weights=[0.70, 0.25, 0.05],
                    k=1
                )[0]
            else:
                priority = random.choices(
                    ["High", "Medium", "Low"],
                    weights=[0.20, 0.60, 0.20],
                    k=1
                )[0]

            maintenance_orders.append({
                "work_order_id": f"WO{work_order_counter:05d}",
                "equipment_id": equipment_id,
                "opening_datetime": opening_datetime,
                "closing_datetime": closing_datetime,
                "maintenance_type": "Corrective",
                "failure_category": failure_category,
                "failure_description": f"{failure_category} failure",
                "downtime_hours": downtime_hours,
                "labor_hours": labor_hours,
                "labor_cost": labor_cost,
                "material_cost": material_cost,
                "total_cost": total_cost,
                "status": "Closed",
                "priority": priority
            })

            work_order_counter += 1

maintenance_df = pd.DataFrame(maintenance_orders)

print("\n--- Synthetic Maintenance Orders ---")

print(f"Total work orders generated: {len(maintenance_df)}")

print("\nFirst 10 work orders:")
print(maintenance_df.head(10))

print("\n--- Work Orders by Equipment ---")
print(
    maintenance_df["equipment_id"]
    .value_counts()
    .sort_index()
)

print("\n--- Failures by Category ---")
print(
    maintenance_df["failure_category"]
    .value_counts()
)

print("\n--- Priority Distribution ---")
print(
    maintenance_df["priority"]
    .value_counts()
)

print("\n--- Maintenance Summary ---")
print(
    maintenance_df[
        [
            "downtime_hours",
            "labor_hours",
            "labor_cost",
            "material_cost",
            "total_cost"
        ]
    ].describe()
)

    # Generate monthly operating history

operating_history = []

record_counter = 1

for _, row in equipment.iterrows():

    equipment_id = row["equipment_id"]
    nominal_hours_day = row["nominal_hours_day"]

    for month in range(1, 13):

        # Number of days in the month
        days_in_month = pd.Period(
            year=2026,
            month=month,
            freq="M"
        ).days_in_month

        # Simplified planned operating time
        planned_hours = nominal_hours_day * days_in_month

        # Downtime generated from corrective maintenance orders
        monthly_orders = maintenance_df[
            (maintenance_df["equipment_id"] == equipment_id)
            & (maintenance_df["opening_datetime"].dt.month == month)
        ]

        downtime_hours = round(
            monthly_orders["downtime_hours"].sum(),
            2
        )

        # Actual operating hours
        operating_hours = round(
            max(planned_hours - downtime_hours, 0),
            2
        )

        # Calendar hours
        calendar_hours = days_in_month * 24

        operating_history.append({
            "record_id": f"OP{record_counter:04d}",
            "equipment_id": equipment_id,
            "year": 2026,
            "month": month,
            "calendar_hours": calendar_hours,
            "planned_hours": planned_hours,
            "downtime_hours": downtime_hours,
            "operating_hours": operating_hours
        })

        record_counter += 1


operating_df = pd.DataFrame(operating_history)

print("\n--- Operating History ---")
print(f"Total records generated: {len(operating_df)}")

print("\nFirst 12 records:")
print(operating_df.head(12))

# Save generated data to Excel
with pd.ExcelWriter(
    FILE_PATH,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:

    maintenance_df.to_excel(
        writer,
        sheet_name="maintenance_orders",
        index=False
    )

    operating_df.to_excel(
        writer,
        sheet_name="operating_history",
        index=False
    )

print("\nMaintenance orders and operating history saved successfully.")

print("\nMaintenance orders saved successfully.")
