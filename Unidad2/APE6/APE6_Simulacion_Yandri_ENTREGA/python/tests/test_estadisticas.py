import csv
from decimal import Decimal
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python/src"))
from estadisticas import chi_cuadrado, decision, kolmogorov_smirnov, leer_csv, ejecutar


class EstadisticasTest(unittest.TestCase):
    def test_fronteras_chi_y_scipy(self):
        values = [Decimal(i) / 10 for i in range(11)]
        obs, expected, statistic, p = chi_cuadrado(values)
        self.assertEqual(obs, [1] * 9 + [2])
        self.assertAlmostEqual(expected, 1.1)
        self.assertAlmostEqual(statistic, 9 / 11)
        reference = stats.chisquare(obs)
        self.assertAlmostEqual(statistic, reference.statistic)
        self.assertAlmostEqual(p, reference.pvalue)
        self.assertTrue(0 <= p <= 1)

    def test_ks_manual_y_scipy(self):
        values = [Decimal("0.1"), Decimal("0.4"), Decimal("0.8")]
        ordered, plus, minus, d, p = kolmogorov_smirnov(values)
        self.assertAlmostEqual(plus, 4 / 15)
        self.assertAlmostEqual(minus, 2 / 15)
        self.assertAlmostEqual(d, 4 / 15)
        ref = stats.kstest(ordered, "uniform", method="exact")
        self.assertAlmostEqual(d, ref.statistic)
        self.assertAlmostEqual(p, ref.pvalue)
        self.assertTrue(0 <= p <= 1)

    def test_muestra_principal(self):
        values = leer_csv(ROOT / "data/lcg_python.csv")
        obs, expected, statistic, p = chi_cuadrado(values)
        self.assertEqual(len(values), 10000)
        self.assertEqual(sum(obs), 10000)
        self.assertEqual(expected, 1000)
        self.assertAlmostEqual(statistic, stats.chisquare(obs).statistic)
        self.assertAlmostEqual(p, stats.chisquare(obs).pvalue)
        ordered, _, _, d, pks = kolmogorov_smirnov(values)
        ref = stats.kstest(ordered, "uniform", method="exact")
        self.assertAlmostEqual(d, ref.statistic)
        self.assertAlmostEqual(pks, ref.pvalue)
        self.assertTrue(0 <= p <= 1 and 0 <= pks <= 1)

    def test_invalidos_y_decision(self):
        self.assertEqual(decision(0.05), "No se rechaza H0")
        self.assertEqual(decision(0.049), "Se rechaza H0")
        for values in ([], [Decimal("NaN")], [Decimal("-0.1")], [Decimal("1.1")]):
            with self.subTest(values=values):
                with self.assertRaises(ValueError): chi_cuadrado(values)
                with self.assertRaises(ValueError): kolmogorov_smirnov(values)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.csv"
            for content in ("otra\n0.2\n", "uniforme\n", "uniforme\nabc\n", "uniforme\nInfinity\n"):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError): leer_csv(path)

    def test_exportacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            ejecutar(ROOT / "data/lcg_python.csv", tmp)
            base = Path(tmp)
            with (base / "tables/chi_cuadrado.csv").open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 10)
            self.assertEqual(sum(int(row["observada"]) for row in rows), 10000)
            for name in ("figures/chi_cuadrado.png", "figures/ks_cdf.png", "tables/estadisticos.csv"):
                self.assertGreater((base / name).stat().st_size, 0)


if __name__ == "__main__": unittest.main()
