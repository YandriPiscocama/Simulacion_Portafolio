"""Genera figuras académicas únicamente desde los CSV medidos."""

import argparse
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--resultados", type=Path, default=ROOT / "resultados")
parser.add_argument("--graficas", type=Path, default=ROOT / "graficas")
args = parser.parse_args()
RESULTS = args.resultados.resolve()
FIGURES = args.graficas.resolve()
FIGURES.mkdir(parents=True, exist_ok=True)


def read_csv(name):
    with (RESULTS / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def save(fig, name):
    fig.savefig(FIGURES / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "figure.figsize": (8, 5)})

table = read_csv("tabla_docente.csv")
if len(table) != 4:
    raise ValueError("La tabla principal debe tener cuatro filas")
n = [int(row["N"]) for row in table]
estimate = [float(row["π estimado"]) for row in table]
error = [float(row["Error"]) for row in table]
python_ms = [float(row["Tiempo Python"]) for row in table]
java_ms = [float(row["Tiempo Java"]) for row in table]


def sample_axis(ax):
    ax.set_xscale("log")
    ax.set_xticks(n, labels=[f"{value:,}".replace(",", " ") for value in n])
    ax.set_xlim(800, 1_250_000)
    ax.grid(axis="y", color="#d7dde3", linewidth=0.7)
    ax.set_xlabel("Tamaño de muestra N (puntos)")


fig, ax = plt.subplots()
ax.plot(n, estimate, "o-", color="#176b9a", linewidth=2, markersize=6, label="Estimación (semilla 42)")
ax.axhline(math.pi, color="#b34c33", linestyle="--", linewidth=1.5, label="π real")
sample_axis(ax)
ax.set_ylabel("Valor estimado de π")
ax.set_title("Convergencia de la estimación de π")
ax.legend(frameon=False)
fig.tight_layout()
save(fig, "convergencia.png")

fig, ax = plt.subplots()
ax.plot(n, error, "o-", color="#b34c33", linewidth=2, markersize=6)
sample_axis(ax)
ax.set_ylim(bottom=0)
ax.set_ylabel("Error absoluto |π estimado − π|")
ax.set_title("Error absoluto frente al tamaño de muestra")
fig.tight_layout()
save(fig, "error.png")

fig, ax = plt.subplots()
ax.plot(n, python_ms, "o-", color="#176b9a", linewidth=2, markersize=6, label="Python")
ax.plot(n, java_ms, "s-", color="#d78921", linewidth=2, markersize=6, label="Java")
sample_axis(ax)
ax.set_yscale("log")
ax.set_ylabel("Tiempo de cálculo (ms, escala logarítmica)")
ax.set_title("Tiempo de cálculo: Python y Java")
ax.legend(frameon=False)
fig.tight_layout()
save(fig, "tiempos.png")

summary_path = RESULTS / "resumen_estadistico.csv"
if summary_path.is_file():
    rows = read_csv("corridas.csv")
    groups = [[float(row["pi_estimado"]) for row in rows
               if row["lenguaje"] == "Python" and int(row["n"]) == size] for size in n]
    if any(len(group) != 20 for group in groups):
        raise ValueError("La gráfica de distribución requiere 20 repeticiones por N")
    fig, ax = plt.subplots()
    ax.boxplot(groups, tick_labels=[f"{value:,}".replace(",", " ") for value in n],
               patch_artist=True, boxprops={"facecolor": "#d5e8f3", "edgecolor": "#176b9a"},
               medianprops={"color": "#b34c33", "linewidth": 2},
               whiskerprops={"color": "#176b9a"}, capprops={"color": "#176b9a"})
    ax.axhline(math.pi, color="#555555", linestyle="--", linewidth=1.2, label="π real")
    ax.set_xlabel("Tamaño de muestra N (puntos)")
    ax.set_ylabel("Estimación de π")
    ax.set_title("Variabilidad en 20 semillas emparejadas (42–61)")
    ax.grid(axis="y", color="#d7dde3", linewidth=0.7)
    ax.legend(frameon=False)
    fig.tight_layout()
    save(fig, "distribucion.png")
else:
    (FIGURES / "distribucion.png").unlink(missing_ok=True)

print("Gráficas generadas desde CSV:", ", ".join(path.name for path in sorted(FIGURES.glob("*.png"))))
