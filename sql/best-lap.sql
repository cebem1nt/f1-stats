SELECT
    ROW_NUMBER() OVER 
        (ORDER BY fastest_lap.fastest_lap_time ASC) as '',
    race.year,
    driver.name as driver,
    race_result.position_text as finish,
    fastest_lap.fastest_lap_lap as lap,
    fastest_lap.fastest_lap_time as time,
    fastest_lap.tyre_manufacturer_id as tyre,
    fastest_lap.engine_manufacturer_id as engine,
    fastest_lap.constructor_id as constructor

FROM 
    race_data fastest_lap
JOIN
    race ON fastest_lap.race_id = race.id
JOIN
    driver on driver.id = fastest_lap.driver_id
LEFT JOIN 
    race_data race_result ON race_result.race_id = fastest_lap.race_id
    AND race_result.driver_id = fastest_lap.driver_id
    AND race_result.type = 'RACE_RESULT'
WHERE 
    fastest_lap.type = 'FASTEST_LAP' 
    AND race.circuit_id = ?