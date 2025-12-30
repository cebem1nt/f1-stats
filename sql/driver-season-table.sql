SELECT 
    rd.race_fastest_lap,
    rd.race_pole_position,
    rd.race_reason_retired,
    constructor.name,
    race_driver_standing.positions_gained,
    grand_prix.name as '',
    q.qualifying_q1 as q1,
    q.qualifying_q2 as q2,
    q.qualifying_q3 as q3,
    rd.race_laps as laps,
    rd.race_grid_position_text as start,
    rd.position_text as finish,
    rd.race_positions_gained as gained,
    rd.race_gap as gap,
    race_driver_standing.position_text as pos,
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
    race_data q on q.race_id = rd.race_id and
    q.driver_id = :id and
    q.type = 'QUALIFYING_RESULT'
LEFT JOIN
    race_driver_standing on race_driver_standing.race_id = race.id
    and race_driver_standing.driver_id = :id
WHERE 
    rd.driver_id = :id and 
    rd.type = 'RACE_RESULT' and 
    race.year = :year