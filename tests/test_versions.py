import unittest
from phonethorn import VERSION as package_version
from phonethorn.cli import VERSION as cli_version
class VersionConsistencyTests(unittest.TestCase):
 def test_consistency(self):
  self.assertEqual(package_version,'0.6.3')
  self.assertEqual(cli_version,package_version)
