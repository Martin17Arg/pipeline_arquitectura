#! /home/martin/macro/bin/python

import json
from google.cloud import bigquery
from verificar_origen import verificar_origen
from verificar_indicador import verificar_indicador
from detectar_origenes_indicador import detectar_origenes_indicador

if __name__ == "__main__":

	# Parametria conexiones
	
	dir_parametria = "./parametria/"
	dir_parametria_origenes = dir_parametria + "origenes/"

	parametria_conexiones = dir_parametria + "conexiones.json"
	with open(parametria_conexiones) as conex:
		conexiones = json.load(conex)

	parametria_fechas_json = dir_parametria_origenes + "bm_fechas.json" 
	with open(parametria_fechas_json) as parametros:
		parametria_fechas = json.load(parametros)

	query_verificacion_origen = "./consultas/verificar_origen.sql"
	with open(query_verificacion_origen) as query_raw:
		query_verificacion = query_raw.read()

	query_verificacion_indicador = "./consultas/verificar_indicador.sql" 
	with open(query_verificacion_indicador) as query_raw:
		query_verificacion_indicador = query_raw.read()
	
	parametria_fct_json = dir_parametria_origenes + "bm_situaciones_prestamos_vw.json"
	with open(parametria_fct_json) as parametros:
		parametria_fct = json.load(parametros)

	parametria_lkp_json = dir_parametria_origenes + "bm_clientes.json"
	with open(parametria_lkp_json) as parametros:
		parametria_lkp = json.load(parametros)
	
	parametria_indicador_json = dir_parametria + "/indicadores/" + "flag_pmo.json"
	with open(parametria_indicador_json) as parametros:
		parametria_indicador = json.load(parametros)
	
	estado_verificacion = dict()
#	client = bigquery.Client()	

	'''
	print("Verificacion ftc:\n")
	estado_verificacion["bm_situaciones_prestamos_vw"] = verificar_origen(client,parametria_fct,conexiones,parametria_fechas,query_verificacion, 202210)
	print("Verificacion fct: ",estado_verificacion["bm_situaciones_prestamos_vw"],"\n")

	print("Verificacion lkp:\n")
	estado_verificacion["bm_clientes"] = verificar_origen(client,parametria_lkp,conexiones,parametria_fechas,query_verificacion, 202210)
	print("Verificacion lkp: ",estado_verificacion["bm_clientes"],"\n")
	
	print("Registro de verificaciones en diccionario:")
	print(estado_verificacion)

	print("\nVerificacion indicadores: (0: tiene registros, 1: no tiene registros\n")
	print("Verificacion de indicador para 202210: ",verificar_indicador(client,parametria_indicador,conexiones,query_verificacion_indicador,202210))
	print("Verificacion de indicador para 202211: ",verificar_indicador(client,parametria_indicador,conexiones,query_verificacion_indicador,202211))
	'''
	print("\nLista de origenes por indicador: \n")
	directorio_bucket = "/home/martin/kpi_macro/dlh-bda-custom/stage-job-files/"
	directorio_parametria_origenes = "./parametria/origenes/"
	print(detectar_origenes_indicador("flag_pmo",parametria_indicador,conexiones,directorio_bucket,directorio_parametria_origenes))
