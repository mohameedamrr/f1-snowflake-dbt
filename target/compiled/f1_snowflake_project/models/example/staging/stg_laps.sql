SELECT
  driver,
  try_to_time(laptime) as laptime,
  lapnumber,
  team,
  position
FROM f1_db.raw.laps