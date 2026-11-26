"""Stand-in app screens for scenes H and K while Klap's own screen recording is missing (a machine reset wiped the
upload). Writes three tiny HyperFrames compositions to cache/mock/, renders them, and encodes them to the same files the
recording would make: assets/video/rec_paste.mp4, rec_gen.mp4 (1080x510) and rec_edit2.mp4 (980x700).
PREVIEW ONLY: these are a stylised mock of the flow, not Klap's real interface. For the final, rebuild the rec_* clips
from the real recording:  bash build/recover.sh path/to/klap.mp4   (or just its "Klap's screen recording" block).
  python3 build/mock_screens.py
"""
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cache", "mock")
V = os.path.join(ROOT, "assets", "video")
INK, VIOLET, SOFT, LINE, MUTED = "#0f172a", "#8b5cf6", "#f4f2ff", "#e6e8ef", "#64748b"

FONTS = """
@font-face { font-family: Pop; font-weight: 500; src: url("assets/fonts/poppins-500.woff2"); }
@font-face { font-family: Pop; font-weight: 600; src: url("assets/fonts/poppins-600.woff2"); }
@font-face { font-family: Pop; font-weight: 700; src: url("assets/fonts/poppins-700.woff2"); }
@font-face { font-family: Pop; font-weight: 800; src: url("assets/fonts/poppins-800.woff2"); }
@font-face { font-family: Mono; font-weight: 700; src: url("assets/fonts/JetBrainsMono-Bold.ttf"); }
* { margin: 0; padding: 0; box-sizing: border-box; }
"""
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 12.5l4.5 4.5 10.5-10.5"/></svg>'
LINK = f'<svg viewBox="0 0 24 24" fill="none" stroke="{MUTED}" stroke-width="2.4" stroke-linecap="round"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/></svg>'
CURSOR = '<svg id="cur" viewBox="0 0 24 24"><path d="M4 2l15 11-6.6 1.1L16 21l-3 1.4-3.6-7L4 19.5z" fill="#0f172a" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>'


def page(w, h, dur, css, body, js):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width={w}, height={h}" />
<script src="assets/vendor/gsap.min.js"></script>
<style>{FONTS}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; background: #fff; }}
#root {{ position: relative; width: {w}px; height: {h}px; overflow: hidden; background: #fff; font-family: Pop; font-weight: 600; color: {INK}; }}
.rail {{ position: absolute; left: 0; top: 0; bottom: 0; width: 84px; border-right: 2px solid {LINE}; background: #fafafc; }}
.rail img {{ position: absolute; left: 20px; top: 20px; width: 44px; }}
.rail i {{ position: absolute; left: 26px; width: 32px; height: 32px; border-radius: 9px; background: {LINE}; }}
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-fps="30" data-width="{w}" data-height="{h}">
<div class="rail"><img src="assets/img/klap_icon_ink.svg" alt=""><i style="top:104px"></i><i style="top:156px"></i><i style="top:208px"></i></div>
{body}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused: true}});
{js}
tl.set({{}}, {{}}, {dur});
window.__timelines["main"] = tl;
</script></body></html>"""


# 1. rec_paste: the link lands in the box, the stream is recognised, "Create shorts" is pressed
PASTE = dict(w=1080, h=510, dur=3.4, css=f"""
#h1 {{ position: absolute; left: 84px; right: 0; top: 52px; text-align: center; font-weight: 800; font-size: 44px; letter-spacing: -.02em; }}
#h2 {{ position: absolute; left: 84px; right: 0; top: 112px; text-align: center; font-weight: 500; font-size: 21px; color: {MUTED}; }}
#box {{ position: absolute; left: 172px; width: 820px; top: 170px; height: 84px; border-radius: 20px; border: 2px solid {LINE}; background: #fff;
  box-shadow: 0 10px 30px rgba(15,23,42,.07); display: flex; align-items: center; padding: 0 16px 0 24px; gap: 14px; }}
#box svg {{ width: 28px; height: 28px; flex: none; }}
#ph, #url {{ position: absolute; left: 76px; font-size: 23px; }}
#ph {{ color: #94a3b8; font-weight: 500; }} #url {{ opacity: 0; font-weight: 600; padding: 2px 6px; border-radius: 6px; }}
#btn {{ position: absolute; right: 12px; top: 11px; height: 58px; padding: 0 28px; border-radius: 14px; background: {VIOLET}; color: #fff;
  font-weight: 700; font-size: 22px; display: flex; align-items: center; gap: 10px; transform-origin: 50% 50%; }}
#spin {{ width: 22px; height: 22px; border-radius: 50%; border: 3px solid rgba(255,255,255,.35); border-top-color: #fff; display: none; }}
#prev {{ position: absolute; left: 172px; width: 820px; top: 282px; height: 160px; border-radius: 20px; background: {SOFT};
  display: flex; align-items: center; gap: 24px; padding: 18px; opacity: 0; }}
#prev .th {{ width: 220px; height: 124px; border-radius: 12px; overflow: hidden; position: relative; flex: none; }}
#prev .th img {{ width: 100%; height: 100%; object-fit: cover; }}
#prev .th b {{ position: absolute; right: 8px; bottom: 8px; font-family: Mono; font-size: 15px; color: #fff; background: rgba(0,0,0,.72); padding: 2px 7px; border-radius: 6px; }}
#prev .k {{ font-family: Mono; font-size: 15px; letter-spacing: .14em; color: {VIOLET}; }}
#prev .t {{ font-weight: 700; font-size: 27px; line-height: 1.2; margin-top: 6px; }}
#prev .m {{ font-weight: 500; font-size: 19px; color: {MUTED}; margin-top: 6px; }}
#cur {{ position: absolute; left: 640px; top: 470px; width: 34px; height: 34px; }}
""", body=f"""
<div id="h1">Turn videos into viral shorts</div><div id="h2">Drop a long video. Get the best clips back.</div>
<div id="box">{LINK}<span id="ph">Paste a YouTube, Twitch or Kick link</span><span id="url">twitch.tv/videos/gta6-launch-stream</span>
  <div id="btn"><span id="spin"></span><span id="bt">Create shorts</span></div></div>
<div id="prev"><div class="th"><img src="assets/img/m_stream.jpg" alt=""><b>3:02:41</b></div>
  <div><div class="k">STREAM FOUND</div><div class="t">GTA VI launch stream</div><div class="m">3 h 2 min · English · gameplay + facecam</div></div></div>
{CURSOR}
""", js="""
tl.set("#ph", {opacity: 0}, .25).fromTo("#url", {opacity: 0, backgroundColor: "rgba(139,92,246,.28)"}, {opacity: 1, duration: .08}, .25)
  .to("#url", {backgroundColor: "rgba(139,92,246,0)", duration: .5}, .45)
  .fromTo("#box", {borderColor: "#e6e8ef"}, {borderColor: "#8b5cf6", duration: .2}, .25)
  .fromTo("#prev", {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: .45, ease: "power3.out"}, .55)
  .to("#cur", {left: 930, top: 236, duration: .75, ease: "power2.inOut"}, .9)
  .to("#btn", {scale: .94, duration: .08, ease: "power1.in"}, 1.72).to("#btn", {scale: 1, duration: .18, ease: "back.out(3)"}, 1.8)
  .set("#spin", {display: "block"}, 1.8).set("#bt", {textContent: "Creating"}, 1.8)
  .to("#spin", {rotation: 720, duration: 1.6, ease: "none"}, 1.8);
""")

# 2. rec_gen: progress through the steps, then three clips with their virality scores
CARDS = (("m_flip", 99), ("m_cops", 94), ("m_heli", 87))
GEN = dict(w=1080, h=510, dur=3.6, css=f"""
#st {{ position: absolute; left: 132px; top: 40px; font-weight: 800; font-size: 32px; letter-spacing: -.01em; }}
#pc {{ position: absolute; right: 48px; top: 44px; font-family: Mono; font-size: 26px; color: {VIOLET}; }}
#bar {{ position: absolute; left: 132px; right: 48px; top: 96px; height: 12px; border-radius: 6px; background: {LINE}; overflow: hidden; }}
#barf {{ width: 100%; height: 100%; background: {VIOLET}; transform-origin: 0 50%; transform: scaleX(0); }}
.step {{ position: absolute; top: 128px; display: flex; align-items: center; gap: 10px; font-size: 19px; font-weight: 600; color: {MUTED}; }}
.step .d {{ width: 28px; height: 28px; border-radius: 50%; background: {LINE}; display: grid; place-items: center; }}
.step .d svg {{ width: 17px; height: 17px; opacity: 0; }}
.card {{ position: absolute; top: 186px; width: 268px; height: 300px; border-radius: 18px; overflow: hidden; background: {SOFT}; opacity: 0;
  box-shadow: 0 12px 30px rgba(15,23,42,.12); }}
.card img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
.card .sc {{ position: absolute; left: 12px; top: 12px; display: flex; align-items: baseline; gap: 4px; padding: 6px 12px; border-radius: 12px;
  background: #fff; font-weight: 800; font-size: 30px; color: {INK}; }}
.card .sc small {{ font-size: 15px; color: {MUTED}; font-weight: 600; }}
.card .lb {{ position: absolute; left: 0; right: 0; bottom: 0; padding: 30px 14px 12px; font-size: 17px; color: #fff; font-weight: 700;
  background: linear-gradient(transparent, rgba(0,0,0,.75)); }}
""", body="""
<div id="st">Finding the best moments</div><div id="pc">0%</div><div id="bar"><div id="barf"></div></div>
""" + "".join(f'<div class="step" id="sp{i}" style="left:{132 + i * 300}px"><span class="d">{CHECK}</span>{t}</div>'
              for i, t in enumerate(("Transcribing", "Finding moments", "Scoring virality"))) + "".join(
    f'<div class="card" id="cd{i}" style="left:{132 + i * 300}px"><img src="assets/img/{s}.jpg" alt=""><div class="sc"><span id="n{i}">0</span><small>/100</small></div>'
    f'<div class="lb">Clip {i + 1} · 0:{[28, 41, 33][i]}</div></div>' for i, (s, v) in enumerate(CARDS)), js="""
const P = {p: 0};
tl.to(P, {p: 1, duration: 1.1, ease: "power1.inOut", onUpdate: () => {
  document.getElementById("pc").textContent = Math.round(P.p * 100) + "%";
  document.getElementById("barf").style.transform = "scaleX(" + P.p + ")"; }}, 0);
[0, 1, 2].forEach(i => {
  const t = .3 + i * .38;
  tl.to(`#sp${i} .d`, {backgroundColor: "#22c55e", duration: .12}, t).to(`#sp${i} .d svg`, {opacity: 1, duration: .12}, t)
    .to(`#sp${i}`, {color: "#0f172a", duration: .12}, t);
});
tl.set("#st", {textContent: "3 clips ready"}, 1.15);
""" + "".join(f"""
tl.fromTo("#cd{i}", {{opacity: 0, y: 30, scale: .96}}, {{opacity: 1, y: 0, scale: 1, duration: .45, ease: "power3.out"}}, {1.2 + i * .14:.2f});
(() => {{ const o = {{v: 0}}; tl.to(o, {{v: {v}, duration: .8, ease: "power2.out", onUpdate: () => document.getElementById("n{i}").textContent = Math.round(o.v)}}, {1.3 + i * .14:.2f}); }})();
""" for i, (s, v) in enumerate(CARDS)))

# 3. rec_edit2: the caption editor, captions popping word by word over the vertical clip
WORDS = ("THIS", "CHASE", "IS", "INSANE")
EDIT = dict(w=980, h=700, dur=3.0, css=f"""
#ph {{ position: absolute; left: 124px; top: 36px; width: 352px; height: 626px; border-radius: 26px; overflow: hidden; background: #000;
  box-shadow: 0 16px 40px rgba(15,23,42,.22); }}
#ph video {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; }}
#cap {{ position: absolute; left: 0; right: 0; top: 420px; text-align: center; font-weight: 800; font-size: 40px; line-height: 1.1; color: #fff;
  -webkit-text-stroke: 2px #000; paint-order: stroke fill; }}
#cap span {{ display: inline-block; margin: 0 4px; opacity: 0; transform-origin: 50% 70%; }}
#pan {{ position: absolute; left: 526px; right: 34px; top: 36px; }}
#pan h3 {{ font-weight: 800; font-size: 30px; letter-spacing: -.01em; }}
#pan .k {{ font-family: Mono; font-size: 15px; letter-spacing: .14em; color: {MUTED}; margin: 22px 0 12px; }}
.tiles {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
.tile {{ height: 86px; border-radius: 14px; border: 2px solid {LINE}; display: grid; place-items: center; font-weight: 800; font-size: 22px; background: #fafafc; }}
.tile.sel {{ border: 3px solid {VIOLET}; background: {SOFT}; }}
.row {{ display: flex; justify-content: space-between; align-items: center; height: 58px; border-bottom: 2px solid {LINE}; font-size: 20px; }}
.tg {{ width: 52px; height: 30px; border-radius: 15px; background: {VIOLET}; position: relative; }}
.tg::after {{ content: ""; position: absolute; right: 4px; top: 4px; width: 22px; height: 22px; border-radius: 50%; background: #fff; }}
.tg.off {{ background: {LINE}; }} .tg.off::after {{ right: auto; left: 4px; }}
#wl {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 18px; }}
#wl b {{ padding: 6px 12px; border-radius: 10px; background: {LINE}; font-size: 17px; font-weight: 700; }}
""", body=f"""
<div id="ph"><video id="pv" src="assets/video/c_flip.mp4" data-start="0" data-duration="3" data-media-start="0" data-track-index="1" muted playsinline></video>
  <div id="cap">{''.join(f'<span id="w{i}">{w}</span>' for i, w in enumerate(WORDS))}</div></div>
<div id="pan"><h3>Captions</h3><div class="k">STYLE</div>
  <div class="tiles"><div class="tile sel" style="background:#0f172a;color:#fff;font-size:24px">BOLD <span style=\"color:#facc15\">POP</span></div><div class="tile">Clean</div>
  <div class="tile" style="color:{VIOLET}">Karaoke</div><div class="tile" style="font-family:Mono;font-size:20px">Mono</div></div>
  <div class="k">ANIMATION</div>
  <div class="row">Word by word<span class="tg"></span></div><div class="row">Highlight keywords<span class="tg"></span></div>
  <div class="row">All caps<span class="tg off" id="caps"></span></div>
  <div id="wl">{''.join(f'<b id="wb{i}">{w.lower()}</b>' for i, w in enumerate(WORDS))}</div></div>
""", js="""
const ON = [.1, .3, .48, .66];
ON.forEach((t, i) => {
  tl.fromTo(`#w${i}`, {opacity: 0, scale: .5, y: 14}, {opacity: 1, scale: 1, y: 0, duration: .22, ease: "back.out(2.6)"}, t)
    .to(`#wb${i}`, {backgroundColor: "#8b5cf6", color: "#fff", duration: .1}, t);
  if (i > 0) tl.to(`#wb${i - 1}`, {backgroundColor: "#e6e8ef", color: "#0f172a", duration: .1}, t);
});
tl.to("#w3", {color: "#facc15", duration: .1}, .66)
  .to("#caps", {backgroundColor: "#8b5cf6", duration: .15}, 1.7);
""")


def frames():
    img = os.path.join(OUT, "img")
    os.makedirs(img, exist_ok=True)
    jobs = [("c_cops", 1.0, "scale=640:-2,crop=640:360", "m_stream"), ("t_flip", 1.0, "scale=360:640", "m_flip"),
            ("t_cops", 1.2, "scale=360:640", "m_cops"), ("t_heli", 1.0, "scale=360:640", "m_heli")]
    for src, t, vf, name in jobs:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", os.path.join(V, src + ".mp4"), "-frames:v", "1", "-vf", vf,
                        "-q:v", "3", os.path.join(img, name + ".jpg")], check=True)
    return img


def build(name, spec, img):
    d = os.path.join(OUT, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "assets", "img"))
    open(os.path.join(d, "index.html"), "w").write(page(spec["w"], spec["h"], spec["dur"], spec["css"], spec["body"], spec["js"]))
    for sub in ("fonts", "vendor", "video"):
        os.symlink(os.path.join(ROOT, "assets", sub), os.path.join(d, "assets", sub))
    for f in os.listdir(img):
        shutil.copy(os.path.join(img, f), os.path.join(d, "assets", "img", f))
    shutil.copy(os.path.join(ROOT, "assets", "img", "klap_icon_ink.svg"), os.path.join(d, "assets", "img"))
    shutil.copy(os.path.join(ROOT, "hyperframes.json"), d)
    return d


if __name__ == "__main__":
    img = frames()
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1")
    for name, spec in (("rec_paste", PASTE), ("rec_gen", GEN), ("rec_edit2", EDIT)):
        d = build(name, spec, img)
        raw = os.path.join(d, "raw.mp4")
        r = subprocess.run(["npx", "--yes", "hyperframes@0.8.203", "render", "-w", "2", "-o", raw], cwd=d, env=env, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True)
        if r.returncode or not os.path.exists(raw):
            print(name, "RENDER FAILED", r.stdout[-1500:], r.stderr[-1500:])
            raise SystemExit(1)
        speed = "setpts=PTS/1.5," if name == "rec_gen" else ""   # played 1.5x, as the real recording was
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-vf", speed + "tpad=stop_mode=clone:stop_duration=2.5", "-an", "-c:v", "libx264",
                        "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-g", "10", "-r", "30", os.path.join(V, name + ".mp4")], check=True)
        print("wrote", name)
