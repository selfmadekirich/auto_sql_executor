CREATE OR REPLACE FUNCTION public.f_check_generated_query(correct_view text, generated_view text)
 RETURNS jsonb
 LANGUAGE plpgsql
AS $function$
declare 
	result jsonb;
    attr_count int8;
    rows_count int8;
    cols_match TEXT[] := '{}';
	hashes_1 TEXT[] := '{}';
    hashes_2 TEXT[] := '{}';
BEGIN
		if not exists(select 1 from information_schema.tables where table_name = correct_view) then 
			raise exception 'Error! Sample view "%s" does not exists!', correct_view;
		end if;
	
        EXECUTE format('select count(*) - (select count(*) from 
		information_schema.columns where table_name = replace(''%I'', ''"'', '''') and table_schema = ''public''
		) t from information_schema.columns
		where table_name = replace(''%I'', ''"'', '''') and table_schema = ''public''', correct_view, generated_view) into attr_count;
 	
		
		EXECUTE format(' select count(*) - ( select count(*) from %I
		) t
		from %I ',correct_view, generated_view) into rows_count;
		
		hashes_1 := (select get_column_hashes(correct_view));
		hashes_2 := (select get_column_hashes(generated_view));
		
		cols_match := (select array(select unnest(hashes_1) except select unnest(hashes_2)));

		return jsonb_build_object(
			'attr_count_mismatch', attr_count,
			'rows_count_mismatch', rows_count,
            'cols_hashes_mismatch', cols_match
		);
END;
$function$
;