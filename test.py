#! /home/martin/macro/bin/python

import json
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

	query_verificacion_fct = "./verificar_fct.sql"
	with open(query_verificacion_fct) as query_raw:
		query_verificacion_fct = query_raw.read()

	query_verificacion_lkp = "./verificar_lkp.sql"
	with open(query_verificacion_lkp) as query_raw:
		query_verificacion_lkp = query_raw.read()
	
	parametria_fct_json = dir_parametria_origenes + "bm_situaciones_prestamos_vw.json"
	with open(parametria_fct_json) as parametros:
		parametria_fct = json.load(parametros)

	parametria_fct_json = dir_parametria_origenes + "bm_clientes.json"
	with open(parametria_lkp_json) as parametros:
		parametria_lkp = json.load(parametros)

	estado_verificacion = dict()

	print("Verificacion ftc:\n")
	if parametria_fct["tipo"] = "fct":
		estado_verificacion["bm_situaciones_prestamos_vw"] = verificar_origen(parametria_fct,conexiones,parametria_fechas,query_verificacion_fct, 202210)
	else:
		estado_verificacion["bm_situaciones_prestamos_vw"] = verificar_origen(parametria_fct,conexiones,parametria_fechas,query_verificacion_lkp, 202210)

	print("Verificacion fct: ",resultados_verificacion_1,"\n")

	print("Verificacion lkp:\n")
	if parametria_fct["tipo"] = "fct":
		estado_verificacion["bm_clientes"] = verificar_origen(parametria_fct,conexiones,parametria_fechas,query_verificacion_fct, 202210)
	else:
		estado_verificacion["bm_clientes"] = verificar_origen(parametria_fct,conexiones,parametria_fechas,query_verificacion_lkp, 202210)

# ver como diferenciar entre lkp y fct
