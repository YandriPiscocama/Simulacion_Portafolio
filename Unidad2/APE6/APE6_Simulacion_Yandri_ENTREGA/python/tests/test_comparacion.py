import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python/src"))
from estadisticas import leer_csv, chi_cuadrado, kolmogorov_smirnov


class ComparacionTest(unittest.TestCase):
    def test_b_coincidencia_repeticion_y_periodo(self):
        original = ROOT / "data/lcg_b_python.csv"
        self.assertEqual(original.read_bytes(), (ROOT / "data/lcg_b_java.csv").read_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "b.csv"
            subprocess.run([sys.executable, str(ROOT / "python/src/lcg.py"), "--seed", "42", "--a", "1", "--c", "1", "--m", "256", "--n", "10000", "--output", str(output)], check=True, stdout=subprocess.DEVNULL)
            self.assertEqual(original.read_bytes(), output.read_bytes())
        with original.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        states = [int(r["estado"]) for r in rows]
        self.assertEqual(len(states), 10000)
        self.assertEqual(len(set(states[:256])), 256)
        self.assertEqual(states[:-256], states[256:])
        self.assertTrue(all(states[i] == (states[i-1] + 1) % 256 for i in range(1, len(states))))

    def test_comparacion_coincide_con_muestras_y_tablas(self):
        with (ROOT / "results/tables/comparacion_a_b.csv").open(encoding="utf-8", newline="") as f:
            comparison = {row["configuracion"]: row for row in csv.DictReader(f)}
        for name, path in [("A", "data/lcg_python.csv"), ("B", "data/lcg_b_python.csv")]:
            values = leer_csv(ROOT / path)
            obs, expected, chi, p = chi_cuadrado(values)
            _, _, _, d, pks = kolmogorov_smirnov(values)
            row = comparison[name]
            self.assertEqual(len(values), 10000)
            self.assertEqual(sum(obs), 10000)
            self.assertEqual(expected, 1000)
            for value, col in [(chi, "chi2"), (p, "p_chi2"), (d, "D"), (pks, "p_ks")]:
                self.assertAlmostEqual(value, float(row[col]))
            self.assertTrue(0 <= p <= 1 and 0 <= pks <= 1)
            self.assertEqual(row["decision_chi2"], "Se rechaza H0" if p < 0.05 else "No se rechaza H0")
            self.assertEqual(row["decision_ks"], "Se rechaza H0" if pks < 0.05 else "No se rechaza H0")


if __name__ == "__main__": unittest.main()
