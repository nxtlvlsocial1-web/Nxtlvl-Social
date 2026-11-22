"""Chibi mascot audience for "The Empty Theater": every character assembled from parts so no two look alike.

Owner's notes on the final (2026-11-20): a chibi mascot audience; then "they all have the same appearance, make sure everyone
has a different hairstyle and facial features, they all have similar heads". Each chibi is one small inline SVG built from
shared <symbol>s, so a hundred-odd characters stay light:
  * 14 hairstyles, each drawn from behind (seated) and from the front (turned round, or walking): short, bun, pigtails,
    ponytail, spiky, afro, long, cap, beanie, mohawk, bob with bangs, headphones, bow, curly;
  * 5 head shapes (a per-character scale on the head group);
  * faces: 5 happy eye types x 5 mouths, glasses or freckles on some, 3 sad eye types for the walkers;
  * colours per character through CSS variables: --hair, --skin, --shirt, --acc (caps, beanies, bows, headphones).
Hairstyles are dealt from shuffled decks, so neighbours rarely share one.
"""
import random

R = random.Random(20261120)
HAIR = ("#3b2219", "#6b3b2a", "#1d1d2b", "#c47a3a", "#e8b04a", "#8a4bd6", "#ff6fae", "#4aa3df", "#2b2b3d", "#d9d2c5", "#b23a2e", "#3fae8c")
SKIN = ("#ffe0cc", "#f6c7a8", "#e0a37f", "#b9785a", "#8a553c", "#ffd3b8")
SHIRT = ("#ff6fae", "#4aa3df", "#ffd27a", "#7ed6a5", "#b48cff", "#ff8a5c", "#f2f2f2", "#5fd0d6", "#2f3a56", "#ffb3d1")
ACC = ("#e53950", "#2f6fe0", "#ffd23f", "#17a673", "#f5f5f5", "#7a3cf0", "#ff7a00", "#111827")
SHAPES = ((1, 1), (1.09, .93), (.93, 1.07), (1.06, 1.03), (.96, .95))
HC = "50 48"                                   # head centre in the 100 x 120 frame
INK = "#2a1220"

H = lambda d: f'<path d="{d}" style="fill:var(--hair)"/>'
A = lambda d: f'<path d="{d}" style="fill:var(--acc)"/>'
SHADE = lambda d: f'<path d="{d}" fill="#000" opacity=".18"/>'
FRINGE = H("M11 50 C9 18 30 4 50 4 C70 4 91 18 89 50 C84 38 76 31 66 30 C60 36 50 38 40 34 C30 32 18 38 11 50 Z")
GLOSS = '<ellipse cx="34" cy="26" rx="13" ry="7" fill="#fff" opacity=".22" transform="rotate(-25 34 26)"/>'
BOW = A("M62 10 L82 0 L82 22 Z") + A("M62 10 L44 0 L44 22 Z") + '<circle cx="62" cy="10" r="5" style="fill:var(--acc)"/>'
CURLS = "".join(f'<circle cx="{x}" cy="{y}" r="11" style="fill:var(--hair)"/>' for x, y in ((18, 30), (28, 16), (42, 8), (58, 8), (72, 16), (82, 30)))
AFRO = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--hair)"/>' for x, y, r in
               ((50, 4, 17), (26, 10, 17), (74, 10, 17), (8, 32, 17), (92, 32, 17), (4, 58, 15), (96, 58, 15), (50, 46, 45)))
PHONES_BAND = ('<path d="M10 46 C10 2 90 2 90 46" style="stroke:var(--acc)" stroke-width="7" fill="none"/>'
               '<rect x="1" y="40" width="15" height="28" rx="7" style="fill:var(--acc)"/><rect x="84" y="40" width="15" height="28" rx="7" style="fill:var(--acc)"/>')

# hairstyles: (from behind, front: drawn behind the face, front: drawn over the face)
STYLES = {
    "short": (f'{H("M50 9 C45 -2 59 -5 57 5")}', "", FRINGE),
    "bun": ('<circle cx="50" cy="8" r="14" style="fill:var(--hair)"/>', '<circle cx="50" cy="5" r="14" style="fill:var(--hair)"/>', FRINGE),
    "pigtails": ('<circle cx="5" cy="62" r="15" style="fill:var(--hair)"/><circle cx="95" cy="62" r="15" style="fill:var(--hair)"/>'
                 '<circle cx="15" cy="55" r="4.5" style="fill:var(--acc)"/><circle cx="85" cy="55" r="4.5" style="fill:var(--acc)"/>',
                 '<circle cx="3" cy="64" r="15" style="fill:var(--hair)"/><circle cx="97" cy="64" r="15" style="fill:var(--hair)"/>'
                 '<circle cx="13" cy="57" r="4.5" style="fill:var(--acc)"/><circle cx="87" cy="57" r="4.5" style="fill:var(--acc)"/>',
                 H("M11 50 C9 16 30 6 50 6 C70 6 91 16 89 50 C84 32 66 26 50 22 C34 26 16 32 11 50 Z")),
    "ponytail": (H("M42 66 C28 84 42 108 56 112 C64 98 66 80 58 66 Z") + '<rect x="42" y="62" width="16" height="7" rx="3" style="fill:var(--acc)"/>',
                 H("M82 30 C106 40 106 82 92 98 C90 76 88 56 78 40 Z"),
                 H("M11 50 C9 16 30 6 52 6 C74 6 91 18 89 50 C80 30 60 22 30 34 C22 38 16 42 11 50 Z")),
    "spiky": (H("M12 42 L16 12 L30 28 L34 0 L48 22 L56 -4 L64 20 L78 2 L78 28 L94 14 L88 44 Z"), "",
              H("M11 46 L13 16 L26 28 L32 2 L44 22 L52 -2 L60 20 L72 2 L76 26 L89 14 L89 46 C80 32 20 32 11 46 Z")),
    "afro": (AFRO, AFRO, H("M14 40 C20 14 80 14 86 40 C70 30 30 30 14 40 Z")),
    "long": (H("M9 46 C9 8 91 8 91 46 L95 104 C80 112 20 112 5 104 Z"), H("M8 46 C8 8 92 8 92 46 L97 106 C80 112 20 112 3 106 Z"),
             H("M11 52 C10 14 30 6 50 6 C70 6 90 14 89 52 C82 30 60 18 50 16 C40 18 18 30 11 52 Z")),
    "cap": (A("M10 46 C10 4 90 4 90 46 C70 40 30 40 10 46 Z") + '<rect x="40" y="36" width="20" height="7" rx="3" style="fill:var(--hair)"/><circle cx="50" cy="8" r="4" style="fill:var(--acc)"/>',
            "", A("M10 42 C10 2 90 2 90 42 Z") + '<ellipse cx="50" cy="42" rx="47" ry="8" style="fill:var(--acc)"/>'
            + '<ellipse cx="50" cy="42" rx="47" ry="8" fill="#000" opacity=".2"/><circle cx="50" cy="24" r="6" fill="#fff" opacity=".85"/>'),
    "beanie": (A("M9 48 C9 2 91 2 91 48 Z") + '<rect x="8" y="38" width="84" height="13" rx="6" fill="#000" opacity=".15"/>'
               '<circle cx="50" cy="2" r="11" fill="#fff"/>', "",
               A("M8 44 C8 0 92 0 92 44 Z") + '<rect x="7" y="33" width="86" height="14" rx="7" style="fill:var(--acc)"/>'
               '<rect x="7" y="33" width="86" height="14" rx="7" fill="#000" opacity=".15"/><circle cx="50" cy="0" r="11" fill="#fff"/>'),
    "mohawk": (H("M42 14 L38 -12 L50 -4 L56 -18 L62 -6 L62 14 Z"), "", H("M42 16 L38 -10 L50 -2 L56 -16 L62 -4 L62 16 C56 12 48 12 42 16 Z")),
    "bob": (H("M7 50 C7 4 93 4 93 50 L95 82 C80 90 20 90 5 82 Z"), H("M7 50 C7 6 93 6 93 50 L95 84 C80 92 20 92 5 84 Z"),
            H("M12 44 C12 6 88 6 88 44 Z")),
    "headphones": (PHONES_BAND, "", FRINGE + PHONES_BAND),
    "bow": (BOW, "", FRINGE + BOW),
    "curly": (CURLS, "", CURLS + H("M12 44 C16 20 84 20 88 44 C70 34 30 34 12 44 Z")),
}
NO_EARS = {"long", "bob", "headphones", "afro"}

# faces (front view)
EYES = {
    "arcs": f'<path d="M28 56 Q35 47 42 56" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M58 56 Q65 47 72 56" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
    "round": f'<circle cx="36" cy="55" r="6.5" fill="{INK}"/><circle cx="64" cy="55" r="6.5" fill="{INK}"/>'
             '<circle cx="38.5" cy="52.5" r="2.4" fill="#fff"/><circle cx="66.5" cy="52.5" r="2.4" fill="#fff"/>',
    "wink": f'<path d="M28 56 Q35 47 42 56" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            f'<circle cx="64" cy="55" r="6" fill="{INK}"/><circle cx="66" cy="53" r="2.2" fill="#fff"/>',
    "dots": f'<circle cx="37" cy="56" r="4" fill="{INK}"/><circle cx="63" cy="56" r="4" fill="{INK}"/>',
    "squint": f'<path d="M30 50 L41 56 L30 62" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<path d="M70 50 L59 56 L70 62" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
}
MOUTHS = {
    "open": '<path d="M41 66 Q50 80 59 66 Z" fill="#9a3b4e"/>',
    "grin": '<path d="M37 65 Q50 85 63 65 Z" fill="#9a3b4e"/><path d="M39 66 L61 66 L60 70.5 L40 70.5 Z" fill="#fff"/>',
    "cat": '<path d="M41 67 Q45.5 73 50 67 Q54.5 73 59 67" stroke="#9a3b4e" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
    "wow": '<ellipse cx="50" cy="70" rx="5.5" ry="6.5" fill="#9a3b4e"/>',
    "tongue": '<path d="M41 66 Q50 80 59 66 Z" fill="#9a3b4e"/><ellipse cx="50" cy="73.5" rx="5" ry="3.2" fill="#ff8fa3"/>',
}
SAD_EYES = {
    "dots": f'<ellipse cx="36" cy="57" rx="4" ry="5.5" fill="{INK}"/><ellipse cx="64" cy="57" rx="4" ry="5.5" fill="{INK}"/>',
    "teary": f'<circle cx="36" cy="57" r="6.5" fill="{INK}"/><circle cx="64" cy="57" r="6.5" fill="{INK}"/>'
             '<circle cx="38" cy="54.5" r="2.4" fill="#fff"/><circle cx="66" cy="54.5" r="2.4" fill="#fff"/>'
             '<path d="M30 61 Q36 64 42 61" stroke="#8fd3ff" stroke-width="2.5" fill="none"/><path d="M58 61 Q64 64 70 61" stroke="#8fd3ff" stroke-width="2.5" fill="none"/>',
    "down": f'<path d="M29 54 Q35 61 42 54" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M58 54 Q65 61 71 54" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
}
SAD_REST = (f'<path d="M28 49 L42 44" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/><path d="M72 49 L58 44" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
            '<path d="M42 75 Q50 67 58 75" stroke="#9a3b4e" stroke-width="4" fill="none" stroke-linecap="round"/>'
            '<path d="M29 63 Q25 70 29 74 Q33 70 29 63 Z" fill="#8fd3ff"/>')
GLASSES = (f'<circle cx="36" cy="55" r="11" stroke="{INK}" stroke-width="3" fill="#fff" fill-opacity=".15"/>'
           f'<circle cx="64" cy="55" r="11" stroke="{INK}" stroke-width="3" fill="#fff" fill-opacity=".15"/><path d="M47 54 Q50 51 53 54" stroke="{INK}" stroke-width="3" fill="none"/>')
FRECKLES = "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#a0583c" opacity=".7"/>' for x, y in ((24, 64), (28, 61), (30, 66), (76, 64), (72, 61), (70, 66)))
BLUSH = '<ellipse cx="26" cy="66" rx="7" ry="4" fill="#ff7fa8" opacity=".55"/><ellipse cx="74" cy="66" rx="7" ry="4" fill="#ff7fa8" opacity=".55"/>'

ARMS = ('<path d="M24 84 L-4 16" style="stroke:var(--shirt)" stroke-width="13" stroke-linecap="round" fill="none"/>'
        '<path d="M76 84 L104 16" style="stroke:var(--shirt)" stroke-width="13" stroke-linecap="round" fill="none"/>'
        '<circle cx="-5" cy="13" r="8" style="fill:var(--skin)"/><circle cx="105" cy="13" r="8" style="fill:var(--skin)"/>')
PHONE = ('<g transform="translate(14 -16)"><circle cx="92" cy="12" r="17" fill="#ffd9ee" opacity=".4"/><rect x="85" y="1" width="14" height="23" rx="3" fill="#2a1a24"/>'
         '<rect x="87" y="3" width="10" height="19" rx="2" fill="#ffeef6"/></g>')
EARS = '<circle cx="11" cy="54" r="8" style="fill:var(--skin)"/><circle cx="89" cy="54" r="8" style="fill:var(--skin)"/>'


def _sym(i, body, vb="0 0 100 120"):
    return f'<symbol id="{i}" viewBox="{vb}" overflow="visible">{body}</symbol>'


DEFS = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>',
        _sym("cArms", ARMS), _sym("cPhone", PHONE), _sym("cEars", EARS), _sym("cBlush", BLUSH), _sym("cGlass", GLASSES), _sym("cFreck", FRECKLES),
        _sym("cBody", '<ellipse cx="50" cy="106" rx="33" ry="24" style="fill:var(--shirt)"/>'),
        _sym("cHeadB", f'<circle cx="50" cy="48" r="39" style="fill:var(--hair)"/>{GLOSS}'),
        _sym("cHeadF", '<circle cx="50" cy="48" r="39" style="fill:var(--skin)"/>'),
        _sym("cSad", SAD_REST),
        _sym("cWBody", '<rect x="34" y="136" width="13" height="30" rx="6" fill="#3a2a40"/><rect x="53" y="136" width="13" height="30" rx="6" fill="#3a2a40"/>'
             '<path d="M27 104 L18 132" style="stroke:var(--shirt)" stroke-width="11" stroke-linecap="round" fill="none"/>'
             '<path d="M73 104 L82 132" style="stroke:var(--shirt)" stroke-width="11" stroke-linecap="round" fill="none"/>'
             '<circle cx="17" cy="135" r="6" style="fill:var(--skin)"/><circle cx="83" cy="135" r="6" style="fill:var(--skin)"/>'
             '<path d="M26 104 Q26 92 50 92 Q74 92 74 104 L76 142 Q50 150 24 142 Z" style="fill:var(--shirt)"/>', "0 0 100 170")]
for k, (back, fb, fo) in STYLES.items():
    DEFS += [_sym(f"hb-{k}", back), _sym(f"hfb-{k}", fb), _sym(f"hfo-{k}", fo)]
for k, v in EYES.items():
    DEFS.append(_sym(f"e-{k}", v))
for k, v in MOUTHS.items():
    DEFS.append(_sym(f"m-{k}", v))
for k, v in SAD_EYES.items():
    DEFS.append(_sym(f"se-{k}", v))
DEFS = "".join(DEFS) + "</defs></svg>"

_deck = []


def _style():
    if not _deck:
        _deck.extend(R.sample(list(STYLES), len(STYLES)))
    return _deck.pop()


def _look():
    return (f"--hair:{R.choice(HAIR)};--skin:{R.choice(SKIN)};--shirt:{R.choice(SHIRT)};--acc:{R.choice(ACC)}")


def _u(sym, extra=""):
    return f'<use href="#{sym}"{extra}/>'


def _head_g(inner, shape):
    sx, sy = shape
    return f'<g transform="translate({HC}) scale({sx} {sy}) translate(-{HC.replace(" ", " -")})">{inner}</g>'


def _extra():
    x = R.random()
    return _u("cGlass") if x < .22 else _u("cFreck") if x < .42 else ""


def _face(happy=True, extra=None):
    if happy:
        f = _u(f"e-{R.choice(list(EYES))}") + _u(f"m-{R.choice(list(MOUTHS))}") + _u("cBlush")
    else:
        f = _u(f"se-{R.choice(list(SAD_EYES))}") + _u("cSad")
    return f + (_extra() if extra is None else extra)


def _front(st):
    return _u(f"hfb-{st}") + _u("cHeadF") + _u(f"hfo-{st}")


def seated(cid, x, top, wd, turn=False, phone=False, style=""):
    """a seated chibi seen from behind; with turn=True it also carries its front (happy) view for turning round"""
    st, shape = _style(), R.choice(SHAPES)
    back = (_u("cEars") if st not in NO_EARS else "") + _u("cHeadB") + _u(f"hb-{st}")
    front = _front(st) + _face(True)
    g = f'<g style="opacity:calc(1 - var(--turn,0))">{_head_g(back, shape)}</g>'
    if turn:
        g += f'<g style="opacity:var(--turn,0)">{_head_g(front, shape)}</g>'
    return (f'<div class="cb" id="{cid}" style="left:{x:.0f}px;top:{top:.0f}px;width:{wd:.0f}px;height:{wd * 1.2:.0f}px;{_look()};{style}">'
            f'<svg class="cbs{" tn" if turn else ""}{" hp" if phone else ""}" viewBox="0 0 100 120" overflow="visible">'
            f'<g style="opacity:var(--arms,0)">{_u("cArms")}</g><g style="opacity:calc(var(--ph,0) * var(--arms,0))">{_u("cPhone")}</g>'
            f'{_u("cBody")}{g}</svg></div>')


def walker(cid, left, top, ww, hh):
    """a standing chibi: sad on the way out, happy (--happy: 1) on the way back"""
    st, shape = _style(), R.choice(SHAPES)
    ex = _extra()
    sad = f'<g style="opacity:calc(1 - var(--happy,0))">{_face(False, ex)}</g>'
    happy = f'<g style="opacity:var(--happy,0)">{_face(True, ex)}</g>'
    head = _head_g(_front(st) + sad + happy, shape)
    return (f'<div class="cbw" id="{cid}" style="left:{left:.0f}px;top:{top:.0f}px;width:{ww:.0f}px;height:{hh:.0f}px;{_look()};--happy:0">'
            f'<svg viewBox="0 0 100 170" overflow="visible">{_u("cWBody")}<g transform="translate(0 4)">{head}</g></svg></div>')
