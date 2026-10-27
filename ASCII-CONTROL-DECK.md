# PHONETHORN ASCII CONTROL DECK

The original terminal artwork is part of PHONETHORN, not a downloaded image. Choose a kitty, ghost, or signal-tower banner and a theme. Artwork changes **display only**, never phone data, network activity or saved reports.

```bash
# Preview original ASCII artwork without searching or processing anything
./RUN.sh --show-art --banner kitty --theme neon
./RUN.sh --show-art --banner ghost --theme ember
./RUN.sh --show-art --banner signal --theme frost

# Minimal terminal output, no decorative art
./RUN.sh --no-banner --examples

# Example offline phone format inspection, fictional documentation number
./RUN.sh --phone "+14155552671" --theme mono --color never

# Save reports using the existing supported options
./RUN.sh --phone "+14155552671" --fusion --out ./PhoneThornReports --banner ghost --theme frost
```

Available switches: `--banner kitty|ghost|signal`, `--theme neon|ember|frost|mono`, `--show-art`, `--no-banner`, and existing `--color auto|always|never`.

The artwork follows the normal color controls: non-interactive output uses no ANSI color by default, `--color always` forces colors where supported, and `--color never` removes them. `NO_COLOR` is honored.
