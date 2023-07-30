def verificar_corrida_indicador(
	indicador: str
	,periodo: int
	,conexiones: dict
	,parametria: dict
	,query_verificacion: str
	) -> int:

	import json
	from google.cloud import bigquery

	# reemplazar parametria en la query template
	query_
	# conectar a BQ y correr la consulta
