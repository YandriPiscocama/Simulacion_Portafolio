# Preguntas de control de la APE 5

1. **¿Qué significa pseudoaleatorio?** Una secuencia pseudoaleatoria se obtiene con un algoritmo determinista diseñado para imitar algunas propiedades de una secuencia aleatoria. Con los mismos parámetros y semilla se repite exactamente.
2. **¿Qué función cumple la semilla?** Define el estado inicial. En este generador de período completo selecciona el punto de partida del mismo ciclo.
3. **¿Qué significa período?** Es el menor número positivo de pasos que devuelve el generador al mismo estado dentro del ciclo. A partir de ese estado se repiten las salidas.
4. **¿Qué ocurre si se utilizan parámetros inadecuados?** Pueden aparecer ciclos cortos o patrones pronunciados. Por ejemplo, con a=1 y c=0 el estado se mantiene fijo para cualquier semilla.
5. **¿Qué ventaja tiene implementar el mismo algoritmo en dos lenguajes?** La comparación permite verificar reproducibilidad y detectar diferencias de aritmética, normalización o exportación entre plataformas.
