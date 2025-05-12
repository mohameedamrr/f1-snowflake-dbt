import snowflake.connector
from dotenv import load_dotenv
import os

# load data from dotenv
load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )



def write_to_snowflake_laps(df):
    conn = get_connection()
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

def write_to_snowflake_results(results_df):
    conn = get_connection()
    cursor = conn.cursor()
    # Use parameterized SQL for safety
    cursor.execute("""
        CREATE OR REPLACE TABLE results (
            DriverNumber INT,
            Abbreviation STRING,
            Position INT,
            TeamName STRING,
            Points INT,
            Status STRING,
            Time STRING               
        )
    """)


    # Insert data (example using df from FastF1)
    for _, row in results_df.iterrows():
        cursor.execute(
            "INSERT INTO results ( DriverNumber, Abbreviation, Position, TeamName, Points, Status, Time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            tuple(row)
        )

    cursor.close()
    conn.close()

def write_to_snowflake_pitStops(pits_df):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE OR REPLACE TABLE pitStops (
            Driver String,
            DriverNumber INT,
            LapNumber INT,
            PitInTime STRING,
            PitOutTime STRING,
            Stint INT,
            Compound STRING               
        )       

    """)
        # Insert data (example using df from FastF1)
    for _, row in pits_df.iterrows():
        cursor.execute(
            "INSERT INTO pitStops ( Driver, DriverNumber, LapNumber, PitInTime, PitOutTime, Stint, Compound) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            tuple(row)
        )
    cursor.close()
    conn.close()

def write_to_snowflake_session(session_df):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE OR REPLACE TABLE session (
        OfficialName String,
        EventName STRING,           
        Location STRING,
        Date STRING,
        Year INT,
        RoundNumber INT           
    )       

""")
        # Insert data (example using df from FastF1)
    for _, row in session_df.iterrows():
        cursor.execute(
            "INSERT INTO session ( OfficialName,EventName, Location, Date, Year, RoundNumber) VALUES (%s,%s, %s, %s, %s, %s)",
            tuple(row)
        )
    cursor.close()
    conn.close()

