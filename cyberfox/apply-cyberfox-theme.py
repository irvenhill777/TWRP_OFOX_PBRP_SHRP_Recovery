#!/usr/bin/env python3
"""Apply the CYBERFOX Bluejay theme overlay to an OrangeFox R12.1 theme tree."""
from __future__ import annotations
import argparse
import datetime as dt
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACCENT = HERE / "theme" / "accent.xml"
PAGE = HERE / "theme" / "pages" / "cyberfox.xml"
SPLASH = HERE / "theme" / "splash.xml"
LOGO = HERE / "theme" / "images" / "SVG" / "Logos" / "cyberfox.svg"
BG = HERE / "theme" / "images" / "Splash" / "cyberfox_bg.svg"

VARS = {
    "primary_50": "#E5FAFF", "primary_100": "#B9F0FF",
    "primary_200": "#8CE4FF", "primary_300": "#5AD6FF",
    "primary_400": "#2CCBFF", "primary_500": "#12B8F5",
    "primary_600": "#079BD8", "primary_700": "#087DBB",
    "primary_800": "#075F91", "primary_900": "#06466B",
    "neutral_100": "#DDF7FF", "neutral_200": "#B5D9E8",
    "neutral_300": "#82AFC3", "neutral_400": "#648EA5",
    "neutral_500": "#456B83", "neutral_600": "#29485F",
    "neutral_700": "#183247", "neutral_800": "#0D2032",
    "neutral_900": "#050D18",
    "background": "#050D18", "power_bg": "#081727",
    "power_hl": "#16BFFF44", "highlight_color": "#0B3B5A",
    "highlight_color_full": "#105277",
    "text": "#DDF7FF", "text_secondary": "#8FC6DB",
    "text_action": "#54D8FF", "text_status": "#A9EFFF",
    "text_menu": "#DDF7FF", "text_light": "#DDF7FF",
    "text_hl_btn": "#03101C", "text_dark": "#0D2032",
    "disabled_bg": "#183247", "disabled_text": "#648EA5",
    "linecolor": "#25BFFF55", "darktransparent": "#050D18DD",
    "theme_style": "CyberFox", "theme_style_act": "CyberFox",
    "groupitems_clr": "#0A1B2B", "actbar_color": "#54D8FF",
    "neutral_light": "#183247", "cards_bg": "#0A1B2B",
    "keyboard_bg": "#0A1B2B", "keyboard_hl": "#16BFFF55",
}

# Recolor the existing R12 theme's baked-in warm icon tints without replacing
# its resource catalogue or page layout.
COLOR_REPLACEMENTS = {
    "#413327": "#BDEEFF",
    "#F9F1E7": "#071321",
    "#FFF8F2": "#0A1B2B",
    "#F0E1CC": "#102B43",
    "#eedfc8": "#0B3B5A",
    "#EEDFC8": "#0B3B5A",
    "#D86100": "#12B8F5",
    "#ed7002": "#12B8F5",
    "#ed6f02": "#12B8F5",
    "#E9E9E944": "#16BFFF33",
}

def locate_theme(args) -> Path:
    if args.theme_dir:
        return Path(args.theme_dir).resolve()
    if not args.source:
        raise SystemExit("Pass --source ORANGEFOX_ROOT or --theme-dir THEME_DIR")
    base = Path(args.source).resolve()
    candidates = [
        base / "bootable/recovery/gui/theme/portrait_hdpi",
        base / "gui/theme/portrait_hdpi",
        base,
    ]
    for candidate in candidates:
        if (candidate / "ui.xml").is_file():
            return candidate
    raise SystemExit(f"Could not locate portrait_hdpi/ui.xml under {base}")

def backup(path: Path):
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = path.with_name(path.name + ".cyberfox-backup-" + stamp)
    shutil.copy2(path, dst)

def patch_variables(path: Path):
    text = path.read_text(encoding="utf-8")
    for name, value in VARS.items():
        pattern = rf'(<variable\s+name="{re.escape(name)}"\s+value=")[^"]*(")'
        text, count = re.subn(pattern, rf'\g<1>{value}\2', text, count=1)
        if count == 0:
            # Some forks reorder attributes; handle value-before-name form.
            pattern = rf'(<variable\s+value=")[^"]*("\s+name="{re.escape(name)}")'
            text = re.sub(pattern, rf'\g<1>{value}\2', text, count=1)
    for old, new in COLOR_REPLACEMENTS.items():
        text = text.replace(old, new)
    ET.fromstring(text)  # fail before writing if malformed
    path.write_text(text, encoding="utf-8")

def patch_accent(path: Path):
    text = path.read_text(encoding="utf-8")
    for old, new in COLOR_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.replace('value="Fox"', 'value="CyberFox"')
    text = text.replace('value="#ed6f02"', 'value="#12B8F5"')
    text = text.replace('value="#D86100"', 'value="#087DBB"')
    ET.fromstring(text)
    path.write_text(text, encoding="utf-8")

def include_help_page(ui: Path):
    text = ui.read_text(encoding="utf-8")
    marker = '<xml name="/twres/pages/cyberfox.xml"/>'
    if marker not in text:
        if "</include>" not in text:
            raise RuntimeError("ui.xml has no </include> block; refusing unsafe patch")
        text = text.replace("</include>", f"\t\t{marker}\n\t</include>", 1)
    ET.fromstring(text)
    ui.write_text(text, encoding="utf-8")

def add_advanced_link(path: Path):
    text = path.read_text(encoding="utf-8")
    if "CYBERFOX // Recovery Guide" in text:
        return
    m = re.search(r'<page\s+name="advanced">([\s\S]*?)</page>', text)
    if not m:
        raise RuntimeError("Could not find the advanced page in pages/advanced.xml")
    body = m.group(1)
    lists = list(re.finditer(r'<listbox\b[^>]*>[\s\S]*?</listbox>', body))
    if len(lists) < 2:
        raise RuntimeError("Advanced page layout differs from expected R12.1 structure")
    target = lists[1]
    item = """
                <listitem name="CYBERFOX // Recovery Guide">
                    <icon res="overview"/>
                    <action function="page">cyberfox</action>
                </listitem>
"""
    new_body = body[:target.end()-len("</listbox>")] + item + body[target.end()-len("</listbox>"):]
    text = text[:m.start(1)] + new_body + text[m.end(1):]
    ET.fromstring(text)
    path.write_text(text, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="OrangeFox source root")
    ap.add_argument("--theme-dir", help="Direct portrait_hdpi theme directory")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()
    theme = locate_theme(args)
    required = [
        theme / "ui.xml", theme / "themes/style.xml",
        theme / "themes/accent.xml", theme / "pages/advanced.xml",
    ]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        raise SystemExit("Missing expected OrangeFox R12 theme files:\n" + "\n".join(missing))
    for p in required:
        ET.parse(p)
    if args.check_only:
        print(f"CYBERFOX CHECK OK: {theme}")
        return
    page_dir = theme / "pages"
    image_dir = theme / "images"
    (image_dir / "SVG/Logos").mkdir(parents=True, exist_ok=True)
    (image_dir / "Splash").mkdir(parents=True, exist_ok=True)
    targets = [
        theme / "themes/style.xml", theme / "themes/accent.xml",
        theme / "ui.xml", theme / "pages/advanced.xml",
        theme / "splash.xml",
    ]
    for p in targets:
        if p.exists():
            backup(p)
    shutil.copy2(PAGE, page_dir / "cyberfox.xml")
    shutil.copy2(LOGO, image_dir / "SVG/Logos/cyberfox.svg")
    shutil.copy2(BG, image_dir / "Splash/cyberfox_bg.svg")
    patch_variables(theme / "themes/style.xml")
    patch_accent(theme / "themes/accent.xml")
    include_help_page(theme / "ui.xml")
    add_advanced_link(theme / "pages/advanced.xml")
    shutil.copy2(SPLASH, theme / "splash.xml")
    ET.parse(theme / "ui.xml")
    ET.parse(theme / "pages/advanced.xml")
    ET.parse(theme / "pages/cyberfox.xml")
    ET.parse(theme / "splash.xml")
    print("CYBERFOX applied successfully.")
    print("Review the generated build on hardware before flashing.")
    print(f"Theme directory: {theme}")

if __name__ == "__main__":
    main()
