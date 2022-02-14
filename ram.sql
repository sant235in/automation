CREATE OR REPLACE PROCEDURE replication_process(p_env VARCHAR2)
AS
-------------------------------------------------------------------------------
--
-- Procedure to check if schema contains tables storing replication info, and
-- do processing as per the info in the tables.
--
-------------------------------------------------------------------------------
    l_count PLS_INTEGER;
BEGIN
    -- Loop through the schemas
    FOR rec_user IN (
                     SELECT username
                     FROM dba_users
                     WHERE oracle_maintained = 'N'
                       AND username <> USER
                    )
    LOOP
        -- Check if the two custom tables storing metadata are available
        SELECT COUNT(*)
        INTO l_count
        FROM dba_tables
        WHERE owner = rec_user.username
          AND table_name = 'IN_COUNTRY_REPLICATION';

        IF l_count <> 0
        THEN
            dbms_output.put_line('IN exist in '||rec_user.username);
        END IF;

        SELECT COUNT(*)
        INTO l_count
        FROM dba_tables
        WHERE owner = rec_user.username
          AND table_name = 'BETWEEN_COUNTRY_REPLICATION';

        IF l_count <> 0
        THEN
            dbms_output.put_line('BET exist in '||rec_user.username);
        END IF;
    END LOOP;
END;
/

-- exec replication_process('DEV')
