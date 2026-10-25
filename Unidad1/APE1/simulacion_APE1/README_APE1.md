# APE 01 — Construcción y simulación computacional de un modelo matemático

Práctica 01 de **Simulación**, orientada a la construcción e implementación de un modelo matemático para analizar la posibilidad de lluvia a partir de datos de humedad, nubosidad y temperatura.

La implementación se desarrolló en **Python** utilizando una organización **Modelo–Vista–Controlador (MVC)**. El programa procesa los datos climáticos, calcula el índice de lluvia, clasifica el resultado y genera gráficas con **Matplotlib** para comparar el modelo original y el modelo ajustado.

## Descripción

El modelo original utiliza la expresión:

```text
I = 0.5H + 0.3N + 0.2Tf
```

donde:

- `H` representa la humedad normalizada.
- `N` representa la nubosidad normalizada.
- `Tf` representa el factor de temperatura.
- `I` representa el índice calculado por el modelo.

Durante la práctica también se realizó un ajuste de los coeficientes, manteniendo como condición que su suma sea igual a 1:

```text
I = 0.60H + 0.25N + 0.15Tf
```

Esto permitió comparar el comportamiento del modelo original con una segunda configuración.

## Características

- Procesamiento de datos de humedad, nubosidad y temperatura.
- Normalización de los valores de humedad y nubosidad.
- Obtención del factor de temperatura `Tf`.
- Cálculo del índice de lluvia.
- Clasificación de los resultados según el valor obtenido.
- Ejecución del modelo original.
- Ejecución de un modelo con coeficientes ajustados.
- Comparación de los resultados obtenidos.
- Generación de gráficas mediante Matplotlib.
- Organización del proyecto utilizando MVC.

## Arquitectura

```text
main.py
   │
   ▼
Controller
   │
   ▼
Model
   │
   ├── Normalización de datos
   ├── Cálculo de Tf
   ├── Cálculo del índice
   └── Clasificación
   │
   ▼
View
   │
   ├── Presentación de resultados
   └── Gráficas con Matplotlib
```

La arquitectura separa las responsabilidades principales del programa:

- **Model:** contiene los datos y cálculos del modelo matemático.
- **Controller:** coordina el procesamiento de los registros y la ejecución del modelo.
- **View:** presenta los resultados y genera las gráficas.
- **main.py:** funciona como punto de entrada de la aplicación.

## Estructura del proyecto

```text
APE1/
├── main.py
├── requirements.txt
├── .gitignore
├── model/
├── controller/
└── view/
```

> Los nombres internos de los archivos pueden variar según la organización utilizada en el proyecto.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd APE1
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

Al ejecutar el programa se deben obtener los resultados correspondientes al modelo original y al modelo ajustado.

El programa permite observar:

- los valores calculados del índice;
- la clasificación obtenida para cada registro;
- el comportamiento del modelo original;
- el comportamiento del modelo ajustado;
- la comparación gráfica entre ambas configuraciones.

El ajuste de los coeficientes permite analizar cómo cambia el resultado cuando se modifica la importancia asignada a cada variable.

## Modelo original y modelo ajustado

### Modelo original

```text
I = 0.5H + 0.3N + 0.2Tf
```

### Modelo ajustado

```text
I = 0.60H + 0.25N + 0.15Tf
```

En ambos casos, la suma de los coeficientes es igual a 1.


### Prompts representativos utilizados

1. `Analiza la estructura del proyecto y verifica si está organizada correctamente.`
2. `Refactoriza la redacción manteniendo la idea original y un lenguaje sencillo.`
3. `Explica de forma sencilla el comportamiento del modelo y los resultados obtenidos.`
