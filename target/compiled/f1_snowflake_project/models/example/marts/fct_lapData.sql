SELECT
driver,
COUNT(*) AS number_of_laps,
AVG(position) AS average_position,
MIN(laptime) as best_lap,
FROM f1_db.raw.stg_laps
GROUP BY driver