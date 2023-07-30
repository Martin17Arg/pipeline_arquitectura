#! /home/martin/macro/bin/python

import json
from google.cloud import bigquery
from verificar_origen import verificar_origen

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

	query_verificacion_sql = "./consultas/verificar_origen.sql"
	with open(query_verificacion_sql) as query_raw:
		query_verificacion = query_raw.read()
	
	parametria_fct_json = dir_parametria_origenes + "bm_situaciones_prestamos_vw.json"
	with open(parametria_fct_json) as parametros:
		parametria_fct = json.load(parametros)

	parametria_lkp_json = dir_parametria_origenes + "bm_clientes.json"
	with open(parametria_lkp_json) as parametros:
		parametria_lkp = json.load(parametros)

	estado_verificacion = dict()
	client = bigquery.Client()	

#	print(query_verificacion)	

	print("Verificacion ftc:\n")
	estado_verificacion["bm_situaciones_prestamos_vw"] = verificar_origen(client,parametria_fct,conexiones,parametria_fechas,query_verificacion, 202210)
	print("Verificacion fct: ",estado_verificacion["bm_situaciones_prestamos_vw"],"\n")

	print("Verificacion lkp:\n")
	estado_verificacion["bm_clientes"] = verificar_origen(client,parametria_lkp,conexiones,parametria_fechas,query_verificacion, 202210)
	print("Verificacion lkp: ",estado_verificacion["bm_clientes"],"\n")
