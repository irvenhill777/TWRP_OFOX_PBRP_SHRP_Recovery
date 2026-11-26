# CYBERFOX BLUEJAY — OrangeFox R12.1 theme overlay

A dark cyberpunk theme overlay for OrangeFox Recovery, targeted at the Pixel 6a (`bluejay`).

## What this bundle changes

- Dark navy/black surfaces with electric-blue and cyan accents.
- Cyan controls, selected states, progress indicators, and status colors.
- Custom vector CyberFox logo and splash background.
- A **CYBERFOX // Recovery Guide** entry in Advanced.
- A help page explaining the existing recovery operations and safe troubleshooting workflow.
- A source-overlay script that applies the theme to an OrangeFox source checkout.

The theme does not add new partition-flashing capabilities. The guide page routes to existing OrangeFox pages and describes what they do. It does not create a fake “one-click bootloop repair” action.

## Apply to an OrangeFox source tree

From the root of the OrangeFox source checkout:

```bash
python3 /path/to/CyberFox-Bluejay/apply-cyberfox-theme.py --source .
```

The script locates `bootable/recovery/gui/theme/portrait_hdpi`, validates XML, and makes timestamped backups before changing existing theme files.

You can also pass the theme directory directly:

```bash
python3 apply-cyberfox-theme.py --theme-dir bootable/recovery/gui/theme/portrait_hdpi
```

## Build-workflow integration

In the existing OrangeFox GitHub Actions workflow, add this step **after manifest sync and before `lunch` / `mka`**:

```yaml
- name: Apply CYBERFOX Bluejay theme
  run: |
    set -euo pipefail
    python3 "$GITHUB_WORKSPACE/cyberfox/apply-cyberfox-theme.py" \
      --source "$ORANGEFOX_ROOT"
```

Place this bundle's `cyberfox/` directory in the repository root. If the workflow uses a different checkout path, adjust the script path only.

## Important compatibility note

The repository's currently inspected `OrangeFox-OFRP.yml` workflow has M5A defaults and M5A-specific patches. Applying a theme does not make that workflow a Pixel 6a build. Before producing a flashable `bluejay` image, the build must use a verified Pixel 6a device tree and the correct Tensor Pixel `vendor_boot` build/installation flow. Do not flash a build merely because the theme overlay validates.

The modern Tensor Pixel OrangeFox source tree documents a universal AIO payload and recovery in `vendor_boot`; use its current maintainer instructions and device configuration as the compatibility reference:
https://github.com/leegarchat/twrp_device_google_pixels

## Validation

```bash
python3 apply-cyberfox-theme.py --theme-dir /path/to/portrait_hdpi --check-only
```

The script checks the expected R12.1 theme files and XML syntax. A successful check is not a device boot test.
