def detectar_origenes_indicador(indicador
	,parametria_indicador
	,conexiones
	,directorio_bucket
	,directorio_parametria_origenes):

	"""
	Analiza la consulta del indicador e identifica los origenes.
	Devuelve una lista con los origenes.
	"""
	
	import glob
	from google.cloud import bigquery

	# importar query del indicador como string
	parametria_indicador.update(conexiones[parametria_indicador["conexion"]])
	
	query_file = f'{directorio_bucket}measure_{indicador}/indicator.sql'
	with open(query_file) as f:
		query_raw = f.read()

#	print(query_raw)

	# importar lista de archivos json en parametria/origenes/
	origenes_parametria_raw = glob.glob(directorio_parametria_origenes+"*.json")
	origenes_clean = list()

	for item in origenes_parametria_raw:
		origenes_clean.append(item.split(".")[1].split("/")[-1])
#	origenes_clean = [origenes_parametria_raw[item].split(".").split("/")[-2] for item in range(len(origenes_parametria_raw))]
#	filter
	print(origenes_clean)		

	# Filtrar los origenes de las queries y agregarlos a una tabla
	origenes = list()

	return origenes	
