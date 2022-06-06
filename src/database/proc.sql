CREATE OR REPLACE PROCEDURE del_all(base_id int)
AS $$
    BEGIN
    delete from equipment where roomid in (select id from room where baseid = base_id);
	delete from room where baseid = base_id;
	delete from reh_base where id = base_id;
    END;
$$ LANGUAGE PLPGSQL;