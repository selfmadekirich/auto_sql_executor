drop function save_query_as_view;
CREATE OR REPLACE FUNCTION save_query_as_view(view_name text, sql_query text)
RETURNS boolean AS
$$
BEGIN
	begin 

        EXECUTE format('CREATE OR REPLACE VIEW %I as %s', view_name, sql_query);
		return true;
	exception 
		when others then 
			return false;
	end;

END;
$$
LANGUAGE plpgsql;