import fastf1
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

# load data from dotenv
load_dotenv()

# Load a session
session = fastf1.get_session(2024, 'Monza', 'R')
session.load()

laps = session.laps
monza_laps = laps.pick_drivers(['LEC', 'NOR', 'VER','PIA', 'HAM', 'SAI'])
df = monza_laps[["Driver", "LapTime", "LapNumber", "Team", "Position"]]

best_leclerc = laps.pick_drivers('LEC').pick_fastest()

# Format: 'HH:MM:SS.sss'
df["LapTime"] = df["LapTime"].apply(
    lambda x: x.strftime('%H:%M:%S.%f')[:-3] if pd.notnull(x) else None
)

# Reset index for cleaner printing
df = df.reset_index(drop=True)

# Print nicely
print(df.to_string(index=False))

print("SNOWFLAKE_ACCOUNT =", os.getenv("SNOWFLAKE_ACCOUNT"))

conn = snowflake.connector.connect(
    user= os.getenv('SNOWFLAKE_USER'),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database= os.getenv("SNOWFLAKE_DATABASE"),
    schema= os.getenv("SNOWFLAKE_SCHEMA")
)


cursor = conn.cursor()

# Use parameterized SQL for safety
cursor.execute("""
    CREATE OR REPLACE TABLE laps (
        Driver STRING,
        LapTime STRING,
        LapNumber INT,
        Team STRING,
        Position INT
    )
""")

# Insert data (example using df from FastF1)
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO laps (Driver, LapTime, LapNumber, Team, Position) VALUES (%s, %s, %s, %s, %s)",
        tuple(row)
    )

cursor.close()
conn.close()