import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def save(path, header, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def main():
    sequences = {}
    for seed in (12345, 42):
        python_csv = ROOT / f"data/python_{seed}.csv"
        java_csv = ROOT / f"data/java_{seed}.csv"
        if python_csv.read_bytes() != java_csv.read_bytes():
            raise ValueError(f"Los CSV difieren para la semilla {seed}")
        sequences[seed] = read(python_csv)
        if len(sequences[seed]) != 10000:
            raise ValueError(f"Cantidad incorrecta para la semilla {seed}")
    primary, secondary = sequences[12345], sequences[42]
    tables = ROOT / "results/tables"
    figures = ROOT / "results/figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    save(tables / "primeras_20.csv",
         ("indice", "estado_python", "uniforme_python", "estado_java", "uniforme_java", "coincide"),
         ((p["indice"], p["estado"], p["uniforme"], j["estado"], j["uniforme"], "Sí" if p == j else "No")
          for p, j in zip(primary[:20], read(ROOT / "data/java_12345.csv")[:20])))
    save(tables / "comparacion_semillas.csv",
         ("indice", "estado_12345", "uniforme_12345", "estado_42", "uniforme_42"),
         ((p["indice"], p["estado"], p["uniforme"], s["estado"], s["uniforme"])
          for p, s in zip(primary[:20], secondary[:20])))
    values = [float(row["uniforme"]) for row in primary]
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), layout="constrained")
    fig.suptitle("APE 5 · Secuencia del generador congruencial lineal")
    axes[0].scatter(range(1, 10001), values, s=2, alpha=.35, label="Semilla 12345")
    axes[0].set_title("Secuencia completa")
    axes[1].plot(range(1, 101), values[:100], ".-", lw=.8, ms=3, label="Semilla 12345")
    axes[1].set_title("Detalle de las primeras 100 observaciones")
    for ax in axes:
        ax.set(xlabel="Índice de observación", ylabel="Valor uniforme", ylim=(0, 1))
        ax.legend(loc="upper right")
        ax.grid(alpha=.2)
    fig.savefig(figures / "secuencia_lcg.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
