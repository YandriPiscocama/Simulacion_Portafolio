import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python" / "src"))
from lcg import generate, normalized


class LCGTests(unittest.TestCase):
    def test_known_sequence(self):
        self.assertEqual(list(generate(1, 5, 3, 16, 5)), [8, 11, 10, 5, 12])
        self.assertEqual(normalized(8, 16), "0.50000000000000000")

    def test_count_range_and_reproducibility(self):
        args = (42, 1664525, 1013904223, 2**32, 10000)
        values = list(generate(*args))
        self.assertEqual(len(values), 10000)
        self.assertTrue(all(0 <= x < args[3] for x in values))
        self.assertTrue(all(0 <= x / args[3] < 1 for x in values))
        self.assertEqual(values, list(generate(*args)))

    def test_invalid_parameters(self):
        for args in [(0, 1, 0, 1, 1), (-1, 1, 0, 16, 1), (16, 1, 0, 16, 1),
                     (0, -1, 0, 16, 1), (0, 16, 0, 16, 1), (0, 1, -1, 16, 1),
                     (0, 1, 16, 16, 1), (0, 1, 0, 16, 0), (0.5, 1, 0, 16, 1)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                list(generate(*args))

    def test_java_and_python_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            subprocess.run(["javac", "-source", "8", "-target", "8", "-d", str(tmp),
                            str(ROOT / "java/src/LCG.java"), str(ROOT / "java/tests/LCGTest.java")], check=True)
            subprocess.run(["java", "-cp", str(tmp), "LCGTest"], check=True)
            py, java = tmp / "python.csv", tmp / "java.csv"
            subprocess.run([sys.executable, str(ROOT / "python/src/lcg.py"), "--output", str(py)],
                           check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["java", "-cp", str(tmp), "LCG", "--output", str(java)],
                           check=True, stdout=subprocess.DEVNULL)
            with py.open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 10000)
            self.assertEqual(py.read_bytes(), java.read_bytes())
            for flag, value in [("--seed", "-1"), ("--a", "-1"), ("--c", "-1"),
                                ("--m", "1"), ("--n", "0")]:
                result = subprocess.run(["java", "-cp", str(tmp), "LCG", flag, value,
                                         "--output", str(java)], capture_output=True)
                self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
