# APE7: estimación de π mediante Monte Carlo

Implementación de la práctica APE7 de Simulación en Python y Java. Ambos programas usan el mismo generador congruencial lineal (LCG), consumen dos valores por punto y calculan `π estimado = 4 × Nc / N`. Para una misma semilla producen el mismo contador `Nc` y la misma estimación.

## Requisitos

- Python 3.12 o posterior.
- JDK 21 para compilar y ejecutar Java.
- Windows PowerShell para `ejecutar_experimentos.ps1`.
- Matplotlib para generar las gráficas. El núcleo y los ejecutables de la simulación usan solamente la biblioteca estándar de Python y Java.

Desde esta carpeta, instalar la dependencia de las gráficas:

```powershell
python -m pip install -r .\requirements.txt
```

El archivo `requirements.txt` contiene solo Matplotlib. No se necesita NumPy como dependencia directa ni bibliotecas para redactar informes.

## Demostración automática

Este comando localiza el JDK, compila Java, ejecuta Python y Java con semilla 42 para `N = 1000, 10000, 100000 y 1000000`, verifica `Nc` y π entre lenguajes, muestra dos tablas y guarda tres gráficas:

```powershell
.\ejecutar_experimentos.ps1 -Graficas
```

Los datos nuevos van a `demostracion/resultados/` y las imágenes nuevas a `demostracion/graficas/`. El script muestra el progreso durante la ejecución. Para obtener también la cuarta gráfica, de distribución entre 20 semillas emparejadas:

```powershell
.\ejecutar_experimentos.ps1 -Repeticiones 20 -Graficas
```

Esta ampliación puede tardar alrededor de 1 a 2 minutos en el equipo usado para preparar la práctica. El tiempo depende del equipo y su carga. Si Python o el JDK están en otra ubicación, use `-PythonExe`, `-JavacExe` y `-JavaExe` con las rutas de sus ejecutables.

## Ejecución directa

```powershell
python .\python\monte_carlo_pi.py 1000 42
New-Item -ItemType Directory -Force .\java\build | Out-Null
javac -d .\java\build .\java\MonteCarloCore.java .\java\MonteCarloPi.java
java -cp .\java\build MonteCarloPi 1000 42
```

Las últimas dos órdenes requieren que `javac` y `java` del mismo JDK estén en `PATH`. La semilla es el segundo argumento; si se omite, ambos programas usan 42. La comprobación de referencia con `N=1000` y semilla 42 es `Nc=773` y `π estimado=3.092` en ambos lenguajes.

## Pruebas y datos

```powershell
python -m unittest discover -s .\tests -p 'test_*.py' -v
python .\tests\validar_resultados.py
```

La suite de pruebas requiere `javac` en `PATH`. `resultados/` contiene las 160 corridas históricas, la tabla de cinco columnas y el resumen estadístico; `graficas/` contiene las cuatro figuras derivadas de esos CSV. Los tiempos históricos pertenecen a la ejecución de la fase 3; para medir la versión actual utilice el ejecutor de demostración. Este último escribe solo en `demostracion/`, carpeta excluida por `.gitignore`.

## Organización

```text
python/      LCG, modelo matemático y programa de terminal
java/        LCG, modelo matemático y programa de terminal
tests/       pruebas, ejecutor, auditoría de CSV y generador de gráficas
resultados/  CSV históricos verificados
graficas/    figuras históricas generadas desde los CSV
```

Las responsabilidades de cada módulo se explican en [ARQUITECTURA.md](ARQUITECTURA.md).
