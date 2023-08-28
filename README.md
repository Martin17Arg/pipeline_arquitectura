# Arquitectura

## V3

Verificacion (primer paso en el flujo)
- OPCION 1:
	- Utilización de parametría en BQ, que se actualiza desde JSON en el Cloud Storage.
	- A través de un join se obtienen los indicadores que están listos para correr (varias tablas).
- OPCION 2: 
	- Verificacion de tablas a través de tabla de calidad de subida --> Se obtiene lista de tablas verificadas.
	- Paralelamente se puede chequear si el indicador ya corrio 
		(debe haber una fuente persistente de esa info indicador-periodo, puede ser 
		BigQuery u otra)
	- A partir de la lista de indicadores completa, se descartan los que ya se corrieron.
	- A partir de la lista de los que no se corrieron, se itera y se verifican los origenes.
	- Si los origenes estan validados (ver primer paso) para ese indicador, se ejecuta la query en 2 pasos:
		1. Cloud function que importa la query y la devuelve con los parametros correctos 
		(reemplazo de nombre de tablas y fecha_ejecucion/periodo).
		2. Ejecución de la query (Workflow, conector BigQuery insert)
		- **Este ultimo paso se puede definir como un subworkflow para poder paralelizarlo.**
	- Logging (a definir):
		- Validación de origenes: informar origenes no validados (lista o registros individuales)
		- Ejecución de indicadores, independientemente del resultado 
		
#### Workflow esquematico (Opcion 2)

- Asignar variables (fecha_ejecucion)
	- Puede que no sea necesario: reemplazar diccionario con fecha y periodo, devuelto por una cloud function.
	
``` yaml
- assignments:
	- fecha_ejecucion: ${time.format(sys.now())}
```

- Definir periodo a partir de fecha de ejecución
	- [ ] TODO: Ver conector CloudFunction

``` yaml
- definir_periodo:
	# Cloud function devuelve periodo en base a fecha de ejecucion
	call: http.get
	args:
		url: #url cloud function
		fecha_ejecucion: ${fecha_ejecucion} 
	result: periodo
```

- Validación de tablas
	- Consulta a BQ. Query personalizada para evaluar condiciones 
	- Inputs: requerimientos para cada origen (uno por origen) 
	- Return: map (diccionario) con origen (key) y resultado de la validacion (value)
 
	- Consulta a tabla de calidad de origenes.
	- JOIN con tabla con requerimientos para cada origen

## Versiones previas 

### V2

- Agregar paralelismo
- Utilizar tabla de calidad de subida de orígenes
- Log que pueda ser interpretado más fácilmente --> alternativas mas intuitivas a Cloud Logging?

### Puntos a revisar

- Como funciona "parallel" dentro de Workflow? se debería limitar la cantidad de trabajos en paralelo?
- Como se puede testear el funcionamiento de un Workflow?
- Debe crearse una cuenta de servicio? quien la crea?

### Lista de tareas:

- [ ] Consulta BQ a tabla de calidad
- [ ] Descargar json de parametría general desde bucket (workflow) --> json.decode
- [ ] Descargar listado de orígenes (json) desde bucket 
- [ ] Descargar listado de indicadores (json) desde bucket
- [ ] Actualizar lista de orígenes por indicador (trigger? o en base a la consulta?)

### Recursos

1. Descarga de objetos desde GCS:
https://cloud.google.com/storage/docs/downloading-objects?hl=es-419#permissions-rest

2. Deserialize JSON (json.decode):
https://cloud.google.com/workflows/docs/reference/stdlib/json/decode

3. Workflow syntax:
https://cloud.google.com/workflows/docs/reference/syntax/syntax-search

4. Workflow pricing:
https://cloud.google.com/workflows/pricing

5. Parallel:
https://cloud.google.com/workflows/docs/reference/syntax/parallel-steps

6. Storage bucket get:
https://cloud.google.com/workflows/docs/reference/googleapis/storage/v1/objects/get

7. Storage connector:
https://cloud.google.com/workflows/docs/samples/workflows-connector-storage

### Flujo de trabajo

- Verificación de orígenes: 
	- que estén actualizados en el último mes (lkp)
	- que tengan datos del ultimo periodo (fct) --> Fecha máxima > fecha_máxima_requerida (inicio ultimo periodo)
	- que tengan suficiente historia (fct) --> Fecha mínima < fecha_mínima_requerida (fin primer periodo)

Se consulta tabla de calidad (ver campos).

- Verificación de indicadores:
	- Detectar orígenes por cada indicador: Consulta BQ --> Lista  
	- Para cada origen se debe chequear que cumpla las condiciones --> alternativa al loop?.
		- Si las condiciones se cumplen, el indicador se corre.
	
Logging?

### Parametría

- conexiones.json: con ubicación de las tablas de origen e indicadores
- orígenes/{tabla_origen}.json: nombre en el dataset, conexión, tipo de tabla

## V1
### Árbol de carpetas y archivos

- parametría
	- conexiones.json: proyecto y dataset para cada conexión (ubicación de orígenes, indicadores, etc)
	- directorios.json: ubicaciones de ciertos buckets de referencia
	- orígenes/
		(un archivo json por origen)
	- indicadores/
		(un archivo json por indicador)
- queries/	(templates sql para realizar operaciones comunes)
	- verificar_origen.sql
	- borrar_indicador_periodo.sql
	- insertar_indicador_periodo.sql

### Procesos

1. Ejecución de indicadores del periodo (automático/manual)
2. Reproceso de indicadores (manual)

### Parametría

- Conexiones: proyecto, dataset
- Orígenes: nombre, conexión, tipo, intervalo_periodos_actualización (solo fct), 
días_desde_actualización (solo lkp), campo_fecha (solo fct)
- Indicadores: nombre, conexión, estado

### Procesamiento de indicadores

A principio de mes, donde la mayoría de las tablas ya estén disponibles y actualizadas, se puede comenzar 
con la ejecución para el total del listado de indicadores.

NOTA: Para evitar repetir la verificación de orígenes que ya se verificaron,
se crea un diccionario con los resultados de verificaciones previas que se consulta previo
a ejecutar una nueva verificación.

### Reproceso automático
El loop sobre el total de indicadores puede realizarse con una frecuencia a definir 
(puede ser diario o puede ser cada un cierto intervalo de días), 
teniendo en cuenta que la razón por la que los indicadores no se corran debería ser 
principalmente por orígenes desactualizados (lo que requiere una acción que no es inmediata) o una falla en
el proceso (en ese caso, una frecuencia diaria o incluso más alta es apropiada).
De todas maneras, esta Cloud function puede ser iniciada manualmente.

Para las nuevas corridas se evita reprocesar los indicadores que ya se corrieron gracias a la primera verificación.
Los orígenes se verifican nuevamente dado que pueden haber cambiado las condiciones.

### Funciones

**Ejecutar_indicadores_activos**
(función orquestador)
- Carga lista de indicadores: tomar archivos de parametría (*opcional: cargar_parametría*)
- Loop sobre lista de indicadores:
	- Verificar si el indicador se corrió para el periodo (*verificar_indicador_periodo*)
	- IF se corrió, pasar a siguiente indicador.
	- ELSE IF no se corrió:
		- Identificar orígenes del indicador a partir de la query (*identificar_orígenes*)
		- Loop sobre los orígenes:
			- Verificar si se el origen ya fue chequeado (diccionario con resultados de la verificación):
			- IF fue chequeado, pasar a siguiente origen
			- ELSE IF  no fue chequeado:
				- Verificar origen (*verificar_origen*)
		- IF algún origen no esta ok, pasar a siguiente indicador
		- ELSE IF todos los orígenes están ok:
			- Insertar registros a la tabla del indicador (*correr_indicador*)

**Verificar_indicador_periodo**

Descripción: Verifica si el indicador corrió para el periodo

Argumentos:
- Indicador (str)
- Periodo (int)
- Conexiones (dict)
- Query_verificación (str)

Return: condición (int)
- 0: No se corrió
- 1: Se corrió el indicador para ese periodo

Para el indicador se levanta su parametría para saber su conexión.

Se utiliza la parametría para reemplazar en la Query_verificación (template) 
los parámetros propios del indicador y el periodo.

Se conecta a BQ y ejecuta la consulta modificada trayendo como resultado la condición. 

*Pasos intermedios: 
- importar query del indicador
- listar orígenes del indicador*

**Verificar_orígenes**

Descripción: Verifica si el origen FCT o LKP está actualizado y con los datos necesarios.

Argumentos:
- Origen (str)
- Periodo (int)
- Conexiones (dict)
