import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from detectors import detect_exploit_families, macro_classes_for


class DetectorTests(unittest.TestCase):
    def test_benign_code_is_unflagged(self):
        self.assertEqual(detect_exploit_families("def add(a, b):\n    return a + b"), [])

    def test_weak_check_is_flagged(self):
        submitted = "def check(x):\n    return True"
        reference = "def check(x):\n    assert x == 3\n    assert x > 0"
        self.assertIn("redefine_check", detect_exploit_families(submitted, reference))

    def test_macro_mapping(self):
        self.assertEqual(macro_classes_for(["process_exit", "redefine_check"]), ["ET", "TM"])


if __name__ == "__main__":
    unittest.main()
