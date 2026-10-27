import contextlib, io, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from phonethorn.cli import main
class OutputTests(unittest.TestCase):
 def call(self, args):
  b=io.StringIO()
  report={"number_intelligence":{"international":"+1 415-555-2671","valid":True,"region_description":"California","number_type":"FIXED_LINE_OR_MOBILE","time_zone_hints":["America/Los_Angeles"]},"web_echo":{"variants":["+14155552671"],"reference_count":4,"public_business_searches":[{"google":"https://www.google.com/search?q=test"}]},"fusion_evidence":{"evidence":[]}}
  with patch('phonethorn.cli.make_report',return_value=report), patch('phonethorn.cli.web_echo',return_value=report['web_echo']):
   with contextlib.redirect_stdout(b):
    result=main(args)
  return result,b.getvalue()
 def test_clean_default(self):
  ok,txt=self.call(['--phone','+14155552671','--web-intel'])
  self.assertEqual(ok,0)
  self.assertIn('◆ PUBLIC RESEARCH',txt)
  self.assertNotIn('public_business_searches:',txt)
  self.assertNotIn('https://www.google.com/search?',txt)
 def test_verbose_retains_details(self):
  ok,txt=self.call(['--phone','+14155552671','--web-intel','--verbose'])
  self.assertEqual(ok,0)
  self.assertIn('https://www.google.com/search?',txt)
 def test_quiet_no_research_dump(self):
  ok,txt=self.call(['--phone','+14155552671','--web-intel','--quiet'])
  self.assertEqual(ok,0)
  self.assertNotIn('PUBLIC RESEARCH',txt)
 def test_report_names_not_home_paths(self):
  with tempfile.TemporaryDirectory() as d:
   ok,txt=self.call(['--phone','+14155552671','--web-intel','--out',d])
   self.assertEqual(ok,0)
   self.assertIn('[SAVED]',txt)
   self.assertNotIn(d,txt)
   self.assertGreater(len(list(Path(d).iterdir())),0)
