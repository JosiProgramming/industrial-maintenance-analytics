from pathlib import Path
import sqlite3
import pandas as pd


# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXCEL_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "industrial_maintenance_data.xlsx"
)

DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "maintenance.db"
)


# Create database directory if it does not exist
DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# Load Excel data
equipment = pd.read_excel(
    EXCEL_PATH,
    sheet_name="equipment_master"
)

maintenance = pd.read_excel(
    EXCEL_PATH,
    sheet_name="maintenance_orders"
)

operating = pd.read_excel(
    EXCEL_PATH,
    sheet_name="operating_history"
)


# Connect to SQLite database
connection = sqlite3.connect(DATABASE_PATH)


# Write DataFrames to SQL tables
equipment.to_sql(
    "equipment",
    connection,
    if_exists="replace",
    index=False
)

maintenance.to_sql(
    "maintenance_orders",
    connection,
    if_exists="replace",
    index=False
)

operating.to_sql(
    "operating_history",
    connection,
    if_exists="replace",
    index=False
)


print("Tables created successfully.")


# Check tables
tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
    """,
    connection
)

print("\n--- Database Tables ---")
print(tables.to_string(index=False))


connection.close()

print("\nDatabase connection closed.")