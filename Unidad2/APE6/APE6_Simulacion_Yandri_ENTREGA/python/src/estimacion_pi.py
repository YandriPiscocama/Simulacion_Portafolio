"""Estimación de pi por Monte Carlo usando la configuración A del LCG.

La estimación de pi es una ampliación propuesta para completar la tabla de la
sección 6; la guía no define este algoritmo.
"""
import argparse
import csv
import math
import statistics
import time
from pathlib import Path

SEED = 42
A = 1664525
C = 1013904223
M = 2**32
SIZES = (1_000, 10_000, 100_000, 1_000_000)


def estimate_pi(n, seed=SEED, a=A, c=C, m=M):
    """Return (points_inside, pi_estimate) for exactly n points."""
    if type(n) is not int or n < 1:
        raise ValueError("n debe ser un entero positivo")
    if not all(type(v) is int for v in (seed, a, c, m)):
        raise ValueError("Los parámetros LCG deben ser enteros")
    if m <= 1 or not (0 <= seed < m and 0 <= a < m and 0 <= c < m):
        raise ValueError("Parámetros LCG fuera de dominio")
    x = seed
    inside = 0
    for _ in range(n):
        x = (a * x + c) % m
        px = x / m
        x = (a * x + c) % m
        py = x / m
        if px * px + py * py <= 1.0:
            inside += 1
    return inside, 4.0 * inside / n


def measured_time(n, repetitions=5):
    if repetitions < 1:
        raise ValueError("repetitions debe ser positivo")
    estimate_pi(min(n, 1_000))  # calentamiento fuera de las mediciones
    samples = []
    result = None
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        result = estimate_pi(n)
        samples.append((time.perf_counter_ns() - start) / 1_000_000_000)
    return result[0], result[1], statistics.median(samples)


def run(sizes=SIZES, repetitions=5, output="results/tables/comparacion_pi.csv", counts_output=None,
        java_results=None):
    rows = []
    count_rows = []
    for n in sizes:
        inside, estimate, elapsed = measured_time(n, repetitions)
        rows.append((n, estimate, abs(estimate - math.pi), elapsed))
        count_rows.append((n, inside))
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    java_times = {}
    if java_results:
        with Path(java_results).open(encoding="utf-8", newline="") as f:
            java_times = {int(row["N"]): row["tiempo_java_s"] for row in csv.DictReader(f)}
        if set(java_times) != {row[0] for row in rows}:
            raise ValueError("Los resultados Java no contienen exactamente los cuatro tamaños")
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(("N", "pi_estimado", "error_absoluto", "tiempo_python_s", "tiempo_java_s"))
        for n, estimate, error, elapsed in rows:
            writer.writerow((n, f"{estimate:.17g}", f"{error:.17g}", f"{elapsed:.9f}", java_times.get(n, "")))
    if counts_output:
        path = Path(counts_output)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(("N", "puntos_dentro"))
            writer.writerows(count_rows)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="results/tables/comparacion_pi.csv")
    parser.add_argument("--counts-output")
    parser.add_argument("--java-results", help="CSV Java generado previamente; completa tiempo_java_s")
    parser.add_argument("--repetitions", type=int, default=5)
    args = parser.parse_args()
    rows = run(repetitions=args.repetitions, output=args.output, counts_output=args.counts_output,
               java_results=args.java_results)
    print("N,pi_estimado,error_absoluto,tiempo_python_s")
    for n, estimate, error, elapsed in rows:
        print(f"{n},{estimate:.17g},{error:.17g},{elapsed:.9f}")


if __name__ == "__main__":
    main()
