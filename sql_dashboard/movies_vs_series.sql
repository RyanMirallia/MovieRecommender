SELECT 
    type, 
    count(*) AS total
FROM titles
GROUP BY type
ORDER BY total DESC