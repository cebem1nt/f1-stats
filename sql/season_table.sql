SELECT
    grand_prix.abbreviation,
    driver.name,
    race_data.position_text,
    season_driver_standing.points,
    race_data.race_pole_position,
    race_data.race_fastest_lap
FROM
    race
JOIN
    race_data on race_data.race_id = race.id
LEFT JOIN
    grand_prix on grand_prix.id = race.grand_prix_id
RIGHT JOIN
    driver on driver.id = race_data.driver_id
RIGHT JOIN
    season_driver_standing on season_driver_standing.year = ? and
    season_driver_standing.driver_id = race_data.driver_id
WHERE
    race.year = ? and
    race_data.type = 'RACE_RESULT'
ORDER BY
    season_driver_standing.points DESC,
    driver.name ASC
