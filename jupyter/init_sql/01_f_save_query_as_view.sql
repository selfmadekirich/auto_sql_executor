drop function if exists f_save_query_as_view;
CREATE OR REPLACE FUNCTION f_save_query_as_view(view_name text, sql_query text)
RETURNS boolean AS
$$
BEGIN
	begin 

        EXECUTE format('DROP VIEW IF EXISTS %I;CREATE OR REPLACE VIEW %I as %s', view_name, view_name, sql_query);
		return true;
	exception 
		when others then 
			return false;
	end;

END;
$$
LANGUAGE plpgsql;