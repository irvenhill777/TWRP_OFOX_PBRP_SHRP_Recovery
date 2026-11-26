# CYBERFOX build integration

## Intended source layout

The overlay expects the OrangeFox R12.1 GUI theme at:

`bootable/recovery/gui/theme/portrait_hdpi/`

It applies:
- `themes/style.xml` dark palette and cool icon tints
- `themes/accent.xml` blue/cyan accent
- `splash.xml` and vector artwork
- `pages/cyberfox.xml` help page
- a navigation item in the existing Advanced page
- an include entry in `ui.xml`

## GitHub Actions step

Add this after `orangefox_sync.sh` and before `lunch`:

```yaml
- name: Apply CYBERFOX Bluejay theme
  run: |
    set -euo pipefail
    python3 "$GITHUB_WORKSPACE/cyberfox/apply-cyberfox-theme.py" \
      --source "$ORANGEFOX_ROOT"
```

If the bundle is stored in a different directory, update the path to `apply-cyberfox-theme.py`.

## Device build warning

The currently inspected workflow in this repository is configured for `M5A`, not `bluejay`. It applies M5A-specific patches and selects a product named from `DEVICE_NAME`. Do not simply change the codename string and flash the output.

Pixel 6a is a Tensor G1 device. Use a verified bluejay tree and the corresponding `vendor_boot` recovery installation process. The current Tensor Pixel source documentation describes a universal AIO package that keeps the stock kernel and delivers the recovery ramdisk to `vendor_boot`:
https://github.com/leegarchat/twrp_device_google_pixels

## What this overlay does not do

- It does not change partition maps, fstab, kernel, AVB, encryption, or boot images.
- It does not automatically repair a bootloop.
- It does not flash boot, init_boot, vendor_boot, vbmeta, or super.
- It does not prove the image boots on physical hardware.

## Safe rescue direction

The bundled `diagnose-bootloop.sh` only collects properties, mount state, block-device names, recovery log, kernel log, and loaded modules. It is deliberately read-only. Use the collected evidence to identify the actual failure before selecting a compatible stock image or repair package.
