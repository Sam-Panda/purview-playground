
-- This query is used to scan the data sources in a SQL Database. It returns the list of tables, views, and schemas in the database.
SELECT 
 'mssql://'+@@SERVERNAME+'.database.windows.net/' + DB_NAME()  +'/' + s.name + '/' + t.name
FROM sys.tables t
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.objects o ON t.object_id = o.object_id
WHERE o.type_desc IN ('USER_TABLE', 'VIEW')

UNION ALL 
-- This query is used to scan the data sources in a SQL Database. It returns the list of tables, views, and schemas in the database. ( SYSTEM VIEWS)
SELECT 
 'mssql://'+@@SERVERNAME+'.database.windows.net/' + DB_NAME()  +'/' + s.name + '/' + t.name
FROM sys.views t
JOIN sys.schemas s ON t.schema_id = s.schema_id

UNION ALL
-- This query is used to scan the data sources in a SQL Database. It returns the list of schemas in the database.
SELECT 
 'mssql://'+@@SERVERNAME+'.database.windows.net/' + DB_NAME()  +'/' + s.name 
FROM sys.schemas s

UNION ALL
--  This query is used to scan the data sources in a SQL Database. It returns the list of databases in the server.
SELECT 'mssql://'+@@SERVERNAME+'.database.windows.net/' + DB_NAME()