# Arquitectura

## V2

- Agregar paralelismo
- Utilizar tabla de calidad de subida de origenes
- Log que pueda ser interpretado más facilmente --> alternativas mas intuitivas a Cloud Logging?

### Puntos a revisar

- Como funciona "parallel" dentro de Workflow? se debería limitar la cantidad de trabajos en paralelo?
- Como se puede testear el funcionamiento de un Workflow?
- Debe crearse una cuenta de servicio? quien la crea?

### Lista de tareas:

- [ ] Consulta BQ a tabla de calidad
- [ ] Descargar json de parametria general desde bucket (workflow) --> json.decode
- [ ] Descargar listado de origenes (json) desde bucket 
- [ ] Descargar listado de indicadores (json) desde bucket
- [ ] Actualizar lista de origenes por indicador (trigger? o en base a la consulta?)

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

- Verificacion de origenes: 
	- que estén actualizados en el último mes (lkp)
	- que tengan datos del ultimo periodo (fct) --> Fecha maxima > fecha_maxima_requerida (inicio ultimo periodo)
	- que tengan suficiente historia (fct) --> Fecha minima < fecha_minima_requerida (fin primer periodo)

Se consulta tabla de calidad (ver campos).

- Verificacion de indicadores:
	- Detectar origenes por cada indicador: Consulta BQ --> Lista  
	- Para cada origen se debe chequear que cumpla las condiciones --> alternativa al loop?.
		- Si las condiciones se cumplen, el indicador se corre.
	
Logging?

### Parametria

- conexiones.json: con ubicacion de las tablas de origen e indicadores
- origenes/{tabla_origen}.json: nombre en el dataset, conexion, tipo de tabla

## V1
### Arbol de carpetas y archivos

- parametria
	- conexiones.json: proyecto y dataset para cada conexion (ubicación de origenes, indicadores, etc)
	- directorios.json: ubicaciones de ciertos buckets de referencia
	- origenes/
		(un archivo json por origen)
	- indicadores/
		(un archivo json por indicador)
- queries/	(templates sql para realizar operaciones comunes)
	- verificar_origen.sql
	- borrar_indicador_periodo.sql
	- insertar_indicador_periodo.sql

### Procesos

1. Ejecucion de indicadores del periodo (automatico/manual)
2. Reproceso de indicadores (manual)

### Parametria

- Conexiones: proyecto, dataset
- Origenes: nombre, conexion, tipo, intervalo_periodos_actualizacion (solo fct), 
dias_desde_actualizacion (solo lkp), campo_fecha (solo fct)
- Indicadores: nombre, conexion, estado

### Procesamiento de indicadores

A principio de mes, donde la mayoría de las tablas ya estén disponibles y actualizadas, se puede comenzar 
con la ejecución para el total del listado de indicadores.

NOTA: Para evitar repetir la verificación de origenes que ya se verificaron,
se crea un diccionario con los resultados de verificaciones previas que se consulta previo
a ejecutar una nueva verificación.

### Reproceso automatico
El loop sobre el total de indicadores puede realizarse con una frecuencia a definir 
(puede ser diario o puede ser cada un cierto intervalo de días), 
teniendo en cuenta que la razón por la que los indicadores no se corran debería ser 
principalmente por origenes desactualizados (lo que requiere una acción que no es inmediata) o una falla en
el proceso (en ese caso, una frecuencia diaria o incluso más alta es apropiada).
De todas maneras, esta cloud function puede ser iniciada manualmente.

Para las nuevas corridas se evita reprocesar los indicadores que ya se corrieron gracias a la primera verificacion.
Los origenes se verifican nuevamente dado que pueden haber cambiado las condiciones.

### Funciones

**Ejecutar_indicadores_activos**
(función orquestador)
- Carga lista de indicadores: tomar archivos de parametria (*opcional: cargar_parametria*)
- Loop sobre lista de indicadores:
	- Verificar si el indicador se corrio para el periodo (*verificar_indicador_periodo*)
	- IF se corrio, pasar a siguiente indicador.
	- ELSE IF no se corrio:
		- Identificar origenes del indicador a partir de la query (*identificar_origenes*)
		- Loop sobre los origenes:
			- Verificar si se el origen ya fue chequeado (diccionario con resultados de la verificacion):
			- IF fue chequeado, pasar a siguiente origen
			- ELSE IF  no fue chequeado:
				- Verificar origen (*verificar_origen*)
		- IF algun origen no esta ok, pasar a siguiente indicador
		- ELSE IF todos los origenes están ok:
			- Insertar registros a la tabla del indicador (*correr_indicador*)

**Verificar_indicador_periodo**

Descripción: Verifica si el indicador corrió para el periodo

Argumentos:
- Indicador (str)
- Periodo (int)
- Conexiones (dict)
- Query_verificacion (str)

Return: condicion (int)
- 0: No se corrió
- 1: Se corrió el indicador para ese periodo

Para el indicador se levanta su parametria para saber su conexion.

Se utiliza la parametria para reemplazar en la Query_verificacion (template) 
los parametros propios del indicador y el periodo.

Se conecta a BQ y ejecuta la consulta modificada trayendo como resultado la condición. 

*Pasos intermedios: 
- importar query del indicador
- listar origenes del indicador*

**Verificar_origenes**

Descripción: Verifica si el origen FCT o LKP está actualizado y con los datos necesarios.

Argumentos:
- Origen (str)
- Periodo (int)
- Conexiones (dict)
