"""
Generate one HTML page per weapon from weapons.json.
Run: python tools/generate_weapon_pages.py
Output: elden-ring/items/weapons/weapon-<slug>.html
"""

import json
import os
import re
import unicodedata

WEAPONS_JSON = os.path.join(os.path.dirname(__file__), "..", "elden-ring", "items", "weapons", "data", "weapons.json")
OUT_DIR      = os.path.join(os.path.dirname(__file__), "..", "elden-ring", "items", "weapons")


def slugify(name):
    s = re.sub(r"[‘‘’`]", "", name)   # strip apostrophes before normalization
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def stat_row(label, val, zero="-"):
    display = str(int(val)) if val else zero
    return f'<tr><td>{label}</td><td class="stat-value">{display}</td></tr>'


def scaling_cell(grade):
    if not grade or grade == "-":
        return '<td class="stat-value muted">—</td>'
    color = {"S": "gold-light", "A": "gold-light", "B": "gold", "C": "text-secondary", "D": "text-muted", "E": "text-muted"}.get(grade, "text-muted")
    return f'<td class="stat-value" style="color:var(--{color})">{grade}</td>'


def generate(w):
    slug     = slugify(w["name"])
    filename = f"weapon-{slug}.html"

    atk = w["attack"]
    scl = w["scaling"]
    req = w["requirements"]

    # Only show attack types with non-zero values
    atk_rows = ""
    for label, key in [("Physical","physical"),("Magic","magic"),("Fire","fire"),("Lightning","lightning"),("Holy","holy"),("Critical","critical")]:
        v = atk.get(key, 0)
        if v:
            atk_rows += f'<tr><td>{label}</td><td class="stat-value">{v}</td></tr>\n'

    # Only show scaling with non-dash values
    scl_headers = []
    scl_cells   = []
    for label, key in [("STR","str"),("DEX","dex"),("INT","int"),("FAI","fai"),("ARC","arc")]:
        grade = scl.get(key, "-")
        if grade and grade != "-":
            scl_headers.append(f"<th>{label}</th>")
            scl_cells.append(scaling_cell(grade))
    scl_header_html = "".join(scl_headers)
    scl_cell_html   = "".join(scl_cells)

    # Requirements: only non-zero
    req_rows = ""
    for label, key in [("STR","str"),("DEX","dex"),("INT","int"),("FAI","fai"),("ARC","arc")]:
        v = req.get(key, 0)
        if v:
            req_rows += f'<tr><td>{label}</td><td class="stat-value">{v}</td></tr>\n'
    if not req_rows:
        req_rows = '<tr><td colspan="2" class="muted">No requirements</td></tr>'

    image_html = ""

    dlc_badge = ""

    desc_html = ""
    if w.get("description"):
        desc_html = f'<div class="lore-box">"{w["description"]}"</div>'

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": f"{w['name']} — Stats, Scaling & Requirements",
        "description": w.get("description") or f"{w['name']} is a {w['category']} in Elden Ring.",
        "mainEntity": {
            "@type": "GameItem",
            "name": w["name"],
            "category": w["category"],
        }
    }, indent=2)

    return filename, f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{w["name"]} stats, scaling, and requirements in Elden Ring.">
    <title>{w["name"]} — Git Gudder Elden Ring</title>

    <script type="application/ld+json">{schema}</script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
    <style>
        .weapon-wrap {{ max-width: 900px; margin: 0 auto; padding: 0 24px 80px; }}
        .weapon-header {{ display: flex; gap: 32px; align-items: flex-start; margin-bottom: 32px; flex-wrap: wrap; }}
        .weapon-img-wrap {{ flex-shrink: 0; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 20px; display: flex; align-items: center; justify-content: center; width: 160px; height: 160px; }}
        .weapon-img {{ max-width: 120px; max-height: 120px; object-fit: contain; image-rendering: pixelated; }}
        .weapon-header-text {{ flex: 1; min-width: 200px; }}
        .weapon-category-label {{ font-family: 'Fira Code', monospace; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold); margin-bottom: 6px; }}
        .weapon-title {{ font-family: 'Cinzel', serif; font-size: 36px; font-weight: 700; color: var(--text-primary); line-height: 1.1; margin-bottom: 10px; }}
        .weapon-meta {{ font-family: 'Fira Code', monospace; font-size: 12px; color: var(--text-muted); display: flex; gap: 20px; flex-wrap: wrap; margin-top: 8px; }}
        .dlc-badge {{ font-family: 'Fira Code', monospace; font-size: 10px; background: rgba(201,168,76,0.12); border: 1px solid var(--gold-dim); color: var(--gold); border-radius: 3px; padding: 2px 7px; vertical-align: middle; }}
        .lore-box {{ background: var(--bg-mid); border-left: 2px solid var(--gold-dim); padding: 16px 20px; margin: 24px 0; font-style: italic; color: var(--text-secondary); border-radius: 0 var(--radius) var(--radius) 0; }}
        .stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px; }}
        @media (max-width: 600px) {{ .stat-grid {{ grid-template-columns: 1fr; }} }}
        .stat-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; }}
        .stat-card-title {{ font-family: 'Cinzel', serif; font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); background: var(--bg-surface); padding: 10px 16px; border-bottom: 1px solid var(--border); }}
        .stat-card table {{ width: 100%; border-collapse: collapse; }}
        .stat-card td {{ padding: 9px 16px; border-bottom: 1px solid rgba(201,168,76,0.05); font-size: 15px; }}
        .stat-card td:first-child {{ color: var(--text-secondary); }}
        .stat-value {{ font-family: 'Fira Code', monospace; color: var(--text-primary); text-align: right; }}
        .muted {{ color: var(--text-muted); font-style: italic; font-size: 13px; }}
        .scl-table {{ width: 100%; border-collapse: collapse; }}
        .scl-table th {{ font-family: 'Fira Code', monospace; font-size: 11px; color: var(--text-muted); padding: 8px 16px; text-align: center; background: var(--bg-surface); border-bottom: 1px solid var(--border); }}
        .scl-table td {{ padding: 10px 16px; text-align: center; font-family: 'Fira Code', monospace; font-size: 16px; font-weight: 500; }}
    </style>
</head>
<body>
    <header class="site-header" id="global-header"></header>

    <main class="content-section">
        <nav class="subpage-nav-container" data-er-nav="weapons"></nav>

        <div class="weapon-wrap">
            <div class="weapon-header">
                {image_html}
                <div class="weapon-header-text">
                    <div class="weapon-category-label">{w["category"]}{dlc_badge}</div>
                    <h1 class="weapon-title">{w["name"]}</h1>
                    <div class="weapon-meta">
                        <span>Weight: {w["weight"]}</span>
                    </div>
                </div>
            </div>

            {desc_html}

            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-card-title">Attack Power</div>
                    <table><tbody>
                        {atk_rows}
                    </tbody></table>
                </div>
                <div class="stat-card">
                    <div class="stat-card-title">Requirements</div>
                    <table><tbody>
                        {req_rows}
                    </tbody></table>
                </div>
            </div>

            {"" if not scl_header_html else f"""
            <div class="stat-card" style="margin-bottom:28px;">
                <div class="stat-card-title">Attribute Scaling</div>
                <table class="scl-table">
                    <thead><tr>{scl_header_html}</tr></thead>
                    <tbody><tr>{scl_cell_html}</tr></tbody>
                </table>
            </div>"""}

        </div>
    </main>

    <footer role="contentinfo" id="global-footer"></footer>
    <script src="/site.js"></script>
</body>
</html>
'''


def main():
    with open(WEAPONS_JSON, encoding="utf-8") as f:
        weapons = json.load(f)

    os.makedirs(OUT_DIR, exist_ok=True)
    generated = 0
    for w in weapons:
        filename, html = generate(w)
        path = os.path.join(OUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        generated += 1

    print(f"Generated {generated} weapon pages in {OUT_DIR}")


if __name__ == "__main__":
    main()
