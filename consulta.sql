CREATE TEMPORARY TABLE cnae (
    cod_cnae VARCHAR(30)
);

\copy cnae FROM './cod_cnae.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

DO $$
DECLARE
BEGIN
    BEGIN
        CREATE TABLE new_table_ipea AS (SELECT * FROM tabela_ipea WHERE cnae_ipea 
                                    IN (SELECT cod_cnae in cnae));        
    END;
END $$;

