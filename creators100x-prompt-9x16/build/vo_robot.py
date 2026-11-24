"""The AI-to-human switch: line r0 ("This reel was written by ChatGPT.") is made synthetic -- constant-phase FFT robot
voice, a slight bitcrush and a narrower band -- and the rest stays Jessica's natural voice. Run after vo_tight.py.
python3 build/vo_robot.py"""
import json, os, shutil, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(os.path.join(ROOT, "plan", "words.json")))
r0_end = max(w["t1"] for w in W if w["line"] == "r0") + .12
r1_start = min(w["t0"] for w in W if w["line"] != "r0")
cut = round(min(r0_end, r1_start - .1), 3)
vo = os.path.join(ROOT, "assets", "audio", "vo.wav"); nat = os.path.join(ROOT, "assets", "audio", os.environ.get("VO_NAT", "vo_natural.wav"))
if not os.path.exists(nat):
    shutil.copy(vo, nat)
robot = ("afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=1024:overlap=0.75,"
         "acrusher=bits=9:mix=.35:mode=log,highpass=f=180,lowpass=f=6500,volume=1.25")
filt = (f"[0:a]atrim=0:{cut},asetpts=PTS-STARTPTS,{robot},afade=t=out:st={cut - .03:.3f}:d=0.03[a];"
        f"[0:a]atrim={cut},asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", nat, "-filter_complex", filt, "-map", "[o]", "-ar", "48000", "-ac", "1",
                "-c:a", "pcm_f32le", vo], check=True)
print(f"robot voice 0-{cut} s")
