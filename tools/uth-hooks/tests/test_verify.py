from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT


def load_verify():
    script = REPO_ROOT / "scripts" / "verify.py"
    spec = importlib.util.spec_from_file_location("verify", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestVerifyScript(unittest.TestCase):
    def test_no_bom_scan_reports_utf8_bom_file(self):
        module = load_verify()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            docs = root / "docs"
            docs.mkdir()
            bom_file = docs / "current-state.md"
            bom_file.write_bytes(b"\xef\xbb\xbf# current state\n")

            failures = module.find_bom_files(root)

        self.assertEqual([path.name for path in failures], ["current-state.md"])

    def test_no_bom_scan_ignores_cache_directories(self):
        module = load_verify()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            cached = root / "tools" / "__pycache__"
            cached.mkdir(parents=True)
            (cached / "cached.py").write_bytes(b"\xef\xbb\xbfprint('cached')\n")

            failures = module.find_bom_files(root)

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
