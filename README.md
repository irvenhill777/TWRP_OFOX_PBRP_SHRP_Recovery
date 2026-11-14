# Boston OrangeFox + Rescue Center (XT2419-1)

This is a **repo add-on / integration starter**, not a prebuilt recovery image.

Target device:
- Motorola Moto G Stylus 5G (2024)
- Model: XT2419-1
- Codename: `boston`
- Qualcomm platform family: `parrot`
- Architecture: `arm64`

## Important compatibility status

The Boston device tree previously identified at `PizzaG/android_device_motorola_boston` is a **TWRP tree**. It is not confirmed to be an OrangeFox Recovery Project (OFRP) tree. The included workflow deliberately checks for `fox_boston.mk` and stops with a clear error if it is missing. Do not rename a TWRP product makefile and assume it is OrangeFox-compatible.

The workflow is a clean Boston-oriented starting point. It does not apply the old M5A-specific vibrator, flashlight, DRM, display-resolution, or maintainer-image patches.

## Contents

- `.github/workflows/OrangeFox-OFRP-Boston.yml` — manually triggered OFRP build workflow.
- `rescue/` — shell-based recovery rescue utilities.
- `device-tree-snippets/` — integration examples for a compatible Boston OFRP tree.
- `rescue/README.md` — installation and safety notes.

## What is implemented

- Read-only device/partition diagnostics.
- A backup script for a short allowlist of boot-chain partitions, only when the exact by-name node exists.
- A guarded raw-image restore utility. It is dry-run by default, rejects dynamic/data/radio/bootloader partitions, checks SHA-256, image size, device identity, and requires an exact typed confirmation before writing.
- A data diagnostics report. It does not run filesystem repair or format commands.
- A fastbootd reboot helper.
- A text-mode menu for recovery shell use.

## What is intentionally NOT implemented

- No native OrangeFox touchscreen GUI page. That requires integration with the actual OFRP GUI/theme framework and testing in the selected manifest.
- No automatic Motorola CFC XML/service-package flasher. Motorola service packages are host-side fastboot scripts and must be handled with the exact firmware package and partition map.
- No raw flashing of `system`, `vendor`, `product`, `system_ext`, `super`, `userdata`, `metadata`, `persist`, modem/radio, GPT, bootloader, or partition table.
- No automatic wipe, format, slot switch, or bootloader relock.
- No `recovery.img` flashing target until the actual XT2419-1 partition layout confirms a dedicated recovery partition.

## Before building

1. Fork the upstream builder recommended by the source repository:  
   https://github.com/mlm-games/TWRP_OFOX_PBRP_SHRP_Recovery_Builder
2. Add a **real Boston OrangeFox-compatible device tree**. It must provide the OFRP product makefile `fox_boston.mk`, BoardConfig, required dependencies, and proprietary files.
3. In GitHub Actions, run **OrangeFox OFRP Boston**.
4. Set `DEVICE_TREE_URL`, `DEVICE_TREE_BRANCH`, and `DEVICE_PATH` to the compatible OFRP tree.
5. Review the build log and artifact. A successful compile does not prove the image is safe to flash.

## Device-side rescue scripts

Copy `rescue/` to the recovery device (for example, `/sdcard/Fox/RescueCenter/`) and run:

```sh
sh /sdcard/Fox/RescueCenter/rescue-center.sh
```

Some OrangeFox builds may not mount internal storage at `/sdcard`; adjust the path accordingly.

### Restore utility

Restore is disabled unless all conditions are met:
- The recovery reports a Boston-family product property.
- The requested exact partition node exists under `/dev/block/by-name/`.
- The target name is on the limited boot-chain allowlist.
- A `SHA256SUMS` file is present beside the image and validates.
- The image is no larger than the target partition.
- The operator passes `--write` and types `RESTORE <partition-name>` exactly.

This is still a low-level write operation. Use it only with an image proven to belong to the exact XT2419-1 firmware/build and the correct slot. If any check is unclear, do not flash.

## Known unknowns

The actual XT2419-1 by-name partition map, active slot, exact recovery placement, OrangeFox-compatible device tree, and matching firmware image hashes have not been verified here. The scripts do not guess these details.
