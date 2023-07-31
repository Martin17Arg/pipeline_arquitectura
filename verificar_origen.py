def verificar_origen(cliente
	,parametria_tabla
	,conexiones
	,parametria_fechas
	,query_verificacion
	,periodo):

	""" Verificar que el origen (LKP o FCT) contiene registros y está actualizado """

	# Crear dict vacio para 
	param = {
		"tabla": ""
		,"tipo":""
		,"conexion": ""
		,"proyecto": ""
		,"dataset": ""
		,"dias_desde_actualizacion": 30
		,"intervalo_periodos_hacia_atras": 1
		,"campo_fecha": "Fecha_Key"
		,"tabla_fechas": ""
		,"proyecto_fechas": ""
		,"dataset_fechas": ""
		}	

	# Cargar conexiones a parametria
	param.update(parametria_tabla)
	param.update(conexiones[parametria_tabla["conexion"]])
	
	# Cargar parametria de tabla calendario
	parametria_fechas.update(conexiones[parametria_fechas["conexion"]])
	param["tabla_fechas"] = parametria_fechas["tabla"]
	param["proyecto_fechas"] = parametria_fechas["proyecto"]
	param["dataset_fechas"] = parametria_fechas["dataset"]

	print(param)

	# Ejecutar consulta de verificacion 
	from google.cloud import bigquery

	query = query_verificacion.format(**param, periodo=periodo)
	
	resultados = cliente.query(query).result()

	for row in resultados:
		condicion = row[0]

	return condicion
