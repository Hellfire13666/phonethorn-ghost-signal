

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

