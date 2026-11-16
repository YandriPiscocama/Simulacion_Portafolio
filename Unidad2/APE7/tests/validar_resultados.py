"""Auditoría independiente de CSV y tabla; no vuelve a simular puntos."""

import csv
import math
from pathlib import Path
import statistics


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "resultados"
SIZES = (1000, 10000, 100000, 1000000)
RUN_FIELDS = ["lenguaje", "n", "repeticion", "semilla", "nc", "pi_estimado", "error_absoluto", "tiempo_ms"]
TABLE_FIELDS = ["N", "π estimado", "Error", "Tiempo Python", "Tiempo Java"]


def read(name, fields):
    with (RESULTS / name).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == fields, (name, reader.fieldnames)
        rows = list(reader)
    assert all(None not in row for row in rows)
    return rows


runs = read("corridas.csv", RUN_FIELDS)
repetitions = max(int(row["repeticion"]) for row in runs)
assert repetitions in (1, 20)
assert len(runs) == 8 * repetitions
index = {}
for row in runs:
    language = row["lenguaje"]
    n = int(row["n"])
    repetition = int(row["repeticion"])
    seed = int(row["semilla"])
    nc = int(row["nc"])
    pi_est = float(row["pi_estimado"])
    error = float(row["error_absoluto"])
    time_ms = float(row["tiempo_ms"])
    assert language in ("Python", "Java") and n in SIZES
    assert 1 <= repetition <= repetitions and seed == 41 + repetition
    assert 0 <= nc <= n and 0 <= pi_est <= 4 and math.isfinite(time_ms) and time_ms >= 0
    assert math.isclose(pi_est, 4.0 * nc / n, rel_tol=0, abs_tol=1e-15)
    assert math.isclose(error, abs(pi_est - math.pi), rel_tol=0, abs_tol=1e-15)
    key = (language, n, repetition)
    assert key not in index
    index[key] = row

for repetition in range(1, repetitions + 1):
    for n in SIZES:
        py = index[("Python", n, repetition)]
        ja = index[("Java", n, repetition)]
        assert py["nc"] == ja["nc"]
        assert float(py["pi_estimado"]) == float(ja["pi_estimado"])
        assert float(py["error_absoluto"]) == float(ja["error_absoluto"])

assert index[("Python", 1000, 1)]["nc"] == "773"
assert float(index[("Python", 1000, 1)]["pi_estimado"]) == 3.092

table = read("tabla_docente.csv", TABLE_FIELDS)
assert len(table) == 4
for row, n in zip(table, SIZES):
    py = index[("Python", n, 1)]
    ja = index[("Java", n, 1)]
    assert row == {"N": str(n), "π estimado": py["pi_estimado"],
                   "Error": py["error_absoluto"], "Tiempo Python": py["tiempo_ms"],
                   "Tiempo Java": ja["tiempo_ms"]}

summary_path = RESULTS / "resumen_estadistico.csv"
if repetitions == 20:
    assert summary_path.is_file()
    with summary_path.open(newline="", encoding="utf-8") as stream:
        summary = list(csv.DictReader(stream))
    assert len(summary) == 8
    for row in summary:
        language, n = row["lenguaje"], int(row["n"])
        values = [index[(language, n, rep)] for rep in range(1, 21)]
        estimates = [float(value["pi_estimado"]) for value in values]
        errors = [float(value["error_absoluto"]) for value in values]
        times = [float(value["tiempo_ms"]) for value in values]
        expected = {"media_pi": statistics.mean(estimates),
                    "desviacion_estandar_pi": statistics.stdev(estimates),
                    "rmse_pi": math.sqrt(statistics.mean((x - math.pi) ** 2 for x in estimates)),
                    "media_error_absoluto": statistics.mean(errors),
                    "mediana_tiempo_ms": statistics.median(times)}
        assert int(row["repeticiones"]) == 20
        for field, actual in expected.items():
            assert math.isclose(float(row[field]), actual, rel_tol=1e-12, abs_tol=1e-15)

print(f"VALIDADO: {len(runs)} corridas, {repetitions} repetición(es) por N y lenguaje; "
      "equivalencia, fórmulas y tabla docente coherentes.")
