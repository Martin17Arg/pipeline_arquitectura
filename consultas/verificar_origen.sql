--PARAMETROS

DECLARE periodo INT64;
DECLARE date_ejecucion DATE;
DECLARE int_meses_atras INT64;
DECLARE tipo_tabla STRING;

--FUNCIONES

CREATE TEMP FUNCTION udf_fecha_desde_periodo(periodo_ejecucion INT64)
-- Convertir periodo a correr a dia 15 del periodo en formato DATE
	RETURNS DATE
	AS (DATE(CAST(FLOOR(periodo_ejecucion/100) AS INT64),MOD(periodo_ejecucion,100),15));

CREATE TEMP FUNCTION udf_fecha_inicio(fecha_ejecucion DATE, periodo INT64)
-- Fecha inicio del periodo (principio del mes correspondiente) 
	RETURNS DATE
	AS (DATE(EXTRACT(YEAR FROM DATE_SUB(fecha_ejecucion, INTERVAL periodo MONTH))
			,EXTRACT(MONTH FROM DATE_SUB(fecha_ejecucion, INTERVAL periodo MONTH))
			,1));

CREATE TEMP FUNCTION udf_fecha_fin(fecha_ejecucion DATE)
-- Fecha fin del periodo (fin del mes correspondiente) 
	RETURNS DATE
	AS (LAST_DAY(DATE_SUB(fecha_ejecucion, INTERVAL 1 MONTH), MONTH));

SET periodo = {periodo};
SET date_ejecucion = udf_fecha_desde_periodo({periodo});
SET int_meses_atras = {intervalo_periodos_hacia_atras};
SET tipo_tabla = '{tipo}';

-- CONSULTA

IF tipo_tabla = 'fct' THEN
-- Verificacion de tablas fct
(

WITH temp_verificacion AS (

SELECT MIN(DATE(f.Fecha)) AS Fecha_min
,MAX(DATE(f.Fecha)) AS Fecha_max
,udf_fecha_inicio(date_ejecucion,int_meses_atras-2) AS Umbral_min
,udf_fecha_inicio(date_ejecucion,0) AS Umbral_max
,MIN(DATE(f.Fecha))<udf_fecha_inicio(date_ejecucion,int_meses_atras-2) AS Condicion_min
,MAX(DATE(f.Fecha))>=udf_fecha_inicio(date_ejecucion,0) AS Condicion_max
,(MIN(DATE(f.Fecha))<udf_fecha_inicio(date_ejecucion,int_meses_atras-2) 
	AND MAX(DATE(f.Fecha))>=udf_fecha_inicio(date_ejecucion,0)) AS Condicion_completa

FROM {proyecto}.{dataset}.{tabla} t
INNER JOIN {proyecto_fechas}.{dataset_fechas}.{tabla_fechas} f ON (f.Fecha_Key = t.{campo_fecha})
)

SELECT
(CASE WHEN Condicion_completa THEN 0
        WHEN Condicion_min THEN 1 -- No tiene ultimo periodo
        WHEN Condicion_max THEN 2 -- No tiene suficiente historia
        ELSE 3 END) -- No tiene ultimo periodo ni suficiente historia
        AS condicion

FROM temp_verificacion
);

ELSEIF tipo_tabla = 'lkp' THEN
-- Verificacion tablas lkp
(
WITH temp_metadata AS
(SELECT 
	DATE_DIFF(udf_fecha_fin(date_ejecucion),DATE(TIMESTAMP_MILLIS(last_modified_time)),DAY) <= 30 
		AS condicion_dias_desde_actualizacion
	,row_count > 0 AS condicion_registros
	,(DATE_DIFF(udf_fecha_fin(date_ejecucion),DATE(TIMESTAMP_MILLIS(last_modified_time)),DAY) <= 30) AND (row_count > 0) 
		AS condicion_completa
  
FROM {proyecto}.{dataset}.__TABLES__ 
WHERE table_id = '{tabla}')

SELECT
(CASE WHEN Condicion_completa THEN 0
        WHEN Condicion_dias_desde_actualizacion THEN 1 -- No está actualizada recientements
        WHEN Condicion_registros THEN 2 -- No tiene registros
        ELSE 3 END) -- No está actualizada ni tiene registros
        AS condicion

FROM temp_metadata

);

-- Falta tipo de tabla
ELSE SELECT 9;
END IF
