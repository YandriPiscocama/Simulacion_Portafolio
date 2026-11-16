"""Comprueba las figuras en una copia temporal, sin tocar las originales."""

from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FigureRegressionTests(unittest.TestCase):
    def test_all_figures_from_historical_csv(self):
        with tempfile.TemporaryDirectory(prefix="ape7_figuras_", dir=ROOT / "tests") as temporary:
            copy_root = Path(temporary)
            (copy_root / "tests").mkdir()
            (copy_root / "resultados").mkdir()
            shutil.copy2(ROOT / "tests" / "graficar_resultados.py", copy_root / "tests")
            for csv_path in (ROOT / "resultados").glob("*.csv"):
                shutil.copy2(csv_path, copy_root / "resultados")

            result = subprocess.run(
                [sys.executable, str(copy_root / "tests" / "graficar_resultados.py")],
                text=True, capture_output=True, encoding="utf-8", errors="replace", timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ("convergencia.png", "error.png", "tiempos.png", "distribucion.png"):
                with self.subTest(name=name):
                    path = copy_root / "graficas" / name
                    with path.open("rb") as stream:
                        header = stream.read(24)
                    self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
                    width, height = struct.unpack(">II", header[16:24])
                    self.assertGreaterEqual(width, 1000)
                    self.assertGreaterEqual(height, 600)


if __name__ == "__main__":
    unittest.main(verbosity=2)
