"""
Generate simple general guide pages for the Convergence Mod section.
Run: python tools/generate_conv_guides.py
"""

import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "convergence", "guides")

GUIDES = [
    # (slug, title, video_id, category_label)
    ("starter-guide",             "Convergence Starter Guide",           "qPrkDRs9raU", "Getting Started"),
    ("launcher-installation",     "New Launcher Installation",           "KtYoIphx6lA", "Getting Started"),
    ("teleport-gear",             "Secret Teleport Gear",                "uhHcIubQpQI", "Getting Started"),
    ("trick-weapons",             "New Trick Weapons",                   "YwtRZDecy_I", "Weapons & Upgrades"),
    ("new-swords",                "New Swords",                          "DTOIfXJWdSg", "Weapons & Upgrades"),
    ("blades-claws-daggers",      "New Blades, Claws & Daggers",         "LD5jrsswdkA", "Weapons & Upgrades"),
    ("prime-weapons",             "Prime Weapons",                       "PbSKwsBFeug", "Weapons & Upgrades"),
    ("galvanic-culling-blade",    "Galvanic Culling Blade",              "QdJ9Dgv5Duo", "Weapons & Upgrades"),
    ("get-to-plus-15",            "How to Get Weapons to +15",           "m8uhgiolBZE", "Weapons & Upgrades"),
    ("shadow-stone-bell-bearings","Shadow Stone Bell Bearings",          "lduaxGSpF2k", "Weapons & Upgrades"),
    ("spellblade-set",            "Spellblade Set & Rogier's Quest",     "lrG2BJabr9M", "Walkthroughs & Locations"),
    ("noxumbra-walkthrough",      "Noxumbra Walkthrough",                "GTK78kniN3I", "Walkthroughs & Locations"),
    ("fog-rift-catacombs",        "Fog Rift Catacombs Walkthrough",      "IQjOQk3K6o0", "Walkthroughs & Locations"),
    ("vulgar-militia-stronghold", "Vulgar Militia Stronghold",           "8x44bM8lL0I", "Walkthroughs & Locations"),
    ("daergraf-boss-guide",       "How to Fight Daergraf",              "npkgp7-Qnhs", "Boss Guides"),
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} — Convergence Mod guide on Git Gudder.">
    <title>{title} — Convergence Mod — Git Gudder</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body>

    <header class="site-header" id="global-header"></header>

    <main class="content-section">
        <nav class="subpage-nav-container" data-conv-nav="general"></nav>

        <div class="guide-body">
            <div style="font-family:\'Fira Code\',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--gold);margin-bottom:6px;">Convergence Mod · {category}</div>
            <h1 style="font-family:\'Cinzel\',serif;font-size:36px;font-weight:700;color:var(--text-primary);line-height:1.1;margin-bottom:24px;">{title}</h1>

            <div class="video-wrapper">
                <iframe
                    src="https://www.youtube.com/embed/{video_id}"
                    title="{title} — Git Gudder Convergence Mod"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
                </iframe>
            </div>
        </div>
    </main>

    <footer role="contentinfo" id="global-footer"></footer>
    <script src="/site.js"></script>
</body>
</html>
'''

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for slug, title, video_id, category in GUIDES:
        path = os.path.join(OUT_DIR, f"{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(title=title, video_id=video_id, category=category))
        print(f"  {slug}.html")
    print(f"Generated {len(GUIDES)} guide pages.")

if __name__ == "__main__":
    main()
