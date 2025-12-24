SELECT 
    race.circuit_id as circuit,
    race.circuit_type,
    race_driver_standing.points as points,
    race_driver_standing.position_number as points_pos,
    race_driver_standing.positions_gained as points_pos_gained,
    race_data.race_laps as laps,
    race_data.race_grid_position_text as grid_pos,
    race_data.race_positions_gained as pos_gained,
    race_data.position_text as finish,
    race_data.race_reason_retired as reason_retired,
    race_data.race_gap as gap,
    race_data.race_fastest_lap as fastest_lap,
    race_data.constructor_id as constructor
FROM 
    race_data
JOIN 
    race ON race.id = race_data.race_id
LEFT JOIN
    race_driver_standing ON race_driver_standing.race_id = race.id
    AND race_driver_standing.driver_id = ?
WHERE 
    race_data.driver_id = ?
    AND race_data.type = 'RACE_RESULT'
    AND race.year = ?