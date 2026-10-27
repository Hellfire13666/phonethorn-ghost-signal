# PHONETHORN // GHOST SIGNAL v0.6.3

![PHONETHORN Cosmic Kitty official cover](PHONETHORN-COVER.png)

**COSMIC KITTIES · CLEAN SIGNAL · GLITCHBYTE PHANTOM LABS**

PHONETHORN is a **phone-number metadata and public-contact research toolkit**, with separate tools for *your own* lost-phone recovery and locally provided location evidence. It **does not** reveal the owner, exact address or live GPS location of a phone number.

## What a phone search actually does

| Mode | Result | Limitation |
| --- | --- | --- |
| `--phone NUMBER` | Validity, standardized formats, numbering region, type and original carrier hint | Not subscriber identification or a verified present-day carrier |
| `--web-intel` | Clickable public search-engine queries for possible public appearances of the number | Research links, **not fetched or verified search hits** |
| `--web-url URL` | Checks one specified public HTTPS business contact page for a textual phone-number mention | A match does not prove ownership |
| `--fusion` | Clearly labeled combination of available evidence | Does not acquire private data |
| `--carrier` | Optional Twilio line-type intelligence | Credentials and provider charges required |
| `--rescue android/iphone` | Official personal lost-device recovery pointers | Use your own account to view device location |
| `--geo-ip`, `--coords`, `--photo-gps` | Separate approximate IP or locally supplied location clues | Not telephone-number-based GPS |

## One-paste Debian-based Linux install

```bash
sudo apt update && sudo apt install -y git python3 python3-venv &&
git clone https://github.com/Hellfire13666/phonethorn-ghost-signal.git phonethorn-ghost-signal &&
cd phonethorn-ghost-signal &&
bash ./INSTALL.sh && bash ./RUN.sh --version
```

If the destination already exists, use [README-UPGRADE.md](README-UPGRADE.md), not another clone over it.

## Beginner phone-search recipes

Run these from the repository directory. The example number is illustrative; substitute **your own number or one you are authorized to research**.

```bash
# Explore all available switches and Cosmic Kitty art
bash ./RUN.sh --menu
bash ./RUN.sh --show-art --banner kitty --theme neon
bash ./RUN.sh --examples

# Basic phone metadata, with tidy terminal output
bash ./RUN.sh --phone '+14155552671' --region US --output clean

# Prepare public web-search links (does not fetch search results)
bash ./RUN.sh --phone '+14155552671' --web-intel

# Run combined public-source research; save local full-art report
bash ./RUN.sh --phone '+14155552671' --web-intel --fusion --popup-results --out ./PhoneThornReports

# Inspect a business contact page you explicitly select
bash ./RUN.sh --phone '+14155552671' --web-url https://example.org/contact

# Technical details versus minimal terminal output
bash ./RUN.sh --phone '+14155552671' --fusion --verbose
bash ./RUN.sh --phone '+14155552671' --fusion --quiet

# Official lost-device help for your own phone
bash ./RUN.sh --rescue android
bash ./RUN.sh --rescue iphone

# Optional paid provider intelligence: requires configured Twilio credentials
# bash ./RUN.sh --phone '+14155552671' --carrier
```

Explore more examples in [COSMIC_KITTIES_EXAMPLES.md](COSMIC_KITTIES_EXAMPLES.md) and [EXAMPLES.md](EXAMPLES.md). The approved cover is stored as [PHONETHORN-COVER.png](PHONETHORN-COVER.png). The full-art local HTML research board embeds that cover when present.

## Privacy and scope

Phone metadata cannot locate a device or identify a private person. Public links are starting points for manual verification, not evidence of a match. Saved reports may include phone numbers and should remain private. Live third-party features are opt-in; carrier service may be billed. Never commit credentials, personal reports, or workstation-specific paths.

## Check your installation

```bash
python3 -B -m unittest discover -s tests -v
```

**Commit identity:** Hellfire13666 <79127597+Hellfire13666@users.noreply.github.com>.
