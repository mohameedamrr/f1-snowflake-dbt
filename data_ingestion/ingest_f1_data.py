import fastf1
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os
import write_to_snowflake
# load data from dotenv
load_dotenv()

def get_session_info(year, race, session, drivers):

    # Load a session
    session_info = fastf1.get_session(year, race, session)
    session_info.load(telemetry=True)

    #---------- Session Details ----------
    session_data = session_info.event
    session_data_df = pd.DataFrame(
        [
            {
                "OfficialName": session_data.OfficialEventName,
                "EventName": session_data.EventName,
                "Location" : session_data.Location,
                "Date": session_data.EventDate,
                "Year": session_data.year,
                "RoundNumber": session_data.RoundNumber
            }
        ]
    )
    session_data_df["Date"] = session_data_df["Date"].astype(str)


    #Write to Snowflake
    write_to_snowflake.write_to_snowflake_session(session_data_df)
    # print(session_data_df)

    # ---------- Laps Data ----------
    laps = session_info.laps.pick_drivers(drivers)
    df = laps[["Driver", "LapTime", "LapNumber", "Team", "Position"]]

    df["LapTime"] = df["LapTime"].apply(
        lambda x: str(x).split(" ")[-1][:-3] if pd.notnull(x) else None
    )

    #Write to snowflake
    write_to_snowflake.write_to_snowflake_laps(df)

    #---------- PitStops Data ----------
    box_laps = laps.pick_box_laps()
    box_df = box_laps[[ "Driver", "DriverNumber", "LapNumber", "PitInTime", "PitOutTime", "Stint", "Compound"]]
    for col in ["PitInTime", "PitOutTime"]:
        box_df.loc[:, col] = box_df[col].apply(lambda x: str(x) if pd.notnull(x) else None)

    #Write to snowflake
    write_to_snowflake.write_to_snowflake_pitStops(box_df)

    # print(box_df)

    # ---------- Results Data ----------
    results = session_info.results
    results_df = results[["DriverNumber","Abbreviation", "Position", "TeamName", "Points", "Status", "Time"]]
    results_df["Time"] = results_df["Time"].apply(
        lambda x: str(x).split(" ")[-1][:-3] if pd.notnull(x) else None
    )

    #print(results_df)
    
    # Write to snowflake
    write_to_snowflake.write_to_snowflake_results(results_df)


def main():
    # Define parameters
    year = 2024
    race = 'Monza'
    session = 'R'  # Race session
    drivers = ['LEC', 'VER', 'HAM', 'NOR']

    # Call session info function
    get_session_info(year, race, session, drivers)


if __name__ == "__main__":
    main()