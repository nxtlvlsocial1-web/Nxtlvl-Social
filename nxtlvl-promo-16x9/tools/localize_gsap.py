"""Point index.html's GSAP tag at the vendored copy (assets/vendor/gsap.min.js, same 3.14.2 build).
The assembler writes a jsdelivr tag; this sandbox (and any offline render machine) can't reach it.
Run after every assemble-index / transitions inject: python3 tools/localize_gsap.py"""
import re, os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
s = open(p).read()
s2, n = re.subn(r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]+/dist/gsap\.min\.js"[^>]*></script>',
                '<script src="assets/vendor/gsap.min.js"></script>', s)
open(p, 'w').write(s2)
print('localized', n, 'gsap tag(s)')
