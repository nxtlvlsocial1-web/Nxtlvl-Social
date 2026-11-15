"""Builds tool/get_chat_clips.py: a copy-paste installer for the setup PDF. Copying from a PDF drops leading spaces, which
breaks Python, so the PDF carries this instead: no indented lines, the tool zlib-compressed in base64 (b64decode skips the
spaces and line breaks a copy adds), and a checksum so the reader knows the copy was complete.
python3 build/make_installer.py  ->  tool/get_chat_clips.py
"""
import base64, hashlib, os, zlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "tool", "chat_clips.py"), "rb").read()
b = base64.b64encode(zlib.compress(src, 9)).decode()
lines = [b[i:i + 96] for i in range(0, len(b), 96)]
h = hashlib.sha256(src).hexdigest()[:12]
out = ("# GTA 6 Chat Clipper installer. Run it once: it writes chat_clips.py\n"
       "# next to this file. If you see zlib.error, copy the block again.\n"
       "import base64, hashlib, os, zlib\n"
       'd = zlib.decompress(base64.b64decode("""\n' + "\n".join(lines) + '\n"""))\n'
       'here = os.path.dirname(os.path.abspath(__file__))\n'
       'p = os.path.join(here, "chat_clips.py")\n'
       'open(p, "wb").write(d)\n'
       f'ok = hashlib.sha256(d).hexdigest().startswith("{h}")\n'
       'print("Done: chat_clips.py is ready." if ok else\n'
       '"Copy error: copy the block again.")\n')
open(os.path.join(ROOT, "tool", "get_chat_clips.py"), "w").write(out)
print(f"tool/get_chat_clips.py: {len(out.splitlines())} lines, longest {max(map(len, out.splitlines()))}")
