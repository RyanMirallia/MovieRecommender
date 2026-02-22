SELECT count(DISTINCT 
    CASE 
        WHEN country LIKE '%,%' THEN SUBSTR(country, 1, INSTR(country, ',') - 1)
        ELSE country 
    END
) AS total_paises
FROM titles
WHERE country <> 'Unknown'