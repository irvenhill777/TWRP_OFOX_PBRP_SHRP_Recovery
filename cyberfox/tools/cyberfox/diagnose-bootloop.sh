#!/sbin/sh
# CYBERFOX read-only bootloop diagnostic collector for Android recovery.
# Does not flash, erase, format, or modify boot-critical partitions.
OUT="/sdcard/CyberFox-Logs"
STAMP="$(date +%Y%m%d-%H%M%S 2>/dev/null)"
[ -n "$STAMP" ] || STAMP="unknown-time"
mkdir -p "$OUT" 2>/dev/null || OUT="/tmp"
LOG="$OUT/bluejay-bootloop-$STAMP.txt"

{
  echo "=== CYBERFOX BLUEJAY BOOTLOOP REPORT ==="
  date 2>/dev/null
  echo
  echo "=== DEVICE ==="
  getprop ro.product.device 2>/dev/null
  getprop ro.build.fingerprint 2>/dev/null
  getprop ro.boot.slot_suffix 2>/dev/null
  echo
  echo "=== SLOT / BOOT STATE ==="
  getprop ro.boot.slot 2>/dev/null
  getprop ro.boot.verifiedbootstate 2>/dev/null
  getprop ro.boot.flash.locked 2>/dev/null
  echo
  echo "=== MOUNTS ==="
  mount 2>/dev/null
  echo
  echo "=== BLOCK DEVICES ==="
  ls -l /dev/block/by-name 2>/dev/null
  echo
  echo "=== RECOVERY LOG ==="
  cat /tmp/recovery.log 2>/dev/null
  echo
  echo "=== KERNEL LOG ==="
  dmesg 2>/dev/null
  echo
  echo "=== MODULES ==="
  lsmod 2>/dev/null
} > "$LOG" 2>&1

echo "CYBERFOX report saved to: $LOG"
echo "This report is diagnostic only. Review it before attempting any repair."
