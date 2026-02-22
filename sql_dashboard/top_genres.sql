SELECT 
    CASE 
        WHEN listed_in LIKE '%,%' THEN SUBSTR(listed_in, 1, INSTR(listed_in, ',') - 1)
        ELSE listed_in 
    END AS genre_name,
    count(*) AS total_titles
FROM titles
GROUP BY genre_name
ORDER BY total_titles DESC
LIMIT 10