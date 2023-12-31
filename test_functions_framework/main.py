from google.cloud import storage
import functions_framework


# Importar query desde GCS
def leer_query(indicador, storage_client):	

	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	query_path = f"stage-job-files/measure_{indicador}/indicator.sql" 

	bucket = storage_client.get_bucket(bucket_name) 	
	
	return bucket.blob(query_path).download_as_string().decode('utf-8')


def leer_parametria(filename, storage_client):

	import json
	
	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	path = f"raw-job-files/{filename}" 

	bucket = storage_client.get_bucket(bucket_name) 		

	return json.loads(bucket.blob(path).download_as_string())


def leer_carpeta_parametria(carpeta,storage_client,lista_keys=None):
# PENDIENTE: hacer individualizado, solo importar archivos utilizados 
	import json
	
	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	path = f"raw-job-files/{carpeta}/" 

	bucket = storage_client.get_bucket(bucket_name) 		
	blob_list = list(bucket.list_blobs(prefix=path))
	
	parametria = dict()

	if lista_keys:
		for item in blob_list:
			parametro = item.name.replace(path,'').replace('.json','')
			if parametro in lista_keys:
				contenido = json.loads(item.download_as_string().decode('utf-8'))
				parametria.update({parametro: contenido})
	else:
		for item in blob_list:
			parametro = item.name.replace(path,'').replace('.json','')
			contenido = json.loads(item.download_as_string().decode('utf-8'))
			parametria.update({parametro: contenido})
		
	return parametria

def identificar_origenes(query, prefix):

	origenes = [word.replace(prefix,'') for word in query.split() if word.startswith(prefix)]

	return set(origenes)


def reemplazar_origenes(query,prefix,origenes_procesado):

	print(origenes_procesado)
	print()
	
	query_procesada = query

	for origen in origenes_procesado.keys():
		string_original = prefix + origen
		string_procesado = origenes_procesado[origen]["proyecto"]+"."+origenes_procesado[origen]["dataset"]+"."+origenes_procesado[origen]["nombre_tabla"]
		query_procesada = query_procesada.replace(string_original,string_procesado)

	return query_procesada

def main(request):

	storage_client = storage.Client()

	if request.args and 'indicador' in request.args:
		
		query = leer_query(request.args.get('indicador'), storage_client)
		prefix = "pre_stage."

		origenes_set = identificar_origenes(query,prefix) 

		# Leer parametria:
		origenes = leer_carpeta_parametria("origenes", storage_client, origenes_set)
		conexiones = leer_carpeta_parametria("conexiones", storage_client)

		for key in origenes.keys():
			origenes[key].update(conexiones[origenes[key]["conexion"]])

		# Reemplazar origenes en la query	
		query_procesada = reemplazar_origenes(query,prefix,origenes)		

		return query_procesada 
				
	else:
		return f'ERROR: falta indicador o indicador no encontrado'
		
