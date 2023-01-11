
SELECT 
-- s.name AS schema_name
-- ,t.name AS table_name
-- ,DB_NAME() as database_name
-- , @@SERVERNAME+'.database.windows.net' as server_name
 'mssql://'+@@SERVERNAME+'.database.windows.net/' + DB_NAME()  +'/' + s.name + '/' + t.name
FROM sys.tables t
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.objects o ON t.object_id = o.object_id
WHERE o.type_desc IN ('USER_TABLE', 'VIEW')

UNION ALL 

SELECT 
 'mssql://'+@@SERVERNAME+'.database.windows.net/' + DB_NAME()  +'/' + s.name + '/' + t.name
FROM sys.views t
JOIN sys.schemas s ON t.schema_id = s.schema_id
