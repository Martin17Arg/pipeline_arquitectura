/* DESCRIPCION INDICADOR
FLAG_PMO
 
 
*/

-- PARAMETROS

DECLARE date_ejecucion DATE DEFAULT CURRENT_DATE;
DECLARE int_meses_atras INT64 DEFAULT {0};
DECLARE array_estado_deuda ARRAY<STRING>;
DECLARE str_familia_productos STRING DEFAULT 'Personales';
DECLARE array_producto_source ARRAY<STRING>;
DECLARE str_cartera STRING DEFAULT 'De Orden';
DECLARE str_producto STRING DEFAULT 'Cuentas de Orden';
DECLARE array_subproductos ARRAY<STRING>;
DECLARE str_banca STRING DEFAULT 'Individuos';

SET array_estado_deuda = ['B.CONTABLE', 'CANCELADA', 'Suspenso'];
SET array_producto_source = ['RDEUTCP','RDEUTCPEI','RPERP','RPERPEI','RPERSCONVP','RPERSJUBP'];
SET array_subproductos = ['PARTICIPACIONES EN OTRAS SOCIEDADES', 'PARTICIPACIONES OTRAS SOCIEDADES R.P.C.','PARTICIPACIONES : CONTADURIA', 'PARTICIPACIONES CONTADURIA'];

-- FUNCIONES

CREATE TEMP FUNCTION udf_periodo(fecha_ejecucion DATE)
-- Periodo YYYYMM
    RETURNS INT64
    AS (EXTRACT(YEAR FROM LAST_DAY(DATE_SUB(fecha_ejecucion, INTERVAL 1 MONTH), MONTH))*100 +
        EXTRACT(MONTH FROM LAST_DAY(DATE_SUB(fecha_ejecucion, INTERVAL 1 MONTH), MONTH)));

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

-- CONSULTA

INSERT INTO {proyecto}.{dataser}.measure_{indicador}

SELECT DISTINCT cc.CODIGO_CLIENTE
	,udf_periodo(date_ejecucion) AS Periodo
	,1 AS flag_pmo

FROM bm_situacion_diaria_cartera s
INNER JOIN bm_clientes cc on (s.Cliente_Key = cc.Cliente_Key)
INNER JOIN bm_prestamos pre on (s.Cuenta_Key = pre.Cuenta_Key)
INNER JOIN bm_fechas f on (s.Fecha_Key = f.Fecha_Key)
INNER JOIN bm_estado_deuda e on (s.Estado_Deuda_Key = e.Estado_Deuda_Key)
INNER JOIN bm_productos p on (s.Producto_Key = p.Producto_Key)
INNER JOIN bm_bancas ba on (s.Banca_Key = ba.Banca_Key)

WHERE DATE(f.Fecha) = udf_fecha_fin(date_ejecucion)
AND e.Estado_Deuda NOT IN UNNEST(array_estado_deuda)
AND (p.Familia_Productos = str_familia_productos OR p.Producto_Source IN UNNEST(array_producto_source))
AND p.Cartera != str_cartera
AND p.Producto != str_producto
AND p.Subproducto NOT IN UNNEST(array_subproductos)
AND ba.Banca = str_banca 
