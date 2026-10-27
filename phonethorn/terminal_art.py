"""Original ASCII launch artwork for PHONETHORN; no external images or system details."""
import os
import sys

ART = {
    "kitty": r"""
      /\_/\        .  *  .     [ COSMIC SIGNAL ]
     ( o.o )  . *    /\     .  FREQUENCY: OPEN
      > ^ <      .  /__\       PHONETHORN // GHOST SIGNAL
    """,
    "ghost": r"""
       .--.           . * .     [ GHOST SIGNAL ]
      / .-.|   .   .          TRANSMISSION: READY
      | | | |    *      .     PHONETHORN // PHANTOM LABS
      |_| |_|  .  *  .
    """,
    "signal": r"""
         /\          .   .      [ SIGNAL TOWER ]
        /  \       .  |  .     PUBLIC SIGNALS ONLY
       / /\ \    .   |||   .   PHONETHORN // FIELD OPS
      /_/  \_\       |||
    """,
}
THEMES = {
    "neon": ("\033[95m", "\033[96m"),
    "ember": ("\033[91m", "\033[93m"),
    "frost": ("\033[96m", "\033[94m"),
    "mono": ("", ""),
}
RESET = "\033[0m"

def banner(style="kitty", theme="neon", color="auto", stream=None):
    if style not in ART:
        raise ValueError("Unknown PHONETHORN banner")
    if theme not in THEMES:
        raise ValueError("Unknown PHONETHORN theme")
    out = stream if stream is not None else sys.stdout
    enabled = (color == "always" or (color == "auto" and getattr(out, "isatty", lambda: False)())) and theme != "mono" and "NO_COLOR" not in os.environ
    primary, secondary = THEMES[theme]
    lines = ART[style].strip("\n").splitlines()
    for index, line in enumerate(lines):
        prefix = primary if index % 2 == 0 else secondary
        print(prefix + line.rstrip() + (RESET if prefix else "") if enabled else line.rstrip(), file=out)
    print("  v0.5.0  |  evidence > assumptions  |  help: --examples", file=out)
