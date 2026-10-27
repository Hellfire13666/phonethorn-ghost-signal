import unittest
from unittest.mock import patch
from phonethorn.fusion import number_variants, web_echo, inspect_public_business_page, twilio_line_type, fusion_evidence, _public_https_host

class FusionTests(unittest.TestCase):
    def test_variants(self):
        self.assertIn('+14155552671', number_variants('+14155552671'))
    def test_search(self):
        r = web_echo('+14155552671')
        self.assertIn('no result scraping', r['mode'])
        self.assertGreaterEqual(len(r['public_business_searches']), 2)
    def test_no_credentials_no_network(self):
        with patch.dict('os.environ', {}, clear=True):
            self.assertEqual(twilio_line_type('+14155552671')['status'], 'not_configured')
    def test_private_destination(self):
        with self.assertRaises(ValueError): _public_https_host('http://example.com')
        with self.assertRaises(ValueError): _public_https_host('https://localhost/contact')
    def test_fusion_no_gps(self):
        out = fusion_evidence({'number_intelligence': {'valid': True}, 'web_echo':{}})
        self.assertFalse(out['live_gps_from_number'])
        self.assertEqual(len(out['evidence']), 2)

if __name__ == '__main__': unittest.main()
