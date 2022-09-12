CREATE OR REPLACE FUNCTION del_all() RETURNS trigger
AS $$
    BEGIN
	delete from rehearsal where roomid in (select id from room where baseid = old.id);
    delete from equipment where roomid in (select id from room where baseid = old.id);
	delete from room where baseid = old.id;
	return old;
    END;
$$ LANGUAGE PLPGSQL;

create trigger del_dependencies
before delete on reh_base
for each row
execute function del_all();