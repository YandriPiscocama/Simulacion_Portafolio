import csv
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python/src"))
from estimacion_pi import estimate_pi, run


class EstimacionPiTest(unittest.TestCase):
    def test_casos_reproducibles_y_formula(self):
        first = estimate_pi(1000)
        self.assertEqual(first, estimate_pi(1000))
        inside, estimate = first
        self.assertEqual(inside, 773)
        self.assertEqual(estimate, 4 * inside / 1000)
        self.assertEqual(abs(estimate - math.pi), abs(4 * inside / 1000 - math.pi))

    def test_cuatro_tamanos(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pi.csv"
            rows = run(repetitions=1, output=output)
            self.assertEqual([row[0] for row in rows], [1000, 10000, 100000, 1000000])
            with output.open(encoding="utf-8", newline="") as f:
                saved = list(csv.DictReader(f))
            self.assertEqual(len(saved), 4)
            self.assertEqual(saved[0].keys(), {"N", "pi_estimado", "error_absoluto", "tiempo_python_s", "tiempo_java_s"})
            for row in saved:
                self.assertGreater(float(row["pi_estimado"]), 0)
                self.assertGreaterEqual(float(row["error_absoluto"]), 0)
                self.assertGreater(float(row["tiempo_python_s"]), 0)

    def test_java_coincide_en_conteos_y_estimacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            subprocess.run(["javac", "-source", "8", "-target", "8", "-d", str(tmp),
                            str(ROOT / "java/src/LCG.java"), str(ROOT / "java/src/EstimacionPi.java")], check=True)
            py_counts = tmp / "py_counts.csv"
            java_counts = tmp / "java_counts.csv"
            run(repetitions=1, output=tmp / "py.csv", counts_output=py_counts)
            subprocess.run(["java", "-cp", str(tmp), "EstimacionPi", "--repetitions", "1",
                            "--output", str(tmp / "java.csv"), "--counts-output", str(java_counts)], check=True,
                           stdout=subprocess.DEVNULL)
            self.assertEqual(py_counts.read_bytes(), java_counts.read_bytes())
            with (tmp / "py.csv").open(encoding="utf-8", newline="") as f: py = list(csv.DictReader(f))
            with (tmp / "java.csv").open(encoding="utf-8", newline="") as f: java = list(csv.DictReader(f))
            for p, j in zip(py, java):
                self.assertEqual(p["N"], j["N"])
                self.assertAlmostEqual(float(p["pi_estimado"]), float(j["pi_estimado"]), places=15)

    def test_resultados_estadisticos_sin_cambios(self):
        expected = {
            ROOT / "results/tables/chi_cuadrado.csv": "7EB685B06BA81DB121B309DB26651D1898B2FDFB30F67365302043EA1310637F",
            ROOT / "results/tables/estadisticos.csv": "B9CE64919B4B447F71018907FB44469E2479D7B80F1109CA38FA515EC3A73E8C",
            ROOT / "results/tables/comparacion_a_b.csv": "3995F35E87451FD4E619B5583DC03C6146958F043099598EE5066591B62F1C63",
        }
        for path, digest in expected.items():
            import hashlib
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest().upper(), digest)


if __name__ == "__main__":
    unittest.main()
