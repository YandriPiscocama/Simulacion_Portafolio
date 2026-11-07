import csv
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python/src"))
from lcg import export, generate


class LCGTests(unittest.TestCase):
    def test_known_states_and_seed(self):
        self.assertEqual(list(generate())[:3], [87628868, 71072467, 2332836374])
        self.assertEqual(next(generate(42)), 1083814273)
        with self.assertRaises(ValueError):
            next(generate(-1))

    def test_csv_recurrence_count_range_and_reproducibility(self):
        for seed in (12345, 42):
            with self.subTest(seed=seed), tempfile.TemporaryDirectory() as folder:
                first, second = Path(folder) / "one.csv", Path(folder) / "two.csv"
                export(seed, first)
                export(seed, second)
                self.assertEqual(first.read_bytes(), second.read_bytes())
                with first.open(encoding="utf-8", newline="") as stream:
                    rows = list(csv.DictReader(stream))
                self.assertEqual(len(rows), 10000)
                state = seed
                with localcontext() as ctx:
                    ctx.prec = 40
                    for index, row in enumerate(rows, 1):
                        state = (1664525 * state + 1013904223) % 4294967296
                        self.assertEqual((int(row["indice"]), int(row["estado"])), (index, state))
                        uniform = Decimal(row["uniforme"])
                        self.assertTrue(0 <= uniform < 1)
                        self.assertEqual(uniform * 4294967296, state)

    def test_java_and_python(self):
        java = os.environ.get("APE5_JAVA", "java")
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            subprocess.run(["javac", "-source", "8", "-target", "8", "-d", str(folder),
                            str(ROOT / "java/src/LCG.java"), str(ROOT / "java/tests/LCGTest.java")], check=True)
            subprocess.run([java, "-cp", str(folder), "LCGTest", str(folder / "test.csv")], check=True)
            for seed in (12345, 42):
                py, j = folder / "python.csv", folder / "java.csv"
                export(seed, py)
                subprocess.run([java, "-cp", str(folder), "LCG", str(seed), str(j)], check=True)
                self.assertEqual(py.read_bytes(), j.read_bytes())


if __name__ == "__main__":
    unittest.main()
