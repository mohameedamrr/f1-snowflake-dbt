SELECT
driver,
COUNT(*) AS number_of_laps,
AVG(position) AS average_position,
MIN(laptime) as best_lap,
FROM {{ref ("stg_laps")}}
GROUP BY driver
