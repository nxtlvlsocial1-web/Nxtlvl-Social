"""Builds build/style.css: style_base.css (shared reel styles) + style_4c.css (this reel), Inter swapped for Poppins (from the
mrgraphiz pack, OFL), then the Cree rig styles. python3 build/style_build.py"""
import os, re
D = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(D, "style_base.css")).read() + open(os.path.join(D, "style_4c.css")).read()
css = re.sub(r"(\d+px(?:/[\d.]+)?) Inter\b", r"\1 Poppins", css.replace("font-family: Inter", "font-family: Poppins"))
css += open(os.path.join(D, "style_cree.css")).read().replace("height: 820px; z-index: 6;", "height: 820px; z-index: 33;")
open(os.path.join(D, "style.css"), "w").write(css)
