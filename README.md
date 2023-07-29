# Arquitectura

### Arbol de carpetas y archivos

- parametria
	- origenes
		(un archivo por origen)
- queries
	(templates sql para realizar operaciones comunes)

### Arbol de funciones

1. Ejecucion de todos los indicadores del periodo (ejecucion automatica a tiempo fijo)
	1. Carga de parametria general
	Loop sobre el total de indicadores:
		2. Verificacion de origenes
		3. Ejecucion del indicador
2. Reproceso de indicadores (manual)

### Parametria

- Conexiones: proyecto, dataset
- Origenes: nombre, conexion, tipo, intervalo_periodos_actualizacion (solo fct), 
dias_desde_actualizacion (solo lkp), campo_fecha (solo fct)
- Indicadores: nombre, conexion, estado

A principio de mes, cuando la mayoría de las tablas ya estén disponibles se puede comenzar 
con la ejecución para el total del listado de indicadores.

Esto se puede realizar con una funcion cuyo objetivo sea tomar todos los indicadores activos 
y comenzar un loop sobre ese listado.
Previo a ese loop se puede cargar la parametria general.

El loop comprende:
- Carga de la parametria del indicador
- Verificacion de origenes, identificados a partir de la query del indicador. 
Esta verificacion debe tener como argumento tambien la parametria del origen.

NOTA: Para evitar repetir la verificación de origenes que ya se verificaron,
se crea un diccionario con los resultados de verificaciones previas que se consulta previo
a ejecutar una nueva verificación.



Para las nuevas corridas
