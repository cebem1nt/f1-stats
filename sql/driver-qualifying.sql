SELECT 
    grand_prix.name as '',
    COALESCE(q.qualifying_time, '----') AS time,
    q.qualifying_q1 as q1,
    q.qualifying_q2 as q2,
    q.qualifying_q3 as q3,
    q.qualifying_gap as gap,
    q.qualifying_interval as interval,
    q.qualifying_laps as laps,
    q.position_text as pos
FROM
    race_data q
JOIN
    race on race.id = q.race_id
JOIN
    grand_prix on grand_prix.id = race.grand_prix_id
WHERE    
    q.type = 'QUALIFYING_RESULT' and
    q.driver_id = :id and
    race.year = :year