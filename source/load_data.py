from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILE_PATH = PROJECT_ROOT / "data" / "raw" / "industrial_maintenance_data.xlsx"

print("Looking for file at:")
print(FILE_PATH)

if not FILE_PATH.exists():
    raise FileNotFoundError(f"File not found: {FILE_PATH}")

# Carrega as abas em DataFrames
equipment = pd.read_excel(FILE_PATH, sheet_name="equipment_master")
maintenance = pd.read_excel(FILE_PATH, sheet_name="maintenance_orders")
parameters = pd.read_excel(FILE_PATH, sheet_name="parameters")
operating = pd.read_excel(FILE_PATH, sheet_name="operating_history")

print("\n--- Equipment Master ---")
print(equipment.head())
print(f"Rows: {len(equipment)}")

print("\n--- Maintenance Orders ---")
print(maintenance.head())
print(f"Rows: {len(maintenance)}")

print("\n--- Parameters ---")
print(parameters.head())
print(f"Rows: {len(parameters)}")

print("\n--- Operating History ---")
print(operating.head())
print(f"Rows: {len(operating)}")

print("\n--- Data Quality Checks ---")

print("\nEquipment duplicated IDs:")
print(equipment["equipment_id"].duplicated().sum())

print("\nMaintenance duplicated work orders:")
print(maintenance["work_order_id"].duplicated().sum())

print("\nNull values in Equipment Master:")
print(equipment.isnull().sum())

print("\nNull values in Maintenance Orders:")
print(maintenance.isnull().sum())

invalid_equipment_ids = maintenance[
    ~maintenance["equipment_id"].isin(equipment["equipment_id"])
]

print("\nMaintenance orders with invalid equipment_id:")
print(len(invalid_equipment_ids))