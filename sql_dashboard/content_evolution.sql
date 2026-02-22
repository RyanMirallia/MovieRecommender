SELECT 
    TRIM(SUBSTR(date_added, INSTR(date_added, ',') + 1, 4)) AS year_added,
    count(*) AS total_added
FROM titles
WHERE date_added IS NOT NULL 
  AND date_added <> 'Unknown'
  AND date_added <> ''
GROUP BY year_added
ORDER BY year_added ASC