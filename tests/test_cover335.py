"""Legality, integrity and incidence controls for the published upper witness."""
import hashlib
import itertools
import unittest
from pathlib import Path
from unittest.mock import patch
from upper335.verify_cover import WITNESS, EXPECTED_SHA256, parse_blocks, build_columns, covered, verify


class Cover335Tests(unittest.TestCase):
    def setUp(self):
        self.raw = WITNESS.read_bytes()

    def changed_first_row(self, transform):
        lines = self.raw.decode('ascii').splitlines()
        cells = lines[0].split(); transform(cells)
        lines[0] = ' '.join(cells) + ' '
        return ('\n'.join(lines) + '\n').encode('ascii')

    def test_exact_witness_and_full_coverage(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), EXPECTED_SHA256)
        result = verify()
        self.assertEqual((result['distinct_blocks'],result['quadruples_checked'],result['uncovered']),
                         (335,316251,0))
        self.assertFalse(result['optimality_claimed'])

    def test_repeated_point_rejected(self):
        with self.assertRaises(ValueError):
            parse_blocks(self.changed_first_row(lambda cells: cells.__setitem__(1,cells[0])))

    def test_out_of_range_point_rejected(self):
        with self.assertRaises(ValueError):
            parse_blocks(self.changed_first_row(lambda cells: cells.__setitem__(0,'55')))

    def test_zero_point_rejected(self):
        with self.assertRaises(ValueError):
            parse_blocks(self.changed_first_row(lambda cells: cells.__setitem__(0,'00')))

    def test_wrong_block_size_rejected(self):
        with self.assertRaises(ValueError):
            parse_blocks(self.changed_first_row(lambda cells: cells.pop()))

    def test_repeated_whole_block_rejected(self):
        lines=self.raw.decode('ascii').splitlines();lines[-1]=lines[0]
        with self.assertRaises(ValueError):
            parse_blocks(('\n'.join(lines)+'\n').encode('ascii'))

    def test_missing_block_rejected(self):
        with self.assertRaises(ValueError):
            parse_blocks(b'\n'.join(self.raw.splitlines()[:-1])+b'\n')

    def test_changed_newlines_rejected_by_byte_pin(self):
        with patch.object(Path,'read_bytes',return_value=self.raw.replace(b'\n',b'\r\n')):
            with self.assertRaises(ValueError):
                verify(WITNESS)

    def test_uncovered_and_shared_owner_controls(self):
        rows=((1,2,3,4),(1,2,3,4),(4,5,6,7))
        columns=build_columns(rows,8)
        found={q for q in itertools.combinations(range(1,9),4) if covered(columns,q)}
        self.assertEqual(found,{(1,2,3,4),(4,5,6,7)})
        self.assertEqual((columns[1]&columns[2]&columns[3]&columns[4]).bit_count(),2)
        self.assertFalse(covered(columns,(1,2,3,8)))


if __name__=='__main__':
    unittest.main()
