"""Animated Shooting Star GIF (no text) for Google Workspace: Gmail signature, Chat, Sites.

Builds anim.html from ../../instagram-profile.svg, captures frames with Playwright (frames.js) at SUB x the GIF
frame rate, blends each SUB into one for motion blur, and writes the GIFs with an optimised palette.
Run:  python3 gif/source/build.py
"""
import os, re, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
SVG = os.path.abspath(os.path.join(HERE, '..', '..', 'instagram-profile.svg'))
FPS, SUB, T = 25, 8, 3.2          # GIF rate, sub-frames per GIF frame, loop length (s)

s = open(SVG).read()
defs = s[s.find('<defs>'):s.find('</defs>') + 7]
body = s[s.find('</defs>') + 7:s.rfind('</svg>')]
bg = ''.join(re.findall(r'<rect[^>]*/>', body))
mark = body[body.find('<g transform'):]
gt = re.search(r'<g transform="([^"]+)">', mark).group(1)
paths = re.findall(r'<path[^>]*/>', mark)          # 3 trails, then the star
trails, star = paths[:3], paths[3]

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;background:#05030C}} svg{{display:block;width:512px;height:512px}}</style></head><body>
<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">{defs.replace('</defs>', '''
<radialGradient id="halo"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset=".25" stop-color="#D8BBFF" stop-opacity=".55"/>
<stop offset="1" stop-color="#A95CFF" stop-opacity="0"/></radialGradient></defs>''')}
{bg}
<g id="mv"><g transform="{gt}">
  <g id="tr">{''.join(trails)}</g>
  <circle id="halo-c" cx="140" cy="60" r="34" fill="url(#halo)" opacity="0"/>
  <g id="st">{star}</g>
</g></g></svg>
<script>
const T={T}, HX=118, HY=82, A=-42*Math.PI/180, DX=Math.cos(A), DY=Math.sin(A);
const cl=v=>Math.max(0,Math.min(1,v)), seg=(t,a,b)=>cl((t-a)/(b-a));
const io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, p3in=x=>x*x*x, xout=x=>x>=1?1:1-Math.pow(2,-10*x);
const $=id=>document.getElementById(id);
window.setT=function(t){{
  t=((t%T)+T)%T;
  // twinkle: the star turns a quarter and flares, a soft halo blooms behind it
  const k=seg(t,.30,1.0), bump=Math.sin(Math.PI*k);
  let rot=90*io(k), sc=1+.32*bump, halo=.9*bump;
  // streak out to the top right, then fly back in from the bottom left
  let d=0, str=1, op=1;
  if(t>=1.30&&t<1.72){{const x=p3in(seg(t,1.30,1.72)); d=300*x; str=1+1.4*x; op=1-seg(t,1.60,1.72);}}
  else if(t>=1.72&&t<2.70){{const x=xout(seg(t,1.72,2.70)); d=-300*(1-x); str=1+1.6*(1-x); op=seg(t,1.72,1.80);}}
  $('mv').setAttribute('transform',`translate(${{d*DX}} ${{d*DY}})`);
  $('mv').setAttribute('opacity',op);
  const a=-42;
  $('tr').setAttribute('transform',`translate(${{HX}} ${{HY}}) rotate(${{a}}) scale(${{str}} 1) rotate(${{-a}}) translate(${{-HX}} ${{-HY}})`);
  $('st').setAttribute('transform',`translate(140 60) rotate(${{rot}}) scale(${{sc}}) translate(-140 -60)`);
  $('halo-c').setAttribute('opacity',halo);
}};
window.setT(0);
</script></body></html>'''
open(os.path.join(HERE, 'anim.html'), 'w').write(html)

fr = os.path.join(HERE, 'frames'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
n = int(round(T * FPS * SUB))
subprocess.run(['node', os.path.join(HERE, 'frames.js'), os.path.join(HERE, 'anim.html'), fr, str(n), str(T), str(SUB)], check=True)

def gif(size, name):
    blur = f'tmix=frames={SUB}:weights=1,select=eq(mod(n\\,{SUB})\\,{SUB - 1}),setpts=N/{FPS}/TB'
    scale = '' if size == 512 else f',scale={size}:{size}:flags=lanczos'
    fc = (f'[0:v]{blur}{scale},split[a][b];[a]palettegen=max_colors=192:stats_mode=full[p];'
          f'[b][p]paletteuse=dither=sierra2_4a')
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-framerate', str(FPS * SUB),
                    '-i', os.path.join(fr, 'f%04d.png'), '-filter_complex', fc, '-loop', '0',
                    os.path.join(OUT, name)], check=True)

gif(512, 'nxtlvl-shooting-star-512.gif')
gif(200, 'nxtlvl-shooting-star-200.gif')
gif(96, 'nxtlvl-shooting-star-96.gif')
shutil.rmtree(fr)
print('wrote', ', '.join(f for f in sorted(os.listdir(OUT)) if f.endswith('.gif')))
