"""Pruebas reproducibles del oráculo y de la equivalencia Python/Java."""

import importlib.util
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PYTHON_SOURCE = ROOT / "python" / "monte_carlo_pi.py"
PYTHON_CORE = ROOT / "python" / "monte_carlo_core.py"
JAVA_SOURCE = ROOT / "java" / "MonteCarloPi.java"
JAVA_CORE = ROOT / "java" / "MonteCarloCore.java"

spec = importlib.util.spec_from_file_location("monte_carlo_core", PYTHON_CORE)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


def parse_output(text: str) -> dict[str, str]:
    return dict(line.split("=", 1) for line in text.splitlines())


class MonteCarloTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        javac = shutil.which("javac")
        if javac is None:
            raise RuntimeError("Se necesita JDK: javac no está disponible")
        java_name = "java.exe" if sys.platform == "win32" else "java"
        cls.java = str(Path(javac).resolve().with_name(java_name))
        if not Path(cls.java).is_file():
            raise RuntimeError("No se encontró java en el mismo JDK que javac")
        cls.build_dir = tempfile.TemporaryDirectory(prefix="ape7_java_", dir=ROOT / "tests")
        compiled = subprocess.run(
            [javac, "-d", cls.build_dir.name, str(JAVA_CORE), str(JAVA_SOURCE)],
            text=True, capture_output=True, encoding="utf-8", timeout=30,
        )
        if compiled.returncode != 0:
            cls.build_dir.cleanup()
            raise RuntimeError(f"Falló javac: {compiled.stderr}")

    @classmethod
    def tearDownClass(cls):
        cls.build_dir.cleanup()

    def run_case(self, language: str, n: str, seed: str = "42"):
        if language == "python":
            command = [sys.executable, str(PYTHON_SOURCE), n, seed]
        else:
            command = [self.java, "-cp", self.build_dir.name, "MonteCarloPi", n, seed]
        return subprocess.run(
            command, text=True, capture_output=True, encoding="utf-8", timeout=60,
        )

    def test_oracle_both_languages(self):
        for language in ("python", "java"):
            with self.subTest(language=language):
                result = self.run_case(language, "1000")
                self.assertEqual(result.returncode, 0, result.stderr)
                data = parse_output(result.stdout)
                self.assertEqual([int(data[f"estado_{i}"]) for i in (1, 2, 3)],
                                 [1083814273, 378494188, 2479403867])
                self.assertEqual(int(data["nc"]), 773)
                self.assertEqual(float(data["pi_estimado"]), 3.092)

    def test_cross_language_four_sizes(self):
        expected = {1000: (773, 3.092), 10000: (7798, 3.1192),
                    100000: (78749, 3.14996), 1000000: (785678, 3.142712)}
        for n, (expected_nc, expected_pi) in expected.items():
            with self.subTest(n=n):
                python_result = self.run_case("python", str(n))
                java_result = self.run_case("java", str(n))
                self.assertEqual(python_result.returncode, 0, python_result.stderr)
                self.assertEqual(java_result.returncode, 0, java_result.stderr)
                py = parse_output(python_result.stdout)
                ja = parse_output(java_result.stdout)
                self.assertEqual(py["nc"], ja["nc"])
                self.assertEqual(float(py["pi_estimado"]), float(ja["pi_estimado"]))
                nc = int(py["nc"])
                estimate = float(py["pi_estimado"])
                self.assertEqual(nc, expected_nc)
                self.assertEqual(estimate, expected_pi)
                self.assertTrue(0 <= nc <= n)
                self.assertTrue(0 <= estimate <= 4)
                self.assertAlmostEqual(estimate, 4.0 * nc / n, places=15)
                for data in (py, ja):
                    self.assertAlmostEqual(float(data["error_absoluto"]),
                                           abs(estimate - math.pi), places=15)
                    self.assertGreaterEqual(float(data["tiempo_ms"]), 0)

    def test_seed_and_determinism(self):
        for seed in ("-1", "4294967297"):
            with self.subTest(seed=seed):
                py_first = parse_output(self.run_case("python", "257", seed).stdout)
                py_again = parse_output(self.run_case("python", "257", seed).stdout)
                java = parse_output(self.run_case("java", "257", seed).stdout)
                for key in ("estado_1", "estado_2", "estado_3", "nc", "pi_estimado"):
                    self.assertEqual(py_first[key], py_again[key])
                    self.assertEqual(float(py_first[key]), float(java[key]))
        generator = core.LCG(42)
        self.assertTrue(all(0.0 <= generator.next_uniform() < 1.0 for _ in range(10000)))

    def test_invalid_inputs(self):
        for language in ("python", "java"):
            for n in ("0", "-1", "abc", "9223372036854775808"):
                with self.subTest(language=language, n=n):
                    result = self.run_case(language, n)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Error:", result.stderr)
                    self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
