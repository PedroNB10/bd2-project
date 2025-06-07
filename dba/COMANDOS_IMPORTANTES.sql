-- Retorna a quantidade de linhas em todas as colunas do banco

SELECT 
    relname AS table_name, 
    n_live_tup AS total_rows
FROM 
    pg_stat_user_tables
ORDER BY 
    total_rows DESC;