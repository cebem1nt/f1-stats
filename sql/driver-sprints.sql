SELECT
    grand_prix.name,
    q.qualifying_q1 as q1,
    q.qualifying_q2 as q2,
    q.qualifying_q3 as q3,
    q.qualifying_gap as gap,
    q.qualifying_interval as interval,
    q.qualifying_laps as laps,
    r.race_grid_position_text as start,
    r.position_text as finish,
    r.race_positions_gained as gained,
    r.race_time_penalty as penalty,
    r.race_gap as gap,
    r.race_interval as interval,
    r.race_points as pts
FROM
    race_data q
JOIN
    race on race.id = q.race_id
JOIN
    grand_prix on grand_prix.id = race.grand_prix_id
LEFT JOIN
    race_data r on r.driver_id = :id and
    r.race_id = q.race_id and
    r.type = 'SPRINT_RACE_RESULT'
WHERE    
    q.type = 'SPRINT_QUALIFYING_RESULT' and
    q.driver_id = :id and
    race.year = :year