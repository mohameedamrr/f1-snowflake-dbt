SELECT
  driver,
  try_to_time(laptime) as laptime,
  lapnumber,
  team,
  position
FROM {{ source('raw_data', 'laps') }}