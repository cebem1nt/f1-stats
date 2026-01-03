SELECT 
    rd.race_fastest_lap,
    rd.race_pole_position,
    rd.race_reason_retired,
    constructor.name,
    race_driver_standing.positions_gained,
    fl.fastest_lap_gap,
    grand_prix.name as '',
    rd.race_grid_position_text as start,
    rd.position_text as finish,
    rd.race_positions_gained as gained,
    rd.race_gap as gap,
    rd.race_laps as laps, 
    rd.race_pit_stops as pits,
    fl.fastest_lap_time as 'best lap time',
    fl.fastest_lap_lap as 'best lap',
    rd.race_time_penalty as penalty, 
    race_driver_standing.position_text as 'pts pos',
    race_driver_standing.points as pts
FROM 
    race_data rd
JOIN 
    race on race.id = rd.race_id
JOIN
    constructor on constructor.id = rd.constructor_id
JOIN
    grand_prix on grand_prix.id = race.grand_prix_id
LEFT JOIN    
    race_data fl on fl.race_id = rd.race_id
    and fl.driver_id = :id 
    and fl.type = 'FASTEST_LAP'
LEFT JOIN
    race_driver_standing on race_driver_standing.race_id = race.id
    and race_driver_standing.driver_id = :id    
WHERE 
    rd.driver_id = :id and 
    rd.type = 'RACE_RESULT' and 
    race.year = :year