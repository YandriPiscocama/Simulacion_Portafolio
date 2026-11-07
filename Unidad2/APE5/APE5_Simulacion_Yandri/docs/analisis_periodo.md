# Período y efecto de la semilla

El teorema de Hull–Dobell establece tres condiciones para que un LCG mixto tenga período completo:

1. El incremento y el módulo son coprimos. Como 1013904223 es impar y 4294967296 = 2³², su máximo común divisor es 1.
2. Cada factor primo del módulo divide a − 1. El único factor primo es 2 y 1664524 es par.
3. Si el módulo es múltiplo de 4, entonces a − 1 también debe serlo. Aquí 1664524 = 4 × 416131.

Se cumplen las tres condiciones. El período es 4294967296 estados para ambas semillas y se deduce sin recorrer el ciclo.

Con semilla 12345 el primer estado es 87628868. Con semilla 42 es 1083814273. Como todos los estados pertenecen a un único ciclo, cambiar la semilla cambia el punto de partida, conservando el período. Una semilla fija permite repetir la secuencia. El período completo por sí solo no garantiza independencia.
