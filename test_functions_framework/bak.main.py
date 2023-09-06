from google.cloud import storage
import functions_framework


# Importar query desde GCS
def leer_query(indicador, gcs):	

	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	query_path = f"stage-job-files/measure_{indicador}/indicator.sql" 

	bucket = gcs.get_bucket(bucket_name) 	
	
	return bucket.blob(query_path).download_as_string().decode('utf-8')


def leer_parametria(filename, gcs):

	import json
	
	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	path = f"raw-job-files/{filename}" 

	bucket = gcs.get_bucket(bucket_name) 		
#	blob = bucket.blob(path)	

	return json.loads(bucket.blob(path).download_as_string())
	#return bucket.blob(path).download_as_string()


def leer_carpeta_parametria(carpeta, gcs):
# PENDIENTE: hacer individualizado, solo importar archivos utilizados 
	import json
	
	bucket_name = "bm-gcp-ue1-t1-ml-bkt-custom"
	path = f"raw-job-files/{carpeta}/" 

	bucket = gcs.get_bucket(bucket_name) 		
	blob_list = list(bucket.list_blobs(prefix=path))

	parametria = dict()
	for item in blob_list:
		conexion = item.name.replace(path,'').replace('.json','')
		contenido = json.loads(item.download_as_string().decode('utf-8'))
		parametria.update({conexion: contenido})

	return parametria

def identificar_origenes(query, prefix):

	origenes = [word for word in query.split() if word.startswith(prefix)]

	return set(origenes)


def reemplazar_origenes(query,prefix,origenes_procesado):

	print(origenes_procesado)
	print()
	
	for origen in origenes_procesado.keys():
		string_original = prefix + origen
		string_procesado = origenes_procesado[origen]["proyecto"]+"."+origenes_procesado[origen]["dataset"]+"."+origenes_procesado[origen]["nombre_tabla"]
		print(string_original)
		print(string_procesado)
		query.replace(string_original,string_procesado)

	return query

def main(request):

	gcs = storage.Client()

	if request.args and 'indicador' in request.args:
		
		query = leer_query(request.args.get('indicador'), gcs)
		prefix = "pre_stage."
		origenes_query = identificar_origenes(query,prefix) 

		#return origenes
		#return request.args.get('indicador')
		
		# Leer parametria:
		conexiones = leer_carpeta_parametria("conexiones", gcs)
		origenes = leer_carpeta_parametria("origenes", gcs)

		for key in origenes.keys():
			#print("key: ",key)
			#print("conexion: ",origenes[key]["conexion"])
			#print(conexiones[origenes[key]["conexion"]])
			#print()
			origenes[key].update(conexiones[origenes[key]["conexion"]])
	
		query_procesada = reemplazar_origenes(query,prefix,origenes)		

		#return query_procesada
		return origenes 
				
	else:
		return f'ERROR: falta indicador o indicador no encontrado'
		
