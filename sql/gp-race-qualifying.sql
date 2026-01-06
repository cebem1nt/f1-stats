SELECT
    driver.name as driver,
    constructor.name as constructor,
    q.qualifying_q1 as q1,
    q.qualifying_q2 as q2,
    q.qualifying_q3 as q3,
    q.qualifying_gap as gap,
    q.qualifying_laps as laps,
    r.race_grid_position_text as grid
FROM
    race_data q
JOIN
    race on race.id = q.race_id
JOIN
    driver on driver.id = q.driver_id
JOIN    
    constructor on constructor.id = q.constructor_id
LEFT JOIN    
    race_data r on r.race_id = q.race_id and
    r.driver_id = q.driver_id and
    r.type = 'RACE_RESULT'
WHERE    
    q.type = 'QUALIFYING_RESULT' and
    race.grand_prix_id = :id and
    race.year = :year