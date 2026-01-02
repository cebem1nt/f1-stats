SELECT
    grand_prix.name,
    pit.pit_stop_lap,
    pit.pit_stop_time
FROM
    race_data pit
JOIN 
    race on race.id = pit.race_id
JOIN
    grand_prix on grand_prix.id = race.grand_prix_id
WHERE
    pit.type = 'PIT_STOP' and
    pit.driver_id = :id and
    race.year = :year