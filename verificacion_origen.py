import json
import typing
from google.cloud import bigquery

def verificar_origen(
	parametria_tabla: dict
	,conexiones: dict
	,parametria_tabla_fechas: dict
	,query_verificacion: str
	,periodo: int
	) -> int:
	"""	Corre queries de verificacion para origenes FCT y LKP """	

	# Agregar proyecto y dataset de la conexion a la parametria de tabla
	parametria_tabla.update(conexiones[parametria_tabla["conexion"]])

	# Tabla fechas: agregar proyecto y dataset
	parametria_tabla_fechas.update(conexiones[parametria_tabla_fechas["conexion"]])
	
	# Completar template con parametria de tabla
	query = query_verificacion.format(**parametria_tabla
				,periodo = periodo
				,proyecto_fechas = parametria_tabla_fechas["proyecto"]
				,dataset_fechas = parametria_tabla_fechas["dataset"]
				,tabla_fechas = parametria_tabla_fechas["tabla"])
	
	# Conexion a BQ y ejecucion de consulta
	client = bigquery.Client()
	resultados = client.query(query).result()

	for row in resultados:
		condicion = row[0]

	return condicion 
