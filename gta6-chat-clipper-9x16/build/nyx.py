"""Nyx, the AI.NXTLVL mascot (shared by build/generate.py and build/generate_vox.py)."""
NIGHT, DEEP, VIOLET, STAR, LAV, PINK, CYAN, ORANGE = "#07050f", "#10022c", "#7f1bf8", "#7a2ffb", "#b687f9", "#ff4fa3", "#3ef0ff", "#ffb36b"


def star_svg(color=STAR, glow=True):
    f = 'filter="url(#sg)"' if glow else ""
    return f'<path {f} d="M12 0c.8 6.6 4.8 10.8 12 12-7.2 1.2-11.2 5.4-12 12-.8-6.6-4.8-10.8-12-12 7.2-1.2 11.2-5.4 12-12z" fill="{color}"/>'


def nyx(nid):
    """Nyx (viewBox 300x360): ids n_e_n (normal eyes), n_e_w (wide), n_e_h (happy), n_e_s (star eyes), n_e_z (sleepy),
    n_shades, n_armR (right arm, pivot 238 248), n_star (antenna star)"""
    return f"""<svg class="nyx" id="{nid}" viewBox="0 0 300 360">
<defs><filter id="sg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="hd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1680"/><stop offset="1" stop-color="#1c0846"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e0f6a"/><stop offset="1" stop-color="#170638"/></linearGradient></defs>
<ellipse cx="150" cy="346" rx="96" ry="10" fill="rgba(0,0,0,.35)"/>
<rect x="146" y="20" width="8" height="42" rx="4" fill="{LAV}"/>
<g class="n_star" transform="translate(132 0) scale(1.5)">{star_svg()}</g>
<g class="n_armL"><rect x="44" y="236" width="34" height="78" rx="17" fill="url(#bd)" stroke="{LAV}" stroke-width="3"/></g>
<g class="n_armR"><rect x="222" y="236" width="34" height="78" rx="17" fill="url(#bd)" stroke="{LAV}" stroke-width="3"/></g>
<rect x="84" y="222" width="132" height="112" rx="34" fill="url(#bd)" stroke="{LAV}" stroke-width="3.5"/>
<g transform="translate(138 262) scale(1)">{star_svg(PINK)}</g>
<rect x="34" y="58" width="232" height="170" rx="46" fill="url(#hd)" stroke="{LAV}" stroke-width="4"/>
<rect x="56" y="80" width="188" height="124" rx="32" fill="{NIGHT}"/>
<rect x="64" y="86" width="90" height="16" rx="8" fill="rgba(255,255,255,.08)"/>
<g class="n_e_n" fill="{CYAN}" filter="url(#sg)"><rect x="98" y="118" width="26" height="40" rx="12"/><rect x="176" y="118" width="26" height="40" rx="12"/></g>
<g class="n_e_w" fill="{CYAN}" filter="url(#sg)" opacity="0"><circle cx="111" cy="138" r="24" fill="none" stroke="{CYAN}" stroke-width="9"/><circle cx="189" cy="138" r="24" fill="none" stroke="{CYAN}" stroke-width="9"/><circle cx="111" cy="138" r="7"/><circle cx="189" cy="138" r="7"/></g>
<g class="n_e_h" opacity="0" fill="none" stroke="{CYAN}" stroke-width="10" stroke-linecap="round" filter="url(#sg)"><path d="M92 148 Q111 118 130 148"/><path d="M170 148 Q189 118 208 148"/></g>
<g class="n_e_s" opacity="0"><g transform="translate(93 120) scale(1.5)">{star_svg(PINK)}</g><g transform="translate(171 120) scale(1.5)">{star_svg(PINK)}</g></g>
<g class="n_e_z" opacity="0" stroke="{CYAN}" stroke-width="9" stroke-linecap="round" filter="url(#sg)"><path d="M94 142 h34"/><path d="M172 142 h34"/></g>
<path class="n_m" d="M136 176 Q150 186 164 176" stroke="{LAV}" stroke-width="6" fill="none" stroke-linecap="round"/>
<g class="n_shades" opacity="0"><rect x="70" y="112" width="70" height="44" rx="14" fill="{NIGHT}" stroke="{PINK}" stroke-width="5"/><rect x="160" y="112" width="70" height="44" rx="14" fill="{NIGHT}" stroke="{PINK}" stroke-width="5"/><path d="M140 130 h20" stroke="{PINK}" stroke-width="5"/></g>
</svg>"""


EYES = ["n_e_n", "n_e_w", "n_e_h", "n_e_s", "n_e_z"]


