"""Núcleo matemático del experimento Monte Carlo, sin E/S ni cronómetro."""

import math

MASK = 0xFFFFFFFF
MODULUS = 4294967296.0
MULTIPLIER = 1664525
INCREMENT = 1013904223


class LCG:
    def __init__(self, seed: int) -> None:
        self.state = seed & MASK

    def next_state(self) -> int:
        self.state = (MULTIPLIER * self.state + INCREMENT) & MASK
        return self.state

    def next_uniform(self) -> float:
        return self.next_state() / MODULUS


def count_inside(n: int, seed: int) -> int:
    if n <= 0:
        raise ValueError("N debe ser un entero positivo")
    generator = LCG(seed)
    nc = 0
    for _ in range(n):
        x = generator.next_uniform()
        y = generator.next_uniform()
        if x * x + y * y <= 1.0:
            nc += 1
    return nc


def estimate_pi(nc: int, n: int) -> float:
    return 4.0 * nc / n


def absolute_error(pi_estimate: float) -> float:
    return abs(pi_estimate - math.pi)
