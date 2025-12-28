SELECT *
FROM (
    SELECT 
        race.year,
        driver.name as driver,
        q.qualifying_q1 as q1,
        q.qualifying_q2 as q2,
        q.qualifying_q3 as q3,
        CASE 
            WHEN q.qualifying_time THEN q.qualifying_time
            WHEN q.qualifying_q1
                and (q.qualifying_q2 is NULL or q.qualifying_q1 <= q.qualifying_q2)
                and (q.qualifying_q3 is NULL or q.qualifying_q1 <= q.qualifying_q3) THEN q.qualifying_q1
            WHEN q.qualifying_q2
                and (q.qualifying_q1 is NULL or q.qualifying_q2 <= q.qualifying_q1)
                and (q.qualifying_q3 is NULL or q.qualifying_q2 <= q.qualifying_q3) THEN q.qualifying_q2
            WHEN q.qualifying_q3
                and (q.qualifying_q1 is NULL or q.qualifying_q3 <= q.qualifying_q1)
                and (q.qualifying_q2 is NULL or q.qualifying_q3 <= q.qualifying_q2) THEN q.qualifying_q3
            ELSE NULL
        END as best,
        q.qualifying_laps as laps,
        q.tyre_manufacturer_id as tyre,
        q.engine_manufacturer_id as engine,
        q.constructor_id as constructor
    FROM     
        race_data q
    JOIN
        race on race.id = q.race_id
    JOIN
        driver on driver.id = q.driver_id
    WHERE 
        q.type = 'QUALIFYING_RESULT' and
        race.circuit_id = ?
) t
WHERE 
    t.best is not NULL
ORDER BY best ASC;