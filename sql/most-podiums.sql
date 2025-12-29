SELECT
    ROW_NUMBER() 
        OVER (ORDER BY total DESC) AS '',
    driver,
    total
FROM (
    SELECT
        driver.name AS driver,
        COUNT(*) AS total
    FROM 
        race_data race_result
    JOIN 
        race ON race_result.race_id = race.id
    JOIN 
        driver ON driver.id = race_result.driver_id
    WHERE 
        race_result.type = 'RACE_RESULT'
        AND race.circuit_id = ?
        AND race_result.position_number <= 3        
    GROUP BY 
        driver.name
)