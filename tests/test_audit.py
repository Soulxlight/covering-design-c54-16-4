"""Meaningful adversarial checks of the public audit's trust boundaries."""
from pathlib import Path
from fractions import Fraction
import copy
import json
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'audit'))
import independent222 as old
import independent223 as new
import verify_audit as audit

class AuditTests(unittest.TestCase):
    def reject_manifest_change(self,mutate):
        with tempfile.TemporaryDirectory(prefix='covering-manifest-test-') as temporary:
            root=Path(temporary)/'packet';root.mkdir()
            (root/'audit').mkdir()
            doc=audit.read(audit.ROOT/'audit/PUBLIC_MANIFEST.json');mutate(doc)
            (root/'audit/PUBLIC_MANIFEST.json').write_text(json.dumps(doc),encoding='utf-8')
            # Synchronized empty checksums must not make an empty manifest valid.
            (root/'SHA256SUMS').write_text('',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'manifest (exact canonical inventory|duplicate names)'):
                audit.verify_manifest(root)

    def test_manifest_empty_inventory_with_empty_checksums_rejected(self):
        self.reject_manifest_change(lambda d:d.update(files=[]))

    def test_manifest_missing_entry_rejected(self):
        self.reject_manifest_change(lambda d:d['files'].pop())

    def test_manifest_unexpected_entry_rejected(self):
        self.reject_manifest_change(lambda d:d['files'].append(dict(path='unexpected.txt',bytes=0,sha256='0'*64)))

    def test_manifest_equal_count_substitution_rejected(self):
        self.reject_manifest_change(lambda d:d['files'][-1].update(path='unexpected.txt'))

    def test_manifest_path_aliases_and_duplicate_rejected(self):
        for alias in ('./verify.py','audit/../verify.py','VERIFY.py','audit\\verify_audit.py'):
            with self.subTest(alias=alias):self.reject_manifest_change(lambda d:d['files'][-1].update(path=alias))
        self.reject_manifest_change(lambda d:d['files'].__setitem__(-1,copy.deepcopy(d['files'][0])))

    def test_rank_floor_covers_empty_case_and_all_matching_types(self):
        self.assertEqual(audit.direct_floor()['matching_isomorphism_types'],729)

    def test_222_full_reconstruction_and_certificate(self):
        v,r=old.build_model();m=audit.read(audit.ROOT/'data/model.json');c=audit.read(audit.ROOT/'data/certificate.json')
        old.check_model(m,v,r)
        self.assertEqual(old.replay_certificate(c,v,r)['reduced_upper'],'-1330103235427/500000000')
        self.assertEqual(old.check_diagnostic(m,v,r),-19318)
        self.assertEqual(len(audit.corruptions222(m,c,v,r)),11)

    def test_223_full_reconstruction_and_certificate_mutations(self):
        v,r=new.build_model();base=audit.ROOT/'audit/data/scout'
        m=audit.read(base/'POINT_LINK_65_MODEL.json');c=audit.read(base/'POINT_LINK_65_EXACT_UPPER_CERTIFICATE.json')
        new.check_model(m,v,r)
        self.assertEqual(new.replay_certificate(c,v,r)['reduced_upper'],'-121049912921/100000000')
        self.assertEqual(len(new.mutations(m,c,v,r)),11)

    def test_all_degree_cases_and_avoidance_needed(self):
        result=new.peta_arithmetic()
        self.assertEqual(result['chord_cases'],557)
        self.assertEqual(result['contradictions'],{'64':-7086,'65':-63})
        self.assertEqual(result['generic_degree19_envelope_violation'],12)

    def test_support_universe_and_supplied_witnesses(self):
        self.assertEqual(new.support_audit()['total_candidate_pairs'],79680)
        self.assertEqual(len(audit.extended_support_checks()),4)

    def test_padding_complete_and_incomplete_boundaries(self):
        fixture=new.small_fixtures()
        self.assertEqual(fixture['triple_multisets_checked'],1287)
        self.assertEqual(fixture['pair_multisets_checked'],210)
        self.assertEqual(fixture['duplicate_omission_objective_error'],6)
        self.assertTrue(fixture['complete_padding_fixture'])
        self.assertTrue(fixture['incomplete_cover_guard_fixture'])

    def test_reject_bool_and_fractional_matrix_coefficients(self):
        v,r=old.build_model();damaged=copy.deepcopy(v);damaged[0]['lower']=False
        with self.assertRaises(ValueError):audit.check_integer_structure(damaged,r)
        damaged=copy.deepcopy(r);damaged[0]['coefficients']['n0']=1.0
        with self.assertRaises(ValueError):audit.check_integer_structure(v,damaged)

if __name__=='__main__':unittest.main()
