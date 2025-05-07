
  create or replace   view f1_db.raw.stg_laps
  
   as (
    SELECT
  driver,
  try_to_time(laptime) as laptime,
  lapnumber,
  team,
  position
FROM f1_db.raw.laps
  );

