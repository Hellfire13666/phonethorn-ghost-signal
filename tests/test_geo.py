import unittest
from phonethorn.cli import ip_geo,coordinate_geo,photo_geo
class GeoTests(unittest.TestCase):
 def test_public_ip_offline(self):
  r=ip_geo('8.8.8.8'); self.assertTrue(r['is_global']); self.assertNotIn('approximate_geography',r)
 def test_private_ip(self):
  self.assertFalse(ip_geo('192.168.1.10')['is_global'])
 def test_coords(self):
  self.assertIn('openstreetmap.org',coordinate_geo(40,-74)['map_url'])
 def test_bad_coords(self):
  with self.assertRaises(ValueError): coordinate_geo(95,0)
