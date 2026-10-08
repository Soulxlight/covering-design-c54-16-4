"""Small adversarial checks for the exact certificate replay."""

import copy
import json
import sys
import unittest
from itertools import combinations
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify  # noqa: E402


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = json.loads((ROOT / "data" / "model.json").read_text(encoding="utf-8"))
        cls.certificate = json.loads((ROOT / "data" / "certificate.json").read_text(encoding="utf-8"))

    def test_exact_certificate_and_diagnostic(self):
        result = verify.verify_files(ROOT / "data")
        self.assertEqual(result["status"], "PASS_EXACT_CERTIFICATE")
        self.assertEqual(result["exact_F_upper"], "-1330103235427/500000000")

    def test_changed_model_row_is_rejected(self):
        changed = copy.deepcopy(self.model)
        changed["rows"][9]["coefficients"]["n3"] += 1
        variables, rows = verify.matrix()
        with self.assertRaisesRegex(ValueError, "matrix mismatch"):
            verify.validate_model(changed, variables, rows)

    def test_changed_certificate_weight_is_rejected(self):
        changed = copy.deepcopy(self.certificate)
        changed["row_numerators"][0] = str(int(changed["row_numerators"][0]) + 1)
        with self.assertRaises(ValueError):
            verify.replay_certificate(self.model, changed)

    def test_all_zero_certificate_is_rejected(self):
        changed = copy.deepcopy(self.certificate)
        changed["row_numerators"] = ["0"] * len(changed["row_numerators"])
        with self.assertRaises(ValueError):
            verify.replay_certificate(self.model, changed)

    def test_221_scalar_bound(self):
        # Independent evaluation of the quadratic upper expression in the
        # companion proof for b=216,...,220.
        values = [-95526 + 20763 * j + 21 * j * j for j in range(5)]
        self.assertEqual(values, [-95526, -74742, -53916, -33048, -12138])
        self.assertTrue(all(value < 0 for value in values))

    def test_standard_third_moment_identity(self):
        # Double count triple/unordered-block-pair incidences on small raw
        # families, including a repeated block occurrence.
        blocks = [set(c) for c in combinations(range(6), 4)]
        triples = [set(c) for c in combinations(range(6), 3)]
        families = [[], blocks[:1], blocks[:7], blocks, blocks + [blocks[0]]]
        for family in families:
            by_pairs = sum(comb(len(a & b), 3)
                           for i, a in enumerate(family) for b in family[i + 1:])
            by_triples = sum(comb(sum(triple <= block for block in family), 2)
                             for triple in triples)
            self.assertEqual(by_pairs, by_triples)

    def test_truncated_moment_is_not_an_all_family_identity(self):
        # Two incomplete legal (54,16) blocks intersect in three points.
        # Their full degree histogram has exactly one degree-two triple.
        first = set(range(16))
        second = {0, 1, 2} | set(range(16, 29))
        self.assertEqual((len(first), len(second), len(first & second)), (16, 16, 3))
        full_triple_sum = sum(comb(int(triple <= first) + int(triple <= second), 2)
                              for triple in map(set, combinations(range(54), 3)))
        block_pair_sum = comb(len(first & second), 3)
        self.assertEqual(full_triple_sum - block_pair_sum, 0)
        self.assertEqual(0 - block_pair_sum, -1)  # degrees 4..104 only


if __name__ == "__main__":
    unittest.main()
