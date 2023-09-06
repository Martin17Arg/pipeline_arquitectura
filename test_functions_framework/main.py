from google.cloud import storage
import functions_framework


# Importar query desde GCS
def leer_query(indicador, gcs):	

	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	query_path = f"stage-job-files/measure_{indicador}/indicator.sql" 

	bucket = gcs.get_bucket(bucket_name) 	
	
	return bucket.blob(query_path).download_as_string().decode('latin1')


def leer_parametria(filename, gcs):

	import json
	
	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	path = f"raw-job-files/{filename}" 

	bucket = gcs.get_bucket(bucket_name) 		
#	blob = bucket.blob(path)	

	return json.loads(bucket.blob(path).download_as_string())
	#return bucket.blob(path).download_as_string()


def leer_carpeta_parametria(carpeta, gcs):

	import json
	
	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	path = f"raw-job-files/{carpeta}" 

	bucket = gcs.get_bucket(bucket_name) 		
	blob_list = list(bucket.list_blobs(prefix=path))

	#return json.loads(bucket.blob(path).download_as_string())
	return blob_list[1].download_as_string()


def identificar_origenes(query):

	prefix = "pre_stage"
	origenes = [word for word in query.split() if word.startswith("pre_stage")]

	return set(origenes)


def reemplazar_origenes(indicador):
	return None

def main(request):

	gcs = storage.Client()

	#if request.args and 'indicador' in request.args:
		
		#query = leer_query(request.args.get('indicador'), gcs)
		#prefix = "pre_stage"
		#origenes = [word for word in query.split() if word.startswith("pre_stage")]

		#return origenes
		#return request.args.get('indicador')
		
			
	#else:
	#	return f'ERROR'
	conexiones = leer_carpeta_parametria("conexiones", gcs)
	
	return conexiones
