import json
import functions_framework

# Listar parametros necesarios

# Importar query desde GCS
def leer_query(indicador):
	
	gcs = storage.Client()

	bucket = gcs.get_bucket("bm-gcp-ue1-t1-ml-bkt-custom") 	
	query_path = f"stage-job-files/measure_{indicador}/indicator.sql" 
	
	return bucket.blob(query_path).download_as_string().decode('latin1')



@functions_framework.http
def start(request):


from flask import Response
import uuid

def main(request):

    try:
    	request_json = request.get_json(silent=True)
		if request_json:
			query = leer_query(request_json['indicador']
			print(query)
        
		return Response(response = 'ok', status = 200)
                
    except Exception as e:
        print("ERROR ", e)
        return Response(response = 'AN ERROR OCCURED', status = 400)
