"""
Build weapon database JSON from Smithbox exports.
Run: python tools/build_weapon_db.py
Outputs: elden-ring/items/weapons/data/weapons.json
"""

import csv
import json
import os
import sys

# ── Paths ──────────────────────────────────────────────────────────────────────
PARAM_CSV    = r"C:\Users\pmaci\Desktop\Elden Ring Mods\unpacked er\param\EquipParamWeapon.csv"
FMG_FILES    = [
    r"C:\Users\pmaci\Desktop\Elden Ring Mods\unpacked er\.smithbox\Workflow\Exported Text\base_weapons.json",
    r"C:\Users\pmaci\Desktop\Elden Ring Mods\unpacked er\.smithbox\Workflow\Exported Text\dlc1_weapons.json",
]
OUT_DIR      = os.path.join(os.path.dirname(__file__), "..", "elden-ring", "items", "weapons", "data")
OUT_FILE     = os.path.join(OUT_DIR, "weapons.json")

# ── Weapon type map ────────────────────────────────────────────────────────────
WEP_TYPE = {
    "1":  "Dagger",
    "3":  "Straight Sword",
    "5":  "Greatsword",
    "7":  "Colossal Sword",
    "9":  "Curved Sword",
    "11": "Curved Greatsword",
    "13": "Katana",
    "14": "Twinblade",
    "15": "Thrusting Sword",
    "16": "Heavy Thrusting Sword",
    "17": "Axe",
    "19": "Greataxe",
    "21": "Hammer",
    "23": "Great Hammer",
    "24": "Flail",
    "25": "Spear",
    "28": "Great Spear",
    "29": "Halberd",
    "31": "Scythe",
    "35": "Fist",
    "37": "Claw",
    "39": "Whip",
    "41": "Colossal Weapon",
    "50": "Light Bow",
    "51": "Bow",
    "53": "Greatbow",
    "55": "Crossbow",
    "56": "Ballista",
    "57": "Glintstone Staff",
    "61": "Sacred Seal",
    "65": "Small Shield",
    "67": "Medium Shield",
    "69": "Greatshield",
    "87": "Torch",
    "88": "Hand-to-Hand",
    "89": "Perfume Bottle",
    "90": "Thrusting Shield",
    "91": "Smithscript (Dagger)",
    "92": "Backhand Blade",
    "93": "Light Greatsword",
    "94": "Great Katana",
    "95": "Beast Claw",
}

SCALING_GRADE = {
    "0": "-", "1": "E", "2": "D", "3": "C", "4": "B", "5": "A", "6": "S"
}


def load_fmg(paths):
    """Load names and captions from one or more Smithbox FMG JSON exports."""
    names, captions = {}, {}
    for path in paths:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for wrapper in data.get("FmgWrappers", []):
            fmg_name = wrapper["Name"]
            entries = wrapper["Fmg"]["Entries"]
            if "WeaponName" in fmg_name:
                for e in entries:
                    text = e.get("Text")
                    if text and text != "[ERROR]":
                        names[str(e["ID"])] = text
            elif "WeaponCaption" in fmg_name:
                for e in entries:
                    text = e.get("Text")
                    if text and text != "[ERROR]":
                        captions[str(e["ID"])] = text
    return names, captions


def parse_scaling(val):
    """Convert raw correctStrength etc. value to a grade letter."""
    try:
        v = int(float(val))
    except (ValueError, TypeError):
        return "-"
    if v <= 0:
        return "-"
    if v < 25:
        return "E"
    if v < 50:
        return "D"
    if v < 75:
        return "C"
    if v < 100:
        return "B"
    if v < 140:
        return "A"
    return "S"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    names, captions = load_fmg(FMG_FILES)

    weapons = []
    with open(PARAM_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        name = row.get("Name", "").strip()
        if not name:
            continue
        # Only base weapons (they reference themselves in originEquipWep)
        if row.get("originEquipWep") != row.get("ID"):
            continue

        wid = row["ID"].strip()

        # Prefer FMG name if available, fall back to param name
        display_name = names.get(wid, name) or name
        description  = captions.get(wid, "")

        wep_type = WEP_TYPE.get(row.get("wepType", ""), "Unknown")

        # Attack
        attack = {
            "physical":  int(float(row.get("attackBasePhysics",  0) or 0)),
            "magic":     int(float(row.get("attackBaseMagic",    0) or 0)),
            "fire":      int(float(row.get("attackBaseFire",     0) or 0)),
            "lightning": int(float(row.get("attackBaseThunder",  0) or 0)),
            "holy":      int(float(row.get("attackBaseDark",     0) or 0)),
            "critical":  int(float(row.get("attackBaseParry",    100) or 100)),
        }

        # Scaling — use raw percentage values mapped to grades
        scaling = {
            "str": parse_scaling(row.get("correctStrength", 0)),
            "dex": parse_scaling(row.get("correctAgility",  0)),
            "int": parse_scaling(row.get("correctMagic",    0)),
            "fai": parse_scaling(row.get("correctFaith",    0)),
            "arc": parse_scaling(row.get("correctLuck",     0)),
        }

        # Requirements
        req = {
            "str": int(float(row.get("properStrength", 0) or 0)),
            "dex": int(float(row.get("properAgility",  0) or 0)),
            "int": int(float(row.get("properMagic",    0) or 0)),
            "fai": int(float(row.get("properFaith",    0) or 0)),
            "arc": int(float(row.get("properLuck",     0) or 0)),
        }

        weight = float(row.get("weight", 0) or 0)

        weapons.append({
            "id":          int(wid),
            "name":        display_name,
            "description": description,
            "category":    wep_type,
            "weight":      weight,
            "attack":      attack,
            "scaling":     scaling,
            "requirements": req,
        })

    weapons.sort(key=lambda w: (w["category"], w["name"]))

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(weapons, f, indent=2, ensure_ascii=False)

    print(f"Written {len(weapons)} weapons to {OUT_FILE}")

    # Summary by category
    from collections import Counter
    cats = Counter(w["category"] for w in weapons)
    for cat, count in sorted(cats.items()):
        print(f"  {count:3d}  {cat}")


if __name__ == "__main__":
    main()
