-- Crear los schemas
CREATE SCHEMA historico;
CREATE SCHEMA laliga_2013_2014;
CREATE SCHEMA laliga_2014_2015;
CREATE SCHEMA laliga_2015_2016;
CREATE SCHEMA laliga_2016_2017;
CREATE SCHEMA laliga_2017_2018;
CREATE SCHEMA laliga_2018_2019;
CREATE SCHEMA laliga_2019_2020;
CREATE SCHEMA laliga_2020_2021;
CREATE SCHEMA laliga_2021_2022;
CREATE SCHEMA laliga_2022_2023;
CREATE SCHEMA laliga_2023_2024;
CREATE SCHEMA laliga2_2013_2014;
CREATE SCHEMA laliga2_2014_2015;
CREATE SCHEMA laliga2_2015_2016;
CREATE SCHEMA laliga2_2016_2017;
CREATE SCHEMA laliga2_2017_2018;
CREATE SCHEMA laliga2_2018_2019;
CREATE SCHEMA laliga2_2019_2020;
CREATE SCHEMA laliga2_2020_2021;
CREATE SCHEMA laliga2_2021_2022;
CREATE SCHEMA laliga2_2022_2023;
CREATE SCHEMA laliga2_2023_2024;

-- Crear las tablas de historico
CREATE TABLE historico.clasificacion (
    posicion_liga INTEGER,
    id_equipo INTEGER PRIMARY KEY,
    nombre_equipo VARCHAR(50),
    puntos INTEGER,
    puntos_por_partido REAL,
    victorias INTEGER,
    empates INTEGER,
    derrotas INTEGER,
    posesion_media REAL,
    tiros_medios_por_partido REAL,
    tiros_a_puerta_medios_por_partido REAL,
    corners_medios_por_partido REAL
);

CREATE TABLE historico.resultados (
    id_partido VARCHAR(50) PRIMARY KEY,
    jornada INTEGER,
    fecha TIMESTAMP WITHOUT TIME ZONE,
    hora TIME,
    id_local INTEGER,
    nombre_local VARCHAR(50),
    id_visitante INTEGER,
    nombre_visitante VARCHAR(50),
    goles_local INTEGER,
    goles_visitante INTEGER,
    posesion_local INTEGER,
    posesion_visitante INTEGER,
    tiros_local INTEGER,
    tiros_visitante INTEGER,
    tiros_a_puerta_local INTEGER,
    tiros_a_puerta_visitante INTEGER,
    corners_local INTEGER,
    corners_visitante INTEGER
);

-- Crear tablas de resultados para cada schema
DO $$
DECLARE
    schema_name TEXT;
BEGIN
    FOR schema_name IN SELECT name FROM schema_names
    LOOP
        EXECUTE format('CREATE TABLE %I.resultados AS SELECT * FROM %I.resultados', schema_name, 'historico');
    END LOOP;
END$$;


-- Crear tablas de clasificación para cada schema (NO FUNCIONA)
DO $$
DECLARE
    schema_name TEXT;
    table_name TEXT;
    column_name TEXT;
    i INT;
BEGIN
    FOR schema_name IN SELECT name FROM schema_names
    LOOP
        FOR i IN 1..42
        LOOP
            FOR table_name IN SELECT name FROM table_names
            LOOP
                FOR column_name IN SELECT unnest(regexp_split_to_array('posicion_liga,id_equipo,nombre_equipo,puntos,puntos_por_partido,victorias,empates,derrotas,posesion_media,tiros_medios_por_partido,tiros_a_puerta_medios_por_partido,corners_medios_por_partido', ','))
                LOOP
                    EXECUTE format('CREATE TABLE %I.%I%d AS SELECT * FROM historico.clasificacion', schema_name, table_name, i);
                    EXECUTE format('ALTER TABLE %I.%I%d ADD COLUMN %I INTEGER', schema_name, table_name, i, column_name);
                END LOOP;
            END LOOP;
        END LOOP;
    END LOOP;
END$$;

