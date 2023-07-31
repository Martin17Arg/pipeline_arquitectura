def verificar_indicador(cliente
	,parametria_indicador
	,conexiones
	,query_verificacion
	,periodo):

	""" Verificar que el origen (LKP o FCT) contiene registros y está actualizado """

	# Crear dict vacio para 
	param = {
		"indicador": ""
		,"conexion": ""
		,"proyecto": ""
		,"dataset": ""
		}	

	# Cargar conexiones a parametria
	param.update(parametria_indicador)
	param.update(conexiones[parametria_indicador["conexion"]])
	
	# Ejecutar consulta de verificacion 
	from google.cloud import bigquery

	query = query_verificacion.format(**param, periodo=periodo)
	
	resultados = cliente.query(query).result()

	for row in resultados:
		condicion = row[0]

	return condicion
