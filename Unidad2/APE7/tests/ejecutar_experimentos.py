"""Ejecuta los programas validados; no implementa otra simulación."""

import argparse
import csv
import math
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SIZES = (1000, 10000, 100000, 1000000)
FIELDS = ("lenguaje", "n", "repeticion", "semilla", "nc", "pi_estimado", "error_absoluto", "tiempo_ms")
TABLE_FIELDS = ("N", "π estimado", "Error", "Tiempo Python", "Tiempo Java")
SUMMARY_FIELDS = ("lenguaje", "n", "repeticiones", "media_pi", "desviacion_estandar_pi",
                  "rmse_pi", "media_error_absoluto", "mediana_tiempo_ms")


def read_output(stdout):
    data = dict(line.split("=", 1) for line in stdout.splitlines())
    required = {"n", "semilla", "estado_1", "estado_2", "estado_3", "nc",
                "pi_estimado", "error_absoluto", "tiempo_ms"}
    if set(data) != required:
        raise ValueError(f"Salida inesperada: {sorted(set(data) ^ required)}")
    return data


def run(command, language, n, seed, repetition):
    completed = subprocess.run(command, text=True, capture_output=True,
                               encoding="utf-8", timeout=120)
    if completed.returncode != 0:
        raise RuntimeError(f"{language}, N={n}, semilla={seed}: {completed.stderr}")
    data = read_output(completed.stdout)
    if int(data["n"]) != n or int(data["semilla"]) != seed:
        raise ValueError("N o semilla no coinciden con la invocación")
    if seed == 42 and tuple(int(data[f"estado_{i}"]) for i in (1, 2, 3)) != (
            1083814273, 378494188, 2479403867):
        raise ValueError("Falló el oráculo de estados del LCG")
    nc = int(data["nc"])
    estimate = float(data["pi_estimado"])
    error = float(data["error_absoluto"])
    elapsed = float(data["tiempo_ms"])
    if not (0 <= nc <= n and 0 <= estimate <= 4 and elapsed >= 0):
        raise ValueError("Rango inválido de resultado")
    if not math.isclose(estimate, 4.0 * nc / n, rel_tol=0, abs_tol=1e-15):
        raise ValueError("π estimado incoherente con Nc")
    if not math.isclose(error, abs(estimate - math.pi), rel_tol=0, abs_tol=1e-15):
        raise ValueError("Error absoluto incoherente")
    if seed == 42 and n == 1000 and (nc != 773 or estimate != 3.092):
        raise ValueError("Falló el oráculo N=1000")
    return {"lenguaje": language, "n": str(n), "repeticion": str(repetition),
            "semilla": str(seed), "nc": str(nc), "pi_estimado": data["pi_estimado"],
            "error_absoluto": data["error_absoluto"], "tiempo_ms": data["tiempo_ms"]}


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_primary(path):
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    primary = [row for row in rows if row["repeticion"] == "1" and row["semilla"] == "42"]
    keys = {(row["lenguaje"], int(row["n"])) for row in primary}
    if len(primary) != 8 or keys != {(lang, n) for lang in ("Python", "Java") for n in SIZES}:
        raise ValueError("CSV previo no contiene exactamente las ocho corridas principales")
    return primary


def verify_pair(python_row, java_row):
    for field in ("n", "repeticion", "semilla", "nc"):
        if python_row[field] != java_row[field]:
            raise ValueError(f"Diferencia Python/Java en {field}: {python_row} / {java_row}")
    for field in ("pi_estimado", "error_absoluto"):
        if float(python_row[field]) != float(java_row[field]):
            raise ValueError(f"Diferencia Python/Java en {field}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeticiones", type=int, choices=(1, 20), default=1)
    parser.add_argument("--resultados", type=Path, default=ROOT / "resultados",
                        help="Carpeta de salida; por defecto, los resultados históricos")
    parser.add_argument("--python", default=sys.executable, help="Ejecutable de Python")
    parser.add_argument("--javac", default="javac", help="Compilador Java del JDK")
    parser.add_argument("--java", help="Ejecutable Java; por defecto, junto a javac")
    args = parser.parse_args()
    javac = shutil.which(args.javac)
    if not javac:
        raise RuntimeError(f"javac no disponible: {args.javac}")
    java = args.java or str(Path(javac).resolve().with_name(
        "java.exe" if sys.platform == "win32" else "java"))
    if not Path(java).is_file():
        raise RuntimeError(f"java no está disponible: {java}")

    result_dir = args.resultados.resolve()
    result_path = result_dir / "corridas.csv"
    primary = read_primary(result_path) if args.repeticiones == 20 else []
    all_rows = list(primary)
    with tempfile.TemporaryDirectory(prefix="ape7_java_", dir=ROOT / "tests") as build:
        subprocess.run([javac, "-d", build, str(ROOT / "java" / "MonteCarloCore.java"),
                        str(ROOT / "java" / "MonteCarloPi.java")],
                       check=True, timeout=30)
        for repetition in range(1, args.repeticiones + 1):
            seed = 41 + repetition
            for n in SIZES:
                if repetition == 1 and primary:
                    pair = [next(row for row in primary if row["lenguaje"] == language
                                 and int(row["n"]) == n) for language in ("Python", "Java")]
                else:
                    py_command = [args.python, str(ROOT / "python" / "monte_carlo_pi.py"), str(n), str(seed)]
                    ja_command = [java, "-cp", build, "MonteCarloPi", str(n), str(seed)]
                    pair = [run(py_command, "Python", n, seed, repetition),
                            run(ja_command, "Java", n, seed, repetition)]
                    all_rows.extend(pair)
                verify_pair(*pair)
                print(f"repetición={repetition} N={n} Nc={pair[0]['nc']} "
                      f"Python_ms={pair[0]['tiempo_ms']} Java_ms={pair[1]['tiempo_ms']}", flush=True)

    all_rows.sort(key=lambda row: (int(row["repeticion"]), int(row["n"]), row["lenguaje"]))
    write_csv(result_path, FIELDS, all_rows)
    primary = [row for row in all_rows if row["repeticion"] == "1"]
    table = []
    for n in SIZES:
        py = next(row for row in primary if row["lenguaje"] == "Python" and int(row["n"]) == n)
        ja = next(row for row in primary if row["lenguaje"] == "Java" and int(row["n"]) == n)
        verify_pair(py, ja)
        table.append({"N": str(n), "π estimado": py["pi_estimado"], "Error": py["error_absoluto"],
                      "Tiempo Python": py["tiempo_ms"], "Tiempo Java": ja["tiempo_ms"]})
    write_csv(result_dir / "tabla_docente.csv", TABLE_FIELDS, table)

    if args.repeticiones == 20:
        summary = []
        for language in ("Python", "Java"):
            for n in SIZES:
                rows = [row for row in all_rows if row["lenguaje"] == language and int(row["n"]) == n]
                estimates = [float(row["pi_estimado"]) for row in rows]
                errors = [float(row["error_absoluto"]) for row in rows]
                times = [float(row["tiempo_ms"]) for row in rows]
                summary.append({"lenguaje": language, "n": n, "repeticiones": len(rows),
                                "media_pi": statistics.mean(estimates),
                                "desviacion_estandar_pi": statistics.stdev(estimates),
                                "rmse_pi": math.sqrt(statistics.mean((x - math.pi) ** 2 for x in estimates)),
                                "media_error_absoluto": statistics.mean(errors),
                                "mediana_tiempo_ms": statistics.median(times)})
        write_csv(result_dir / "resumen_estadistico.csv", SUMMARY_FIELDS, summary)
    else:
        (result_dir / "resumen_estadistico.csv").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
