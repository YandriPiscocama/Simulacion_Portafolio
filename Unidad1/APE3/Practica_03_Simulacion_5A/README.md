# Simulador M/M/1 — Vista Web

Práctica 03 de **Simulación de un sistema de líneas de espera M/M/1 mediante SimPy**.

La versión final usa una **vista web local**, una paleta visual azul y una animación interactiva de la cola. La lógica continúa separada mediante **MVC** y patrones básicos de diseño.

## Características

- Tres escenarios fijos definidos por la práctica:
  - Escenario 1: λ = 2.0, μ = 3.0.
  - Escenario 2: λ = 2.5, μ = 3.0.
  - Escenario 3: λ = 2.9, μ = 3.0.
- El usuario solo indica **N**, número de repeticiones.
- En cada repetición se genera automáticamente **una semilla**, compartida por los tres escenarios.
- Los resultados se calculan y mantienen **en memoria**; no se crean CSV ni archivos de resultados.
- Tabla comparativa con:
  - ρ
  - L
  - Lq
  - W
  - Wq
  - tiempo promedio de espera simulado
  - tamaño promedio de cola simulado
- Gráficas de:
  - comportamiento de la cola en el tiempo;
  - tiempo de espera en el tiempo;
  - ρ observado y teórico relacionado con tiempo de espera y tiempo de ejecución/servicio.
- Animación web conceptual en cuatro etapas: llegada → cola FIFO → atención → salida.
- Patrones utilizados:
  - **Strategy** para las métricas teóricas M/M/1;
  - **Factory** para los escenarios fijos.


## Estructura del proyecto

```text
SIMULACION/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
├── src/
│   ├── analyzers/
│   │   └── result_analyzer.py
│   ├── controllers/
│   │   └── simulation_controller.py
│   ├── models/
│   │   └── mm1_model.py
│   ├── patterns/
│   │   ├── scenario_factory.py
│   │   └── theory_strategy.py
│   └── views/
│       └── chart_view.py

```

# Cómo clonar y ejecutar

## 1. Clonar el repositorio

Reemplaza `URL_DEL_REPOSITORIO` por el enlace real de GitHub:

```bash
git clone URL_DEL_REPOSITORIO
cd SIMULACION
```

## 2. Crear el entorno virtual

### Linux 

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cuando el entorno esté activo normalmente aparecerá `(.venv)` al inicio de la terminal.

## 3. Actualizar pip e instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Ejecutar la aplicación

```bash
python3 app.py
```

Después abre en el navegador:

```text
http://127.0.0.1:5000
```

Para detener el servidor usa `Ctrl + C` en la terminal.
