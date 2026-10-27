import contextlib
import io
import unittest
from phonethorn.cli import main

class SwitchboardTests(unittest.TestCase):
    def run_cli(self, args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(args)
        return code, output.getvalue()

    def test_no_args_show_banner_and_switches(self):
        code, screen = self.run_cli([])
        self.assertEqual(code, 0)
        self.assertIn('PHONETHORN SWITCHBOARD', screen)
        self.assertIn('--phone NUMBER', screen)

    def test_menu_command(self):
        code, screen = self.run_cli(['--menu', '--no-banner'])
        self.assertEqual(code, 0)
        self.assertIn('PHONE SIGNALS', screen)

    def test_banner_standalone(self):
        code, screen = self.run_cli(['--show-art','--banner','ghost','--color','never'])
        self.assertEqual(code, 0)
        self.assertNotIn('SWITCHBOARD', screen)

    def test_normal_commands_not_intercepted(self):
        code, screen = self.run_cli(['--rescue','android','--no-banner'])
        self.assertEqual(code, 0)
        self.assertNotIn('SWITCHBOARD', screen)

if __name__ == '__main__':
    unittest.main()
