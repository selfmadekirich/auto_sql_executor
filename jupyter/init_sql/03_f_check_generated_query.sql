drop function if exists f_check_generated_query;
CREATE OR REPLACE FUNCTION f_check_generated_query(correct_view text, generated_view text)
RETURNS jsonb AS
$$
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
		information_schema.columns where table_name = ''%I''
		) t from information_schema.columns
		where table_name = ''%I''', correct_view, generated_view) into attr_count;
 	
		
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
$$
LANGUAGE plpgsql;


/*
select check_generated_query('not_exists', 'all')

-- output: Error!

select check_generated_query('test_001', 'test_001')

-- output: {"attr_count_mismatch": 0, "rows_count_mismatch": 0, "cols_hashes_mismatch": []}

select check_generated_query('test_001', 'test')

-- {"attr_count_mismatch": 1, "rows_count_mismatch": -48994, "cols_hashes_mismatch": ["25265c47e5182330fe2e74235c5a1e75", "38654549aaf1f3e0eb259e9cc3902cfd", "098c1ebc8d18a24e4958e06122877b86"]}


-- test_002 и test_003 - одни и те же запросы,но с разным порядком столбцов
select check_generated_query('test_002', 'test_003')

-- {"attr_count_mismatch": 0, "rows_count_mismatch": 0, "cols_hashes_mismatch": []}

*/