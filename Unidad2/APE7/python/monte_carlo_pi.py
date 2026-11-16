"""CLI del experimento: argumentos, tiempo de cálculo y salida estructurada."""

from __future__ import annotations

import sys
import time

from monte_carlo_core import LCG, absolute_error, count_inside, estimate_pi

MAX_SIGNED_LONG = (1 << 63) - 1
MIN_SIGNED_LONG = -(1 << 63)


def parse_args(argv: list[str]) -> tuple[int, int]:
    if len(argv) not in (2, 3):
        raise ValueError("Uso: python monte_carlo_pi.py N [semilla]")
    try:
        n = int(argv[1])
        seed = int(argv[2]) if len(argv) == 3 else 42
    except ValueError as exc:
        raise ValueError("N y semilla deben ser enteros") from exc
    if not 1 <= n <= MAX_SIGNED_LONG:
        raise ValueError("N debe estar entre 1 y 9223372036854775807")
    if not MIN_SIGNED_LONG <= seed <= MAX_SIGNED_LONG:
        raise ValueError("La semilla debe ser un entero con signo de 64 bits")
    return n, seed


def main(argv: list[str]) -> int:
    try:
        n, seed = parse_args(argv)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    probe = LCG(seed)
    first_states = [probe.next_state() for _ in range(3)]

    start_ns = time.perf_counter_ns()
    nc = count_inside(n, seed)
    elapsed_ns = time.perf_counter_ns() - start_ns

    pi_estimate = estimate_pi(nc, n)
    error = absolute_error(pi_estimate)
    print(f"n={n}")
    print(f"semilla={seed}")
    for index, state in enumerate(first_states, start=1):
        print(f"estado_{index}={state}")
    print(f"nc={nc}")
    print(f"pi_estimado={pi_estimate}")
    print(f"error_absoluto={error}")
    print(f"tiempo_ms={elapsed_ns / 1_000_000.0:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
