import argparse
import csv
from decimal import Decimal, localcontext
from pathlib import Path

A, C, M, N = 1664525, 1013904223, 2**32, 10_000


def generate(seed=12345):
    if not 0 <= seed < M:
        raise ValueError("La semilla debe pertenecer a [0, m)")
    state = seed
    for _ in range(N):
        state = (A * state + C) % M
        yield state


def export(seed, path):
    states = generate(seed)
    first = next(states)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream, localcontext() as ctx:
        ctx.prec = 40
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("indice", "estado", "uniforme"))
        writer.writerow((1, first, f"{Decimal(first) / M:.32f}"))
        for index, state in enumerate(states, 2):
            writer.writerow((index, state, f"{Decimal(state) / M:.32f}"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LCG de la APE 5")
    parser.add_argument("seed", type=int)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        export(args.seed, args.output)
    except ValueError as exc:
        parser.error(str(exc))
