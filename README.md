# PHONETHORN // GHOST SIGNAL 🐈‍⬛🌌

![PHONETHORN Cosmic Kitties cover](phonethorn_ghost_signal_cyber_station.png)

**AnonymissGlitch · Cosmic Kitties Edition · v0.5.0**  
A featured **GlitchByte Phantom Labs** project for phone-number metadata, public business-contact references, optional carrier lookups, GEO utilities, recovery guidance, and evidence reports.

> **Before installing:** Verify that `INSTALL.sh`, `requirements.txt`, and the `phonethorn/` source folder are present at the repository root. The cover displays once `phonethorn_ghost_signal_cyber_station.png` is uploaded to the root.

## 🐾 One-paste installation (MX Linux / Debian)

First-time installation, after all source files have been uploaded:

```bash
sudo apt update && sudo apt install -y git python3 python3-venv &&
git clone https://github.com/Hellfire13666/phonethorn-ghost-signal.git "$HOME/phonethorn-ghost-signal" &&
bash "$HOME/phonethorn-ghost-signal/INSTALL.sh" &&
"$HOME/.local/bin/phonethorn" --examples
```

Requires an internet connection for dependency installation. If `phonethorn` is not in your PATH, run `"$HOME/.local/bin/phonethorn"`.

## 📱 Phone intel recipes

```bash
# Start with a safe demo number (replace only with your own or authorized numbers)
phonethorn --phone "+14155552671" --region US

# Generate public search-engine links (does not automatically scrape search results)
phonethorn --phone "+14155552671" --web-intel

# Check a specific public business contact page
phonethorn --phone "+14155552671" --web-url "https://example.org/contact"

# Fusion analysis and HTML / JSON / TXT reports
phonethorn --phone "+14155552671" --fusion --out "$HOME/PhoneThornReports"
```

## 🌍 GEO recipes

```bash
# Public IP geography (approximate; not phone GPS)
phonethorn --geo-ip 8.8.8.8 --live-geo

# Plot coordinates already known to you
phonethorn --coords 40.7128 -74.0060

# Check GPS metadata in your own picture (optional Pillow dependency)
phonethorn --photo-gps "$HOME/Pictures/my-own-photo.jpg"
```

## 🛟 Recovery & diagnostics

```bash
phonethorn --rescue android
phonethorn --rescue iphone
phonethorn --devices
phonethorn --examples
```

## 📡 Optional Carrier Signal

```bash
# Uses optional Twilio credentials and can incur provider fees
phonethorn --phone "+14155552671" --carrier
```

Set up your own credentials privately according to the package documentation; **never commit API keys to GitHub**.

## 🔎 What this tool actually does

- Offline number formatting and metadata with the `phonenumbers` library.
- Web Echo produces links to manually search public sources; it does **not** harvest private account data.
- A user-specified business webpage may be checked for a public phone-number mention.
- GEO separates IP geography, coordinates, and photo metadata, which **cannot locate a phone just from its number**.
- Optional paid carrier intelligence; no paid request made by `--fusion` alone.
- Evidence Vault reports to locally specified output folders.

Run the bundled unit tests:

```bash
python3 -m unittest discover -s tests -v
```

**Lab home:** [GlitchByte Phantom Labs](https://github.com/Hellfire13666/glitchbyte-phantom-labs)  
**Project:** PHONETHORN // GHOST SIGNAL · Cosmic Kitties Edition  
**License:** MIT (see repository `LICENSE` file once uploaded).
