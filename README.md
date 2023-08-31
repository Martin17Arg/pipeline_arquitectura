# Arquitectura

## V3

1. Identificar fecha y periodo
	- Fecha ejecucion: desde workflow
	- Periodo: desde cloud function o expresion (mas compleja) de workflow	

``` yaml
- assignments:
  - fecha_ejecucion: ${text.substring(time.format(sys.now()),0,10)} # YYYY-MM-DD
```

2. Verificación de origenes

- Inputs:
	1. Parametria de origenes (json): listado de origenes y requisitos de validacion
	2. Tabla de calidad de origenes (BQ): tabla con registros de subidas de origenes
	3. Conexiones: ubicación de los distintos dataset

**Parametria de origenes:**

``` json
["bm_saldos": {
	"nombre_dataset": "fct_saldos"
	,"conexion": "dw"
	,"periodos_necesarios": 12
	},
"bm_clientes": { 
	"nombreDataset": "lkp_clientes"
	,"conexion": "dw"
	,"max_dias_desde_actualizacion": 30
	}
]
```

**Tabla de indicadores corridos**

| Indicador | Periodo |
| :-  | :-: |
| flag_td | 202306 |
| cli_convenio | 202306 |

**Conexiones:**

``` json
["dw": {
	"proyecto": "bm-gcp-t1-ml"
	,"dataset": "pre_stage"
	},
"ind": {
	"proyecto": "bm-gcp-t1-ml"
	,"dataset": "post_stage"
	}
]
```

- Pasos:
	- La parametria se incorpora a BQ para joinear con la tabla de calidad.
	- A través de un conector a BQ en workflow se ejecuta una query que devuelva la lista de origenes validados.

- Return:
	- Lista de origenes validados

3. Verificación de indicadores ya corridos para el periodo.
	- Inputs:
		- Tabla con indicadores-periodo corridos satisfactoriamente
		- Lista de indicadores a correr para el periodo (indicadores activos)
	- Pasos:
		- Consulta a tabla de indicadores corridos para el periodo actual.
		- Filtrar de la lista de indicadores a correr los que ya se corrieron (de acuerdo a la consulta previa)
	- Return:
		- Lista de indicadores que aún no se corrieron para el periodo.

*NOTA: pasos 1 y 2 se pueden paralelizar*

4. Ejecución de indicadores
	- Inputs:
		- Lista de indicadores que aún no se corrieron (paso 2)
		- Lista de origenes validados (paso 1)
		- Conexiones
		- Query (traida desde GCS)
	- Pasos:
		- Importar query desde GCS
		- Identificar origenes (buscar en la query strings que comienzen con "pre_stage.*" [version actual])
			- Realizarlo con Cloud function
		- Validar que todas esas strings estén en la lista de origenes validados.
		- Condición: 
			- si alguno de los origenes no está en la tabla de validados, cortar la ejecución del indicador
			- Si todos los origenes están validados, continuar.
		- Reemplazar en la query origenes con los nombres reales de las tablas de origen 
		(de acuerdo a parametria de origenes y conexiones)
 		- Ejecutar indicador (insert) a partir de la query modificada


## Ejemplos:

### 3.1


