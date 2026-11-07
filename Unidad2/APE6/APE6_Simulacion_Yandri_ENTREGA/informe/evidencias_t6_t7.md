# Evidencias T6 y respuestas de control T7

## Experimento y comparación

Se generaron 10 000 valores por configuración, con α=0,05. Ambas implementaciones exportaron CSV idénticos por configuración. Para A se conservaron los datos y resultados anteriores; para B se usaron archivos independientes. La comparación completa está en `results/tables/comparacion_a_b.csv`.

| Configuración | Semilla | a | c | m | χ² | p χ² | D KS | p KS | Decisión en ambas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 42 | 1664525 | 1013904223 | 4294967296 | 9,758 | 0,3704295 | 0,0125061 | 0,0868668 | No se rechaza H₀ |
| B | 42 | 1 | 1 | 256 | 3,708 | 0,9295594 | 0,0051375 | 0,9532291 | No se rechaza H₀ |

B avanza por estados consecutivos módulo 256. Como se suma 1 módulo 256, recorre los 256 estados antes de repetirse: su período es 256, por lo que la muestra de 10 000 contiene ciclos repetidos. Se eligió como contraste explícito de A, no como generador recomendado. Aunque B obtuvo valores p mayores, eso no demuestra que sea mejor: las pruebas aquí examinan ajuste marginal a uniformidad, no independencia ni imprevisibilidad. La calibración habitual de sus valores p presupone observaciones independientes; además, los valores LCG son discretos y deterministas.

**Archivos de evidencia:**
- Datos A: `data/lcg_python.csv`, `data/lcg_java.csv`; datos B: `data/lcg_b_python.csv`, `data/lcg_b_java.csv`.
- Tablas A: `results/tables/chi_cuadrado.csv`, `results/tables/estadisticos.csv`; tablas B: `results/configuracion_b/tables/`.
- Figuras A: `results/figures/`; figuras B: `results/configuracion_b/figures/`.
- Comparación de los CSV: SHA-256 A `742235ac0fc79610581285755f4b5c32403ea99c912364e485cd9cb5e41750f8`; B `6dc689158e2ca0af13d0cb1c050c858c4d416d43508d9ae8e543fa65073bf2b7`. Los dos lenguajes coinciden byte por byte en cada configuración.

## Preguntas de control

1. **¿Qué es la hipótesis nula?** Es la afirmación de referencia que se somete a contraste; aquí se plantea que la distribución de los valores es uniforme U(0,1).
2. **¿Qué representa el valor p?** Bajo H₀ y los supuestos de la prueba, es la probabilidad de observar un estadístico al menos tan extremo como el obtenido. No es la probabilidad de que H₀ sea verdadera.
3. **¿Qué significa rechazar H₀?** Que el resultado es suficientemente incompatible con H₀, según el criterio y nivel α elegidos; aquí se rechaza cuando p<0,05. La decisión está sujeta a los supuestos y a la posibilidad de error.
4. **¿Qué diferencia existe entre Chi-cuadrado y KS?** Chi-cuadrado compara frecuencias observadas y esperadas por intervalos; KS mide la máxima diferencia entre las funciones acumuladas empírica y teórica sin agrupar en intervalos.
5. **¿Por qué una prueba estadística no demuestra que un generador sea verdaderamente aleatorio?** Porque analiza propiedades concretas de una muestra finita y puede no detectar otros defectos. Un LCG es determinista; por ejemplo, B recorre estados consecutivos y repite cada 256, pese a no rechazar H₀ en estas pruebas.

La plantilla institucional no está incluida; la adaptación del informe corresponde a T8 y permanece pendiente.
