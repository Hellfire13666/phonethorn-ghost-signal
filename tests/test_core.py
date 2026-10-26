import tempfile
import unittest
from pathlib import Path
from phonethorn.cli import make_report, render_html, save_report, public_links, rescue_steps
class Tests(unittest.TestCase):
    def test_rescue(self):
        r = make_report(rescue='android')
        self.assertEqual(r['find_device_url'], 'https://android.com/find')
        self.assertTrue(rescue_steps('iphone'))
    def test_html_escape(self):
        r = make_report(rescue='iphone')
        r['test'] = '<script>alert(1)</script>'
        self.assertNotIn('<script>', render_html(r))
    def test_save(self):
        with tempfile.TemporaryDirectory() as temp:
            names = save_report(make_report(rescue='android'), temp, 'all')
            self.assertEqual(len(names), 3)
            self.assertTrue(all(Path(x).exists() for x in names))
    def test_public_links(self):
        self.assertIn('google.com/search', public_links('+14155552671')['web_search'])
    def test_phone_when_dependency_present(self):
        try:
            import phonenumbers
        except ImportError:
            self.skipTest('phonenumbers dependency not installed')
        from phonethorn.cli import lookup
        data = lookup('+14155552671', 'US')
        self.assertIn('geo_warning', data)
        self.assertNotIn('live_gps', data)
if __name__ == '__main__': unittest.main()
