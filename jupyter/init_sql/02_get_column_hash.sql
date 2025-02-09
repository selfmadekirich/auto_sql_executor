CREATE OR REPLACE FUNCTION get_column_hashes(table_name TEXT)
RETURNS TEXT[] AS
$$
DECLARE
    col_name TEXT;
    hash_result TEXT;
    hashes TEXT[] := '{}';
    query TEXT;
BEGIN
    
    FOR col_name IN
        SELECT column_name
        FROM information_schema.columns c
        WHERE c.table_name = get_column_hashes.table_name
        ORDER BY ordinal_position
    LOOP
        query := format('SELECT md5(array_agg(%I)::TEXT) FROM %I', col_name, get_column_hashes.table_name);
        
        EXECUTE query INTO hash_result;
        
        hashes := array_append(hashes, hash_result);
    END LOOP;

    RETURN hashes;
END;
$$
LANGUAGE plpgsql;