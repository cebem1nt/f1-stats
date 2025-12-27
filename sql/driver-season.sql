SELECT 
    race_data.race_fastest_lap,
    race_data.race_pole_position,
    grand_prix.abbreviation as '',
    race_data.race_grid_position_text as pos,
    race_data.position_text as finish,
    race_data.race_positions_gained as gained,
    race_data.race_laps as laps,
    race_data.race_reason_retired as 'reason retired',
    race_data.race_gap as gap,
    race_driver_standing.points as pts,
    race_driver_standing.position_number as 'pts pos',
    race_driver_standing.positions_gained as 'pts pos gained',
    constructor.name as ''
FROM 
    race_data
JOIN 
    race on race.id = race_data.race_id
JOIN
    constructor on constructor.id = race_data.constructor_id
JOIN
    grand_prix on grand_prix.id = race.grand_prix_id
LEFT JOIN
    race_driver_standing on race_driver_standing.race_id = race.id
    and race_driver_standing.driver_id = :id
WHERE 
    race_data.driver_id = :id and 
    race_data.type = 'RACE_RESULT' and 
    race.year = :year