# APE 6 — Validación estadística de números pseudoaleatorios

Esta carpeta contiene la entrega independiente de la APE 6 de Simulación. Se generan números mediante un generador congruencial lineal (LCG) y se evalúa su compatibilidad con U(0,1) mediante Chi-cuadrado y Kolmogorov-Smirnov.

## Tecnologías

- Python 3.12, NumPy, SciPy y Matplotlib.
- Java/JDK para la segunda implementación del LCG.
- CSV para el intercambio y la comparación de secuencias.

## Preparar Python

Desde esta carpeta:

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r python/requirements.txt
```

La carpeta `.venv` es local y no forma parte de la entrega distribuible.

## Ejecutar los generadores

Configuración A:

```powershell
python python/src/lcg.py --output data/lcg_python.csv > $null
javac -source 8 -target 8 -d java/build java/src/LCG.java
java -cp java/build LCG --output data/lcg_java.csv > $null
```

Configuración B:

```powershell
python python/src/lcg.py --seed 42 --a 1 --c 1 --m 256 --n 10000 --output data/lcg_b_python.csv > $null
javac -source 8 -target 8 -d java/build java/src/LCG.java
java -cp java/build LCG --seed 42 --a 1 --c 1 --m 256 --n 10000 --output data/lcg_b_java.csv > $null
```

Los parámetros `--seed`, `--a`, `--c`, `--m`, `--n` y `--output` son configurables. La semilla X0 no se exporta; se guardan 10 000 estados y sus valores normalizados.

## Ejecutar Chi-cuadrado y KS

```powershell
python python/src/estadisticas.py --input data/lcg_python.csv --results results
python python/src/estadisticas.py --input data/lcg_b_python.csv --results results/configuracion_b
```

Las pruebas usan α=0,05, diez intervalos para Chi-cuadrado y la distribución uniforme U(0,1) para KS.

## Ejecutar pruebas

```powershell
python -m unittest discover -s python/tests -v
```

Las pruebas verifican los generadores, las estadísticas, la reproducibilidad, el período de la configuración B y la coincidencia entre Python y Java.

## Resultados

- `data/`: secuencias CSV de las configuraciones A y B.
- `results/tables/`: tablas estadísticas de A y comparación A vs. B.
- `results/figures/`: gráficas de A.
- `results/configuracion_b/`: tablas y gráficas de B.
- `informe/`: evidencias experimentales y espacio reservado para el informe institucional posterior.

Los resultados incluidos fueron generados previamente y se conservan separados por configuración. No se incluye todavía el documento Word institucional.

## Estimación de π por Monte Carlo

Esta ampliación completa la tabla de la sección 6. Se usan dos valores consecutivos de la configuración A por punto y se estima π como cuatro veces la proporción de puntos dentro del cuarto de círculo unitario. Los tiempos, en segundos, son medianas de cinco repeticiones tras el calentamiento y dependen del equipo y del entorno.

Desde la raíz de la entrega, en PowerShell, con Python y el JDK disponibles:

```powershell
javac -source 8 -target 8 -d java/build java/src/LCG.java java/src/EstimacionPi.java
java -cp java/build EstimacionPi --repetitions 5 --output results/reproduccion_pi/java.csv --counts-output results/reproduccion_pi/conteos_java.csv
python python/src/estimacion_pi.py --repetitions 5 --java-results results/reproduccion_pi/java.csv --output results/reproduccion_pi/comparacion_pi.csv --counts-output results/reproduccion_pi/conteos_python.csv
python -m unittest discover -s python/tests -v
```

Si el lanzador `java` del PATH falla, ejecuta directamente el `java.exe` del JRE o JDK instalado. Los comandos guardan la nueva medición en `results/reproduccion_pi/`. La medición entregada, el CSV de Java y los dos archivos de conteos están en `results/tables/`.
