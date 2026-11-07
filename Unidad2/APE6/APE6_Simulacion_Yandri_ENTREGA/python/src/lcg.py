"""Generador congruencial lineal y exportación CSV reproducible."""
import argparse
import csv
from decimal import Decimal, ROUND_HALF_EVEN, localcontext

DEFAULTS = (42, 1664525, 1013904223, 2**32, 10000)


def generate(seed, a, c, m, n):
    if any(type(v) is not int for v in (seed, a, c, m, n)):
        raise ValueError("Los parámetros deben ser enteros")
    if m <= 1 or not (0 <= seed < m and 0 <= a < m and 0 <= c < m) or n < 1:
        raise ValueError("Se requiere m > 1, 0 <= semilla,a,c < m y n >= 1")
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        yield x


def normalized(x, m):
    # Precisión suficiente incluso para parámetros enteros grandes.
    with localcontext() as ctx:
        ctx.prec = max(len(str(m)), len(str(x))) + 25
        scale = max(17, len(str(m)) + 1)
        ctx.prec = len(str(m)) + scale + 5
        return format((Decimal(x) / Decimal(m)).quantize(Decimal(1).scaleb(-scale), rounding=ROUND_HALF_EVEN), "f")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag, default in zip(("seed", "a", "c", "m", "n"), DEFAULTS):
        parser.add_argument("--" + flag, type=int, default=default)
    parser.add_argument("--output", default="data/lcg_python.csv")
    args = parser.parse_args()
    try:
        # Validar antes de crear el archivo.
        values = list(generate(args.seed, args.a, args.c, args.m, args.n))
    except ValueError as exc:
        parser.error(str(exc))
    with open(args.output, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(("indice", "estado", "uniforme"))
        print("indice,estado,uniforme")
        for i, x in enumerate(values, 1):
            row = (i, x, normalized(x, args.m))
            writer.writerow(row)
            print(",".join(map(str, row)))


if __name__ == "__main__":
    main()
