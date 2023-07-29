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
		1. Verificar si el indicador ya no se corrió para el periodo (si se corrió, se saltea)
		2. Verificacion de origenes del indicador (deducidos a partir del texto de la query del indicador)
		3. Ejecucion del indicador
2. Reproceso de indicadores (manual)

### Parametria

- Conexiones: proyecto, dataset
- Origenes: nombre, conexion, tipo, intervalo_periodos_actualizacion (solo fct), 
dias_desde_actualizacion (solo lkp), campo_fecha (solo fct)
- Indicadores: nombre, conexion, estado

### Procesamiento de indicadores

A principio de mes, donde la mayoría de las tablas ya estén disponibles y actualizadas, se puede comenzar 
con la ejecución para el total del listado de indicadores.

Esto se puede realizar con una funcion cuyo objetivo sea tomar todos los indicadores activos 
y comenzar un loop sobre ese listado.

Previo a ese loop se carga la parametria general.

El loop comprende:
- Verificar que el indicador no se corrio ya para ese periodo
- Carga de la parametria del indicador
- Verificacion de origenes, identificados a partir de la query del indicador. 
Esta verificacion debe tener como argumento tambien la parametria del origen.

NOTA: Para evitar repetir la verificación de origenes que ya se verificaron,
se crea un diccionario con los resultados de verificaciones previas que se consulta previo
a ejecutar una nueva verificación.

### Reproceso automatico
El loop sobre el total de indicadores puede realizarse con una frecuencia a definir 
(puede ser diario, puede ser cada un cierto intervalo de días), 
teniendo en cuenta que la razón por la que los indicadores no se corran debería ser 
principalmente por origenes desactualizados (lo que requiere una acción que no es inmediata) o una falla en
el proceso (en ese caso, una frecuencia diaria o incluso más alta es apropiada).
De todas maneras, esta cloud function puede ser iniciada manualmente.

Para las nuevas corridas se evita reprocesar los indicadores que ya se corrieron gracias a la primera verificacion.
Los origenes se verifican nuevamente dado que pueden haber cambiado las condiciones.

### Funciones

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
 
