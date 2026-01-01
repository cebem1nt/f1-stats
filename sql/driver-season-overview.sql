SELECT
    r.grand_prix_id,
    rd.race_fastest_lap,
    rd.race_pole_position,
    q.qualifying_q3_millis,
    rd.race_grid_position_number,
    rd.position_number,
    rd.race_positions_gained,
    rd.race_gap_millis,
    rd.race_laps,
    rd.race_time_penalty,
    rds.points,
    rd.race_points,
    rds.position_number
FROM 
    race_data rd
JOIN 
    race r on r.id = rd.race_id
JOIN
    constructor c on c.id = rd.constructor_id
JOIN
    grand_prix gp on gp.id = r.grand_prix_id
LEFT JOIN
    race_data q on q.race_id = rd.race_id and
    q.driver_id = :id and
    q.type = 'QUALIFYING_RESULT'
LEFT JOIN
    race_driver_standing rds on rds.race_id = r.id
    and rds.driver_id = :id
WHERE 
    rd.driver_id = :id and 
    rd.type = 'RACE_RESULT' and 
    r.year = :year