SELECT IF(COUNT(Codigo_cliente)>0,0,1) as condicion
FROM {proyecto}.{dataset}.measure_{indicador}
WHERE periodo = {periodo}
