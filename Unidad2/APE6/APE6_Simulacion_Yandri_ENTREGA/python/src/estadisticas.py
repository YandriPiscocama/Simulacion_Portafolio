"""Pruebas de uniformidad sobre un CSV producido por el generador LCG."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

ALPHA = 0.05


def leer_csv(path):
    values = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "uniforme" not in reader.fieldnames:
            raise ValueError("El CSV debe contener la columna uniforme")
        for line, row in enumerate(reader, 2):
            try:
                value = Decimal(row["uniforme"])
                if not value.is_finite() or not Decimal(0) <= value <= Decimal(1):
                    raise ValueError
            except (InvalidOperation, TypeError, ValueError):
                raise ValueError(f"Valor uniforme inválido en línea {line}") from None
            values.append(value)
    if not values:
        raise ValueError("La muestra está vacía")
    return values


def chi_cuadrado(values):
    if not values:
        raise ValueError("La muestra está vacía")
    observed = [0] * 10
    for value in values:
        if not value.is_finite() or not Decimal(0) <= value <= Decimal(1):
            raise ValueError("Valores deben estar en [0,1]")
        # Comparación decimal exacta: cada frontera pertenece a la clase derecha.
        index = next((i for i in range(9) if value < Decimal(i + 1) / 10), 9)
        observed[index] += 1
    expected = len(values) / 10
    statistic = sum((count - expected) ** 2 / expected for count in observed)
    return observed, expected, statistic, float(stats.chi2.sf(statistic, df=9))


def kolmogorov_smirnov(values):
    if not values:
        raise ValueError("La muestra está vacía")
    if any(not v.is_finite() or not Decimal(0) <= v <= Decimal(1) for v in values):
        raise ValueError("Valores deben estar en [0,1]")
    ordered = np.sort(np.asarray([float(v) for v in values]))
    n = len(ordered)
    positions = np.arange(1, n + 1)
    d_plus = float(np.max(positions / n - ordered))
    d_minus = float(np.max(ordered - (positions - 1) / n))
    d = max(d_plus, d_minus)
    return ordered, d_plus, d_minus, d, float(stats.kstwo.sf(d, n))


def decision(p):
    return "Se rechaza H0" if p < ALPHA else "No se rechaza H0"


def ejecutar(input_path, result_dir):
    values = leer_csv(input_path)
    observed, expected, chi, p_chi = chi_cuadrado(values)
    ordered, d_plus, d_minus, d, p_ks = kolmogorov_smirnov(values)
    result_dir = Path(result_dir)
    tables = result_dir / "tables"
    figures = result_dir / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    with (tables / "chi_cuadrado.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["intervalo", "observada", "esperada"])
        for i, count in enumerate(observed):
            label = f"[{i/10:.1f},{(i+1)/10:.1f}{']' if i == 9 else ')'}"
            writer.writerow([label, count, expected])
    with (tables / "estadisticos.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["prueba", "n", "estadistico", "valor_p", "alfa", "decision", "gl", "d_mas", "d_menos"])
        writer.writerow(["Chi-cuadrado", len(values), chi, p_chi, ALPHA, decision(p_chi), 9, "", ""])
        writer.writerow(["KS", len(values), d, p_ks, ALPHA, decision(p_ks), "", d_plus, d_minus])
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(10)
    ax.bar(x, observed, label="Observada", color="steelblue")
    ax.plot(x, [expected] * 10, color="darkorange", marker="o", label="Esperada")
    ax.set(xticks=x, xticklabels=[f"{i/10:.1f}–{(i+1)/10:.1f}" for i in x],
           xlabel="Intervalo", ylabel="Frecuencia", title="Frecuencias observadas y esperadas")
    ax.legend(); fig.tight_layout(); fig.savefig(figures / "chi_cuadrado.png", dpi=150); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.step(np.r_[0, ordered, 1], np.r_[0, np.arange(1, len(ordered)+1)/len(ordered), 1],
            where="post", label="CDF empírica")
    ax.plot([0, 1], [0, 1], "--", label="CDF uniforme teórica")
    ax.set(xlabel="x", ylabel="F(x)", title="Distribución acumulada empírica y teórica", xlim=(0, 1), ylim=(0, 1))
    ax.legend(); fig.tight_layout(); fig.savefig(figures / "ks_cdf.png", dpi=150); plt.close(fig)
    print(f"Muestra: {len(values)}; alfa={ALPHA}")
    print("Intervalo        Observada  Esperada")
    for i, count in enumerate(observed):
        print(f"[{i/10:.1f},{(i+1)/10:.1f}{']' if i == 9 else ')'}       {count:>6}  {expected:>8.2f}")
    print(f"Chi-cuadrado: X2={chi:.12g}, gl=9, p={p_chi:.12g}; {decision(p_chi)}")
    print(f"KS: D+={d_plus:.12g}, D-={d_minus:.12g}, D={d:.12g}, p={p_ks:.12g}; {decision(p_ks)}")
    if expected < 5:
        print("Advertencia: frecuencia esperada menor que 5; la aproximación Chi-cuadrado puede ser inadecuada.")
    print("No rechazar H0 no demuestra aleatoriedad ni independencia; los valores p suponen observaciones independientes.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="data/lcg_python.csv")
    parser.add_argument("--results", default="results")
    args = parser.parse_args()
    try:
        ejecutar(args.input, args.results)
    except (ValueError, OSError, csv.Error) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
