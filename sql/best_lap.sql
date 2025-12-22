SELECT
    race.year,
    race_result.position_text AS position,
    fastest_lap.driver_number,
    fastest_lap.driver_id,
    fastest_lap.constructor_id,
    fastest_lap.engine_manufacturer_id,
    fastest_lap.tyre_manufacturer_id,
    fastest_lap.fastest_lap_lap AS lap,
    fastest_lap.fastest_lap_time AS time,
    fastest_lap.fastest_lap_time_millis AS time_ms
FROM 
    race_data fastest_lap
JOIN
    race ON fastest_lap.race_id = race.id
LEFT JOIN 
    race_data race_result ON race_result.race_id = fastest_lap.race_id
    AND race_result.driver_id = fastest_lap.driver_id
    AND race_result.type = 'RACE_RESULT'
WHERE 
    fastest_lap.type = 'FASTEST_LAP' 
    AND race.circuit_id = ?
ORDER BY 
    fastest_lap.fastest_lap_time ASC;