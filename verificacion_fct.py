import os
import json
from google.cloud import bigquery

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/martin/.config/gcloud/application_default_credentials.json"


def verificar_fct(request):
"""Verificar que la fct tenga datos del periodo que se corre y la cantidad especificada de periodos hacia atras"""	
	
	with open("verificacion_fct.sql") as f:
		raw_query = f.read()

	query = raw_query.format(**request)

	client = bigquery.Client()
	resultados = client.query(query).result()
	campo = "Verificada"

	return resultados[campo][0]

if __name__ == "__main__":

	with open("bm_situaciones_prestamos_vw.json") as parametros:
		request = json.load(parametros)
	
	print(request)

	verificar_fct(request)
