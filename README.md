# PHONETHORN // GHOST SIGNAL 🐈‍⬛🌌

![PHONETHORN: Rosie and Cosmic Kitty](PHONETHORN-COVER.png)

**AnonymissGlitch · Cosmic Kitties Edition · v0.5.0**  
A special [GlitchByte Phantom Labs](https://github.com/Hellfire13666/glitchbyte-phantom-labs) toolkit for phone metadata, public contact references, GEO utilities, personal lost-device recovery, and evidence reports.

> The cover above requires `PHONETHORN-COVER.png` at the repository root. If the picture does not appear, upload the PNG with that exact filename.

## 🐾 One-paste install — Debian-based Linux

Copy this **whole block** into a terminal for a first-time installation:

```bash
sudo apt update &&
sudo apt install -y git python3 python3-venv &&
git clone https://github.com/Hellfire13666/phonethorn-ghost-signal.git "$HOME/phonethorn-ghost-signal" &&
bash "$HOME/phonethorn-ghost-signal/INSTALL.sh" &&
"$HOME/.local/bin/phonethorn" --version &&
"$HOME/.local/bin/phonethorn" --examples
```

**Already have a folder named `~/phonethorn-ghost-signal`?** Don't clone over it. For an existing clean Git clone, use:

```bash
cd "$HOME/phonethorn-ghost-signal" &&
git pull --ff-only &&
bash ./INSTALL.sh &&
"$HOME/.local/bin/phonethorn" --examples
```

The installer creates a Python virtual environment, installs the published requirements, and adds `~/.local/bin/phonethorn`. Python dependencies require internet access. If `phonethorn` is not on your PATH, use `"$HOME/.local/bin/phonethorn"`.

## 📱 Easy phone recipes

```bash
# Number metadata (illustrative number)
phonethorn --phone "+14155552671" --region US

# Generate public search links; does NOT automatically scrape results
phonethorn --phone "+14155552671" --web-intel

# Check a specified, public business-contact page
phonethorn --phone "+14155552671" --web-url "https://example.org/contact"

# Combine free evidence and save HTML, JSON and TXT reports
phonethorn --phone "+14155552671" --fusion --out "$HOME/PhoneThornReports"
```

## 🌍 GEO recipes

```bash
# Approximate public IP geolocation (not a mobile phone's GPS)
phonethorn --geo-ip 8.8.8.8 --live-geo

# Map coordinates supplied by you
phonethorn --coords 40.7128 -74.0060

# Read GPS EXIF metadata from a photo you own; optional Pillow dependency
phonethorn --photo-gps "$HOME/Pictures/my-own-photo.jpg"
```

## 🛟 Lost-phone recovery and device checks

```bash
phonethorn --rescue android
phonethorn --rescue iphone
phonethorn --devices
phonethorn --examples
```

## 📡 Optional carrier lookup

```bash
# May incur Twilio API charges; requires your configured credentials
phonethorn --phone "+14155552671" --carrier
```

The tool uses optional Twilio Lookup v2 line-type intelligence. Set your own `TWILIO_API_KEY` and `TWILIO_API_SECRET` privately. **Never commit keys, private phone reports, or secret environment files to GitHub.** The ordinary `--fusion` command does not invoke the paid carrier lookup on its own.

## 🔎 What the modules mean

| Module | What it actually provides |
| --- | --- |
| Phone Intel | Number formats, numbering region, validity, possible type and carrier hints |
| Web Echo | Manual search-engine links for publicly indexed number references |
| Business Page Intel | Matches number mentions on one user-selected public HTTPS page |
| Carrier Signal | Optional paid line-type/carrier information where provider data is available |
| GEO | Approximate IP geography, supplied coordinates, photo EXIF metadata |
| Evidence Vault | Local HTML, JSON and TXT reports with source labels |
| Recovery | Official recovery guidance for your own missing devices |

A phone number alone **cannot provide live device GPS**. Public number reports can be inaccurate, out of date, or affected by number portability and spoofing. The tool is meant for your own numbers, authorized inquiries, and legitimately public business information, not private-account enumeration.

## 🧪 Tests

```bash
cd "$HOME/phonethorn-ghost-signal"
./RUN.sh --examples
python3 -m unittest discover -s tests -v
```

Local automated tests have been performed on packaged versions, but this public repository install still needs a real Debian-based Linux clean-install check. Live external providers were not verified in those offline tests.

**Part of:** GlitchByte Phantom Labs · AnonymissGlitch · Cosmic Kitties  
**License:** MIT, see [LICENSE](LICENSE).
