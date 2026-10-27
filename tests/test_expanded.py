import unittest
from phonethorn.fusion import web_echo
from phonethorn.board import board_html
class Expanded(unittest.TestCase):
 def test_references(self):
  results=web_echo('+14155552671')
  self.assertGreaterEqual(results['reference_count'],20)
  self.assertEqual(len(results['public_search_references'][0]['engines']),4)
  self.assertIn('no result scraping',results['mode'])
 def test_safe_html(self):
  html=board_html({'web_echo':{'reference_count':0},'name':'<script>alert(1)</script>'})
  self.assertNotIn('<script>alert(1)</script>',html)
  self.assertIn('PHONETHORN',html)
if __name__=='__main__':unittest.main()
