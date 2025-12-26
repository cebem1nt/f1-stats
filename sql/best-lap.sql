SELECT
    race.year,
    race_result.position_text as pos,
    fastest_lap.driver_number as num,
    driver.name as driver,
    fastest_lap.constructor_id as constructor,
    fastest_lap.engine_manufacturer_id as engine,
    fastest_lap.tyre_manufacturer_id as tyre,
    fastest_lap.fastest_lap_lap as lap,
    fastest_lap.fastest_lap_time as time,
    fastest_lap.fastest_lap_time_millis as milis 
FROM 
    race_data fastest_lap
JOIN
    race ON fastest_lap.race_id = race.id
LEFT JOIN 
    race_data race_result ON race_result.race_id = fastest_lap.race_id
    AND race_result.driver_id = fastest_lap.driver_id
    AND race_result.type = 'RACE_RESULT'
RIGHT JOIN
    driver on driver.id = fastest_lap.driver_id
WHERE 
    fastest_lap.type = 'FASTEST_LAP' 
    AND race.circuit_id = ?
ORDER BY 
    fastest_lap.fastest_lap_time ASC;