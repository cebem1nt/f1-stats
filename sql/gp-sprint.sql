SELECT
    r.race_positions_gained,
    r.race_reason_retired,
    driver.name as driver,
    constructor.name as constructor,
    r.race_grid_position_text as start,
    r.position_text as finish,
    r.race_gap as gap,
    r.race_laps as laps,
    r.race_time_penalty as penalty,
    r.race_points as pts
FROM
    race_data r
JOIN
    race on race.id = r.race_id
JOIN
    driver on driver.id = r.driver_id
JOIN    
    constructor on constructor.id = r.constructor_id
WHERE    
    r.type = 'SPRINT_RACE_RESULT' and
    race.grand_prix_id = :id and
    race.year = :year