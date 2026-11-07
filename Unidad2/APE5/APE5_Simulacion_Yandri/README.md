# APE 5 — Generador Congruencial Lineal en Python y Java

Práctica de Simulación de Sistemas de la Universidad Nacional de Loja. Se usa la numeración 05 de Datos generales de la guía.

Desde la raíz del proyecto, en PowerShell y con Python 3.12 y un JDK disponibles:

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
javac -source 8 -target 8 -d java/build java/src/LCG.java
foreach ($semilla in 12345, 42) {
    python python/src/lcg.py $semilla "data/python_$semilla.csv"
    java -cp java/build LCG $semilla "data/java_$semilla.csv"
}
python python/src/analisis.py
python -m unittest discover -s python/tests -v
```

En Linux o macOS, activa el entorno con `source .venv/bin/activate` y ejecuta los generadores una vez por cada semilla. Si el lanzador Java de Windows falla, usa la ruta directa a `java.exe` y define `APE5_JAVA` con esa ruta para la suite.

- [Especificación](docs/especificacion.md)
- [Primeras 20 observaciones](results/tables/primeras_20.csv)
- [Comparación de semillas](results/tables/comparacion_semillas.csv)
- [Gráfica](results/figures/secuencia_lcg.png)
- [Período y semilla](docs/analisis_periodo.md)
- [Preguntas de control](docs/preguntas_control.md)
