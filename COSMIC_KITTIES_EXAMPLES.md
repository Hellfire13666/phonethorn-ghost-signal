# PHONETHORN v0.6.3 // ANONYMISSGLITCH · COSMIC KITTIES 🐈‍⬛

Phone-number metadata, publicly documented business contacts, optional paid carrier line-type intelligence, local GEO analysis, and personal lost-device recovery. **No phone-number-to-live-GPS capability.**

## Install once on Debian-based Linux

```bash
cd "$HOME/PHONETHORN-v0.6.3-DEBIAN-CORRECTION" && bash ./INSTALL.sh
```

`~/.local/bin/phonethorn` is the launcher. `./RUN.sh` runs from the extracted folder even without installing.

## Recipes

```bash
phonethorn --examples
phonethorn --phone '+14155552671' --region US
phonethorn --phone '+14155552671' --web-intel
phonethorn --phone '+14155552671' --web-url https://example.org/contact
phonethorn --phone '+14155552671' --fusion --out "$HOME/PhoneThornReports"
phonethorn --phone '+14155552671' --carrier  # PAID when credentials configured
phonethorn --geo-ip 8.8.8.8 --live-geo
phonethorn --coords 40.7128 -74.0060
phonethorn --photo-gps "$HOME/Pictures/my-own-photo.jpg" # optional Pillow
phonethorn --devices
phonethorn --rescue android
```

**Web Echo** produces manual Google/Bing search links, not scraped results. `--web-url` checks one user-specified public HTTPS business page for a matching textual mention; it does not crawl links, bypass access controls, or identify private individuals. `--fusion` combines evidence with transparency labels and does not incur a paid API call unless `--carrier` is explicitly given.

**Carrier Signal** uses Twilio Lookup v2 `line_type_intelligence`, which incurs provider charges. To enable for an authorized number, obtain API credentials and `export TWILIO_API_KEY=...` and `export TWILIO_API_SECRET=...` in your own shell. Do not put secrets in reports or repos. Never send credentials to ChatGPT. Without keys, module reports `not_configured`. Provider data may be incomplete and is not an exact location.

**Evidence Vault** exports HTML, JSON and TXT, owner-only file permissions where supported. `--out` is required to save. Local reports may include phone numbers: handle as private data.

Run tests: `python3 -m unittest discover -s tests -v`. Live network/provider tests are not included; install and validate them in your own Debian-based Linux environment. Third-party provider rates, availability and terms can change.

Code MIT licensed. Original toolkit maintained independently; no unreviewed older Holmes code copied.
