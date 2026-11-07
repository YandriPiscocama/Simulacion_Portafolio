# Especificación APE 5

La guía de la semana 5 identifica la práctica como N.º 05 en Datos generales, aunque el encabezado dice N.º 004.

La generación principal usa semilla 12345, a=1664525, c=1013904223, m=4294967296 y N=10000. La segunda ejecución cambia únicamente la semilla a 42. El índice 1 representa el primer estado calculado después de la semilla.

Cada programa exporta índice, estado y cociente exacto X/m con 32 decimales, separador coma, UTF-8 y salto LF. El análisis exige igualdad de los CSV completos por semilla y exporta dos tablas de 20 filas y una figura con la secuencia principal completa y un detalle de sus primeras 100 observaciones.

La aceptación comprueba cantidad, recurrencia, normalización, reproducibilidad, casos de referencia y coincidencia entre lenguajes. El período se justifica con Hull–Dobell.
