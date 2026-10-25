# APE 02 — Comparación de modelos determinísticos, estocásticos, discretos y continuos

Práctica 02 de **Simulación**, orientada a comparar diferentes paradigmas de modelado mediante un sistema de crecimiento poblacional.

La implementación se desarrolló en **Python** utilizando una organización **Modelo–Vista–Controlador (MVC)**. El programa ejecuta cuatro modelos —determinístico, discreto, estocástico y continuo mediante Euler— y genera gráficas individuales y una comparación general utilizando **Matplotlib**.

## Descripción

La práctica permite observar cómo cambia el comportamiento de una población dependiendo del tipo de modelo utilizado.

Se implementaron cuatro enfoques:

- modelo determinístico;
- modelo discreto;
- modelo estocástico;
- modelo continuo mediante el método de Euler.

Cada uno utiliza los mismos parámetros generales de simulación, pero representa el crecimiento de manera diferente.

## Características

- Implementación de cuatro modelos de crecimiento poblacional.
- Modelo determinístico mediante crecimiento exponencial.
- Modelo discreto por períodos definidos.
- Modelo estocástico con incorporación de ruido aleatorio.
- Modelo continuo aproximado mediante el método de Euler.
- Uso de `r` como tasa de crecimiento.
- Uso de `sigma` como nivel de variabilidad del modelo estocástico.
- Uso de `dt` como tamaño del paso del modelo continuo.
- Generación de una gráfica individual para cada modelo.
- Generación de una gráfica comparativa.
- Organización del proyecto utilizando MVC.

## Arquitectura

```text
main.py
   │
   ▼
Controller
   │
   ├────────► Modelo determinístico
   ├────────► Modelo discreto
   ├────────► Modelo estocástico
   └────────► Modelo continuo
   │
   ▼
View
   │
   ├── Gráficas individuales
   └── Gráfica comparativa
```

La arquitectura separa las responsabilidades principales del programa:

- **Model:** contiene la lógica matemática de cada uno de los cuatro modelos.
- **Controller:** ejecuta los modelos con los parámetros definidos y organiza los resultados.
- **View:** representa los resultados mediante gráficas con Matplotlib.
- **main.py:** funciona como punto de entrada del programa.

## Estructura del proyecto

```text
simulacion_modelos/
├── main.py
├── requirements.txt
├── controller/
│   └── simulacion_controller.py
├── model/
│   ├── modelo_deterministico.py
│   ├── modelo_discreto.py
│   ├── modelo_estocastico.py
│   └── modelo_continuo.py
└── view/
    └── vista_simulacion.py
```

## Modelos implementados

### Modelo determinístico

Utiliza un crecimiento exponencial:

```text
P(t) = P0 × e^(r × t)
```

Al no incorporar aleatoriedad, los mismos parámetros de entrada producen siempre los mismos resultados.

### Modelo discreto

La población se actualiza por períodos:

```text
P_nuevo = P_actual + r × P_actual
```

El cambio se calcula a partir de la población obtenida en el período anterior.

### Modelo estocástico

Incorpora un componente aleatorio:

```text
P_nuevo = P_actual + r × P_actual + ruido
```

El valor del ruido se genera mediante una distribución normal y su variabilidad está relacionada con el parámetro `sigma`.

### Modelo continuo mediante Euler

Se utiliza una aproximación numérica mediante el método de Euler:

```text
P_nuevo = P_actual + dt × (r × P_actual)
```

El parámetro `dt` define el tamaño del paso utilizado para calcular valores intermedios durante la simulación.

## Parámetros utilizados

Durante las pruebas del proyecto se utilizaron los siguientes valores:

```text
P0 = 1000
r = 0.1
tiempo = 6
sigma = 50
dt = 0.5
```

Donde:

- `P0` representa la población inicial.
- `r` representa la tasa de crecimiento.
- `tiempo` representa la duración total de la simulación.
- `sigma` representa el nivel de variabilidad del modelo estocástico.
- `dt` representa el tamaño del paso utilizado en el método de Euler.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd simulacion_modelos
```

Reemplaza `URL_DEL_REPOSITORIO` por el enlace correspondiente del repositorio.

### 2. Crear el entorno virtual

#### Linux / Ubuntu / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

Cuando el entorno virtual esté activo normalmente aparecerá `(.venv)` al inicio de la terminal.

### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Las principales librerías utilizadas en esta práctica son:

- NumPy
- Matplotlib

### 4. Ejecutar el programa

```bash
python main.py
```

En Linux también puede utilizarse:

```bash
python3 main.py
```

## Comprobación de resultados

Al ejecutar el programa se generan las gráficas correspondientes a:

- modelo determinístico;
- modelo discreto;
- modelo estocástico;
- modelo continuo mediante Euler;
- comparación de los cuatro modelos.

Las gráficas permiten observar las diferencias entre los modelos, la influencia de la tasa de crecimiento `r`, el efecto de la aleatoriedad en el modelo estocástico y el comportamiento del método de Euler mediante el parámetro `dt`.
