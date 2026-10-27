import io
import unittest
from contextlib import redirect_stdout

from phonethorn.cli import main
from phonethorn.terminal_art import ART, THEMES, banner


class TerminalArtTests(unittest.TestCase):
    def test_all_art_styles_plain_text(self):
        for style in ART:
            with self.subTest(style=style):
                stream = io.StringIO()
                banner(style=style, color="never", stream=stream)
                output = stream.getvalue()
                self.assertIn("PHONETHORN", output)
                self.assertNotIn("\033[", output)

    def test_all_themes(self):
        for theme in THEMES:
            with self.subTest(theme=theme):
                stream = io.StringIO()
                banner(style="kitty", theme=theme, color="always", stream=stream)
                self.assertIn("PHONETHORN", stream.getvalue())
                if theme == "mono":
                    self.assertNotIn("\033[", stream.getvalue())

    def test_show_art_and_quiet_switch(self):
        for style in ART:
            with self.subTest(style=style):
                stream = io.StringIO()
                with redirect_stdout(stream):
                    result = main(["--show-art", "--banner", style, "--color", "never"])
                self.assertEqual(result, 0)
                self.assertIn("PHONETHORN", stream.getvalue())
        stream = io.StringIO()
        with redirect_stdout(stream):
            result = main(["--no-banner", "--show-art"])
        self.assertEqual(result, 0)
        self.assertEqual(stream.getvalue(), "")

    def test_existing_examples_still_works(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            result = main(["--examples", "--no-banner"])
        self.assertEqual(result, 0)
        self.assertIn("--rescue iphone", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
