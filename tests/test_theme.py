import unittest
from phonethorn.cli import render_html, coordinate_geo, EXAMPLES, VERSION
class ThemeTest(unittest.TestCase):
 def test_skin(self):
  page=render_html({'tool':'PHONETHORN','x':'<script>'})
  self.assertIn('COSMIC KITTIES',page)
  self.assertNotIn('<script>',page)
 def test_examples(self):
  self.assertIn('--rescue iphone', EXAMPLES)
 def test_coordinate(self):
  self.assertIn('openstreetmap.org',coordinate_geo(1,2)['map_url'])
 def test_version(self):
  self.assertEqual(VERSION,'0.5.0')
