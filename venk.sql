Declare
v_usr_env varchar2(10);
v_svr_host varchar2(100);
v_stmt_str      VARCHAR2(200);
TYPE CurTyp  IS REF CURSOR;
v_icr_cursor CurTyp;
cursor c1 is select distinct owner from dba_tables 
             where owner in(select username from all_users 
                            where oracle_maintained ='N' 
                            and table_name in ('IN_COUNTRY_REPLICATION','BETWEEN_COUNTRY_REPLICATION') order by 1);
Begin
select sys_context('USERENV','DB_NAME'),sys_context('USERENV','SERVER_HOST') into v_usr_env,v_svr_host from dual;

FOR v1 in c1 loop
v_stmt_str := 'SELECT count(1) FROM :i.IN_COUNTRY_REPLICATION';
OPEN v_icr_cursor FOR v_stmt_str using v1.owner;

  LOOP
    FETCH v_icr_cursor INTO cnt_record;
    EXIT WHEN v_icr_cursor%NOTFOUND;
  END LOOP;

CLOSE v_icr_cursor;

End;
