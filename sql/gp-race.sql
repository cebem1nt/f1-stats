SELECT 
    rd.race_fastest_lap,
    rd.race_pole_position,
    rd.race_reason_retired,
    rds.positions_gained,
    fl.fastest_lap_gap,
    rd.race_positions_gained as gained,
    d.name as '',
    c.name as constructor,
    rd.race_grid_position_text as start,
    rd.position_text as finish,
    rd.race_gap as gap,
    rd.race_laps as laps, 
    rd.race_pit_stops as pits,
    fl.fastest_lap_time as 'best lap time',
    fl.fastest_lap_lap as 'best lap',
    rd.race_time_penalty as penalty,
    rds.position_text as 'pts pos',
    rd.race_points as pts
FROM 
    race_data rd
JOIN 
    race on race.id = rd.race_id
JOIN
    driver d on d.id = rd.driver_id
JOIN
    grand_prix on grand_prix.id = race.grand_prix_id
JOIN
    constructor c on c.id = rd.constructor_id    
LEFT JOIN    
    race_data fl on fl.race_id = rd.race_id
    and fl.driver_id = rd.driver_id
    and fl.type = 'FASTEST_LAP'
LEFT JOIN
    race_driver_standing rds on rds.race_id = race.id
    and rds.driver_id = rd.driver_id
WHERE 
    race.grand_prix_id = :id and 
    race.year = :year and
    rd.type = 'RACE_RESULT'
ORDER BY
    rd.position_display_order ASC
