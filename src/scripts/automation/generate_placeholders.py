#!/usr/bin/env python3
"""Generate SVG placeholder images for all JG Mart product categories."""

import os
import pathlib

OUTPUT_DIR = pathlib.Path("G:/JGC Mart/JGC Mart - Hermes/06_Web_Catalog/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def svg_tag(w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'


def make_svg(name, grad_stops, paths, text_lines, w=300, h=220):
    """Build a complete SVG string.

    Args:
        name: filename (for reference, not used in output)
        grad_stops: tuple of (angle_or_coords, [(offset, color), ...])
        paths: list of (path_d, fill, opacity)
        text_lines: list of (y, text, font_size, fill, font_weight)
        w, h: dimensions
    """
    g_id = "g"
    stops_xml = "\n      ".join(
        f'<stop offset="{off}" style="stop-color:{col};stop-opacity:1"/>'
        for off, col in grad_stops[1]
    )
    # angle or coord-based gradient
    if isinstance(grad_stops[0], str):
        grad_def = (
            f'<linearGradient id="{g_id}" x1="0%" y1="0%" x2="100%" y2="100%" '
            f'gradientTransform="rotate({grad_stops[0]})">\n      {stops_xml}\n    </linearGradient>'
        )
    else:
        grad_def = (
            f'<linearGradient id="{g_id}" x1="{grad_stops[0][0]}%" y1="{grad_stops[0][1]}%" '
            f'x2="{grad_stops[0][2]}%" y2="{grad_stops[0][3]}%">\n      {stops_xml}\n    </linearGradient>'
        )

    paths_xml = "\n  ".join(
        f'<path d="{d}" fill="{f}" opacity="{o if o != 1 else "1"}"/>'
        for d, f, o in paths
    )
    texts_xml = "\n  ".join(
        f'<text x="150" y="{y}" font-family="Inter,Segoe UI,system-ui,sans-serif" '
        f'font-size="{fs}" fill="{f}" text-anchor="middle"'
        + (f' font-weight="{fw}"' if fw else "")
        + f' dominant-baseline="central">{t}</text>'
        for y, t, fs, f, fw in text_lines
    )

    return (
        f'{svg_tag(w, h)}\n'
        f'  <defs>\n    {grad_def}\n  </defs>\n'
        f'  <rect width="{w}" height="{h}" fill="url(#{g_id})" rx="8"/>\n'
        f'  {paths_xml}\n'
        f'  {texts_xml}\n'
        f'</svg>'
    )


SVGS = {}

# ─── 1. Rice & Dal (warm beige) ───
SVGS["rice_dal"] = make_svg(
    "rice_dal",
    ("30", [("0%", "#F5E6C8"), ("100%", "#D4A853")]),
    [
        # bowl body
        ("M90,130 Q90,180 150,180 Q210,180 210,130 Z", "#FFF8E7", 0.9),
        # bowl rim
        ("M82,130 Q150,145 218,130 Q218,125 150,138 Q82,125 82,130", "#E8C36A", 0.7),
        # rice grains
        ("M105,125 Q110,105 120,110 Q130,100 140,110 Q150,95 160,108 Q170,100 180,112 Q190,102 195,115", "#FFF", 0.8),
        ("M110,118 Q118,108 128,115 Q138,105 148,114 Q158,102 168,112 Q178,104 188,115", "#FFF", 0.5),
        # steam
        ("M130,105 Q135,90 145,95 Q140,80 150,85", "#FFF", 0.25),
        ("M160,105 Q165,88 175,93 Q170,78 180,83", "#FFF", 0.2),
    ],
    [
        (195, "Rice & Dal", 16, "#5C3D1A", "700"),
        (210, "চাউল ও ডাল", 11, "#8B6914", "500"),
    ],
)

# ─── 2. Oil & Spices (warm golden) ───
SVGS["oil_spices"] = make_svg(
    "oil_spices",
    ("45", [("0%", "#FDBB2D"), ("100%", "#E07A1B")]),
    [
        # oil bottle body
        ("M100,90 L100,180 L195,180 L195,90 Z", "#FFF8DC", 0.85),
        # bottle neck
        ("M120,90 L120,65 L175,65 L175,90 Z", "#FFF8DC", 0.85),
        # bottle cap
        ("M125,60 L125,50 L170,50 L170,60 Z", "#B8520A", 0.8),
        # label on bottle
        ("M115,110 L115,160 L180,160 L180,110 Z", "#D4691E", 0.3),
        # oil drop
        ("M140,100 C140,108 145,110 148,110 C151,110 155,108 155,100 C155,95 148,85 148,85 C148,85 140,95 140,100", "#FDBB2D", 0.7),
        # spice dots
        ("M80,150 C82,148 78,145 80,143", "#B22222", 0.7),
        ("M82,160 C84,158 80,155 82,153", "#B22222", 0.6),
        ("M84,170 C86,168 82,165 84,163", "#B22222", 0.5),
        ("M215,145 C217,143 213,140 215,138", "#228B22", 0.6),
        ("M213,155 C215,153 211,150 213,148", "#228B22", 0.7),
        ("M217,165 C219,163 215,160 217,158", "#228B22", 0.5),
    ],
    [
        (195, "Oil & Spices", 15, "#5C2D0A", "700"),
        (210, "তেল ও মশলা", 11, "#7A4010", "500"),
    ],
)

# ─── 3. Vegetables (green tones) ───
SVGS["vegetables"] = make_svg(
    "vegetables",
    ("30", [("0%", "#81C784"), ("100%", "#2E7D32")]),
    [
        # broccoli/cauliflower top
        ("M120,120 Q110,90 120,80 Q115,60 130,65 Q140,45 155,60 Q170,45 180,65 Q195,60 190,80 Q200,90 190,120 Z", "#4CAF50", 0.85),
        # stem
        ("M140,120 L140,170 L170,170 L170,120 Z", "#66BB6A", 0.7),
        # carrot body
        ("M60,180 L80,110 L100,180 Z", "#FF8A65", 0.8),
        # carrot leaves
        ("M80,110 Q75,95 70,100", "#4CAF50", 0.7),
        ("M80,110 Q80,92 85,98", "#4CAF50", 0.7),
        ("M80,110 Q88,95 92,102", "#4CAF50", 0.7),
        # tomato
        ("M210,160 A20,18 0 1,1 210,196 A20,18 0 1,1 210,160", "#EF5350", 0.85),
        # tomato stem
        ("M210,160 Q208,153 210,150", "#4CAF50", 0.7),
        # small dots/details
        ("M120,95 Q130,85 140,95", "#388E3C", 0.3),
    ],
    [
        (195, "Vegetables", 15, "#F1F8E9", "700"),
        (210, "সবজি", 11, "#DCEDC8", "500"),
    ],
)

# ─── 4. Fish (blue tones) ───
SVGS["fish"] = make_svg(
    "fish",
    ("30", [("0%", "#64B5F6"), ("100%", "#1565C0")]),
    [
        # fish body
        ("M90,130 Q90,80 150,100 Q210,80 210,130 Q210,170 150,150 Q90,170 90,130 Z", "#90CAF9", 0.9),
        # tail
        ("M210,100 L240,75 L240,180 L210,155 Z", "#64B5F6", 0.85),
        # eye
        ("M115,115 A8,8 0 1,1 115,131 A8,8 0 1,1 115,115", "#FFF", 0.9),
        # pupil
        ("M118,120 A4,4 0 1,1 118,128 A4,4 0 1,1 118,120", "#0D47A1", 0.9),
        # scales pattern
        ("M140,115 Q145,105 150,115 Q145,125 140,115", "rgba(255,255,255,0.3)", 1),
        ("M155,110 Q160,100 165,110 Q160,120 155,110", "rgba(255,255,255,0.3)", 1),
        ("M130,130 Q135,120 140,130 Q135,140 130,130", "rgba(255,255,255,0.3)", 1),
        ("M150,125 Q155,115 160,125 Q155,135 150,125", "rgba(255,255,255,0.3)", 1),
        # mouth
        ("M92,128 L100,128", "#1565C0", 0.5),
        # fin
        ("M140,95 L145,75 L155,80 L155,95", "rgba(255,255,255,0.2)", 1),
        ("M150,150 L155,175 L165,170 L165,150", "rgba(255,255,255,0.2)", 1),
    ],
    [
        (195, "Fish", 16, "#E3F2FD", "700"),
        (210, "মাছ", 11, "#BBDEFB", "500"),
    ],
)

# ─── 5. Meat (red-brown tones) ───
SVGS["meat"] = make_svg(
    "meat",
    ("30", [("0%", "#E57373"), ("100%", "#8D2E2E")]),
    [
        # drumstick/meat cut shape
        ("M130,180 Q100,180 90,160 Q80,140 85,120 Q90,105 100,105 Q110,105 115,115 Q120,100 135,95 Q150,90 160,95 Q170,100 175,115 Q180,110 190,115 Q200,120 200,140 Q200,160 180,175 Q165,185 150,180 Z", "#EF9A9A", 0.9),
        # inner detail / muscle lines
        ("M120,130 Q135,120 150,130 Q165,140 175,130", "rgba(139,46,46,0.25)", 1),
        ("M110,145 Q125,135 140,145 Q155,155 170,145", "rgba(139,46,46,0.2)", 1),
        # bone
        ("M95,160 L85,175 L78,170", "#FFCCBC", 0.8),
        # fat marbling dots
        ("M140,110 A3,2 0 1,1 140,114 A3,2 0 1,1 140,110", "#FFCCBC", 0.5),
        ("M160,130 A3,2 0 1,1 160,134 A3,2 0 1,1 160,130", "#FFCCBC", 0.4),
        ("M120,155 A2,2 0 1,1 120,159 A2,2 0 1,1 120,155", "#FFCCBC", 0.5),
    ],
    [
        (195, "Meat", 16, "#FFEBEE", "700"),
        (210, "মাংস", 11, "#F8BBD0", "500"),
    ],
)

# ─── 6. Dairy & Eggs (cream tones) ───
SVGS["dairy_eggs"] = make_svg(
    "dairy_eggs",
    ("30", [("0%", "#FFF3E0"), ("100%", "#FFCC80")]),
    [
        # milk carton body
        ("M100,65 L100,175 L195,175 L195,65 Z", "#FFF", 0.9),
        # milk carton top (gable)
        ("M100,65 L120,40 L175,40 L195,65 Z", "#FFF8E1", 0.85),
        # carton ridge
        ("M147,40 L147,65", "#FFCC80", 0.6),
        # carton label
        ("M110,90 L110,155 L185,155 L185,90 Z", "#FFF3E0", 0.5),
        # carton text area
        ("M130,105 L130,140 L165,140 L165,105 Z", "#FFB74D", 0.3),
        # egg 1 (left)
        ("M55,140 A22,28 0 1,1 55,196 A22,28 0 1,1 55,140", "#FFFEF5", 0.9),
        # egg 1 highlight
        ("M50,155 A6,8 0 1,1 50,171 A6,8 0 1,1 50,155", "#FFF", 0.5),
        # egg 2 (right)
        ("M240,150 A18,24 0 1,1 240,198 A18,24 0 1,1 240,150", "#FFFEF5", 0.85),
        # egg 2 highlight
        ("M236,162 A4,6 0 1,1 236,174 A4,6 0 1,1 236,162", "#FFF", 0.5),
    ],
    [
        (195, "Dairy & Eggs", 14, "#795548", "700"),
        (210, "দুধ ও ডিম", 11, "#8D6E63", "500"),
    ],
)

# ─── 7. Fruits (bright rainbow) ───
SVGS["fruits"] = make_svg(
    "fruits",
    ("30", [("0%", "#FF8A65"), ("100%", "#E040FB")]),
    [
        # basket/bowl
        ("M70,160 Q70,195 150,195 Q230,195 230,160 Z", "#FFF8E1", 0.85),
        # apple (red)
        ("M125,110 A24,22 0 1,1 125,154 A24,22 0 1,1 125,110", "#E53935", 0.85),
        # apple stem
        ("M125,110 Q128,100 132,98", "#795548", 0.7),
        # apple leaf
        ("M132,98 Q140,95 138,102", "#66BB6A", 0.7),
        # orange
        ("M165,120 A20,18 0 1,1 165,156 A20,18 0 1,1 165,120", "#FF9800", 0.85),
        # orange navel
        ("M165,125 A2,2 0 1,1 165,129 A2,2 0 1,1 165,125", "#F57C00", 0.5),
        # banana arc
        ("M80,150 Q75,130 90,115 Q100,100 115,105 Q110,115 100,130 Q90,145 85,155 Z", "#FFF176", 0.85),
        # grapes (bunch)
        ("M175,100 A10,9 0 1,1 175,118 A10,9 0 1,1 175,100", "#7B1FA2", 0.8),
        ("M190,108 A9,8 0 1,1 190,124 A9,8 0 1,1 190,108", "#8E24AA", 0.75),
        ("M185,95 A8,7 0 1,1 185,109 A8,7 0 1,1 185,95", "#9C27B0", 0.75),
        ("M180,112 A8,7 0 1,1 180,126 A8,7 0 1,1 180,112", "#AB47BC", 0.7),
    ],
    [
        (195, "Fruits", 16, "#FCE4EC", "700"),
        (210, "ফল", 11, "#F8BBD0", "500"),
    ],
)

# ─── 8. FMCG (teal tones) ───
SVGS["fmcg"] = make_svg(
    "fmcg",
    ("30", [("0%", "#80CBC4"), ("100%", "#00695C")]),
    [
        # bottle / spray body
        ("M115,70 L115,175 L180,175 L180,70 Z", "#B2DFDB", 0.85),
        # bottle neck
        ("M130,70 L130,50 L165,50 L165,70 Z", "#B2DFDB", 0.8),
        # pump/spray nozzle
        ("M140,50 L140,35 L155,35 L155,50 Z", "#4DB6AC", 0.8),
        # spray button
        ("M143,35 L143,28 L152,28 L152,35 Z", "#26A69A", 0.8),
        # spray mist
        ("M145,28 Q140,20 135,22 Q130,18 125,24 Q120,20 118,28", "rgba(255,255,255,0.3)", 1),
        ("M150,28 Q155,18 160,22 Q165,16 170,24 Q175,18 178,26", "rgba(255,255,255,0.25)", 1),
        # label stripe
        ("M115,100 L115,150 L180,150 L180,100 Z", "#009688", 0.3),
        # small dot details on label
        ("M130,110 A4,4 0 1,1 130,118 A4,4 0 1,1 130,110", "#FFF", 0.4),
        ("M145,110 A4,4 0 1,1 145,118 A4,4 0 1,1 145,110", "#FFF", 0.4),
        ("M160,110 A4,4 0 1,1 160,118 A4,4 0 1,1 160,110", "#FFF", 0.4),
        ("M130,125 A4,4 0 1,1 130,133 A4,4 0 1,1 130,125", "#FFF", 0.4),
        ("M145,125 A4,4 0 1,1 145,133 A4,4 0 1,1 145,125", "#FFF", 0.4),
        ("M160,125 A4,4 0 1,1 160,133 A4,4 0 1,1 160,125", "#FFF", 0.4),
    ],
    [
        (195, "FMCG", 16, "#E0F2F1", "700"),
        (210, "প্রয়োজনীয়", 11, "#B2DFDB", "500"),
    ],
)

# ─── 9. Beverages (cool blue tones) ───
SVGS["beverages"] = make_svg(
    "beverages",
    ("30", [("0%", "#4FC3F7"), ("100%", "#0277BD")]),
    [
        # bottle left (soda/can shape)
        ("M70,90 L70,175 L120,175 L120,90 Z", "#B3E5FC", 0.85),
        # can top
        ("M72,90 L72,80 L118,80 L118,90 Z", "#81D4FA", 0.85),
        # can pull tab
        ("M90,85 L95,75 L100,85 Z", "#4FC3F7", 0.7),
        # can label
        ("M70,105 L70,155 L120,155 L120,105 Z", "#29B6F6", 0.3),
        # bottle right (glass bottle shape)
        ("M160,70 L180,50 L210,50 L230,70 L230,175 L160,175 Z", "#E1F5FE", 0.85),
        # bottle neck
        ("M175,70 L180,55 L210,55 L215,70 Z", "#E1F5FE", 0.8),
        # bottle label
        ("M165,95 L165,150 L225,150 L225,95 Z", "#0288D1", 0.3),
        # bottle liquid level
        ("M160,130 L160,175 L230,175 L230,130 Z", "rgba(3,169,244,0.25)", 1),
        # bubbles in bottle
        ("M180,145 A3,3 0 1,1 180,151 A3,3 0 1,1 180,145", "rgba(255,255,255,0.4)", 1),
        ("M195,140 A2,2 0 1,1 195,144 A2,2 0 1,1 195,140", "rgba(255,255,255,0.35)", 1),
        ("M210,148 A3,3 0 1,1 210,154 A3,3 0 1,1 210,148", "rgba(255,255,255,0.3)", 1),
        ("M190,155 A2,2 0 1,1 190,159 A2,2 0 1,1 190,155", "rgba(255,255,255,0.35)", 1),
    ],
    [
        (195, "Beverages", 15, "#E1F5FE", "700"),
        (210, "পানীয়", 11, "#B3E5FC", "500"),
    ],
)

# ─── 10. Snacks (orange tones) ───
SVGS["snacks"] = make_svg(
    "snacks",
    ("30", [("0%", "#FFB74D"), ("100%", "#E65100")]),
    [
        # snack package / bag
        ("M90,60 L90,185 L200,185 L200,60 Z", "#FFF3E0", 0.85),
        # package top seal
        ("M90,60 L200,60 L190,50 L100,50 Z", "#FFCC80", 0.85),
        # package zigzag bottom
        ("M90,185 Q100,175 110,185 Q120,175 130,185 Q140,175 150,185 Q160,175 170,185 Q180,175 190,185 Q195,175 200,185", "#FFCC80", 0.85),
        # label area
        ("M100,85 L100,155 L190,155 L190,85 Z", "#FF9800", 0.3),
        # cracker/snack pieces
        ("M120,105 L130,95 L140,105 L130,115 Z", "#FFE082", 0.8),
        ("M150,110 L160,100 L170,110 L160,120 Z", "#FFE082", 0.75),
        ("M135,125 L145,115 L155,125 L145,135 Z", "#FFE082", 0.7),
        # star/crunch detail
        ("M115,130 L118,124 L121,130 L118,136 Z", "#FFE082", 0.5),
        ("M168,105 L171,99 L174,105 L171,111 Z", "#FFE082", 0.5),
        # chip/crisp
        ("M178,130 A8,6 0 1,1 178,142 A8,6 0 1,1 178,130", "#FFCC80", 0.6),
    ],
    [
        (195, "Snacks", 16, "#3E1A00", "700"),
        (210, "স্ন্যাকস", 11, "#5D2E00", "500"),
    ],
)


# ─── Fallback placeholder (green circle with ?) ───
SVGS["placeholder"] = make_svg(
    "placeholder",
    ("30", [("0%", "#4CAF50"), ("100%", "#2E7D32")]),
    [
        # circle background
        ("M150,70 A40,40 0 1,1 150,150 A40,40 0 1,1 150,70", "rgba(255,255,255,0.15)", 1),
    ],
    [
        (110, "?", 40, "#FFF", "700"),
        (175, "Placeholder", 14, "rgba(255,255,255,0.8)", "600"),
    ],
)


def main():
    written = []
    for cat_id, svg_content in SVGS.items():
        # skip placeholder - handled separately below
        if cat_id == "placeholder":
            continue
        # sanitize filename
        safe_name = cat_id.replace(" ", "_")
        filepath = OUTPUT_DIR / f"{safe_name}.svg"
        filepath.write_text(svg_content, encoding="utf-8")
        size_kb = len(svg_content.encode("utf-8")) / 1024
        written.append((filepath.name, size_kb))

    # also write placeholder.svg (fallback image)
    placeholder = OUTPUT_DIR / "placeholder.svg"
    placeholder.write_text(SVGS.get("placeholder", ""), encoding="utf-8")
    written.append(("placeholder.svg", len(SVGS.get("placeholder", "").encode("utf-8")) / 1024))

    print(f"✅ Generated {len(written)} SVG placeholders in {OUTPUT_DIR}")
    print()
    for name, kb in written:
        print(f"   {name:25s}  {kb:.1f} KB")
    print()
    print("All category placeholders are ready for instant loading.")


if __name__ == "__main__":
    main()
