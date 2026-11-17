// Cover for the @write-script reel (v4): the hook frame (person in the mirror, DIDN'T WORK stamp, Cree, the pile of
// rejected scripts) at 4.75 s, shrunk into the 3:4 profile-grid crop, with a cover title on top and a Creedom badge.
// node build/cover.cjs  ->  renders/creators100x_creedom-write-script_reels_9x16_v4_cover.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const out = path.join(root, 'renders', 'creators100x_creedom-write-script_reels_9x16_v4_cover.png');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(root, 'index.html'));
  await p.waitForTimeout(1500);
  await p.evaluate(async () => { await document.fonts.ready; window.__timelines.main.seek(4.8, false); });
  await p.addStyleTag({ content: `
    .head { display: none !important; }
    #cam { transform: translateY(110px) scale(.86) !important; }
    #ctitle { position: absolute; left: 50px; right: 50px; top: 252px; z-index: 70; text-align: center; font-family: Inter; color: #0B0B0B; }
    #ctitle .k { display: inline-block; padding: 10px 26px; border-radius: 999px; background: #101111; color: #CCFB79; font: 30px Mono; letter-spacing: .1em; }
    #ctitle .t { margin-top: 18px; font-weight: 800; font-size: 118px; line-height: .98; letter-spacing: -.05em; }
    #ctitle .t em { font-style: normal; color: #F343A2; }
    #ctitle .t b { position: relative; display: inline-block; }
    #ctitle .t b i { position: absolute; left: -.04em; right: -.04em; bottom: .05em; height: .42em; background: #CCFB79; border-radius: .08em; z-index: -1; }
    #cbadge { position: absolute; left: 50%; top: 1548px; transform: translateX(-50%); z-index: 70; display: flex; align-items: center; gap: 18px;
      padding: 18px 34px; border-radius: 999px; background: #fff; border: 5px solid #101111; box-shadow: 10px 10px 0 #101111; white-space: nowrap;
      font: 800 44px Inter; letter-spacing: -.02em; }
    #cbadge img { height: 46px; }
    #cbadge span { color: #F343A2; }` });
  await p.evaluate(() => {
    const t = document.createElement('div'); t.id = 'ctitle';
    t.innerHTML = '<div class="k">I TRIED 40 AI SCRIPTS</div><div class="t">Not <em>one</em><br><b><i></i>worked.</b></div>';
    const g = document.createElement('div'); g.id = 'cbadge';
    g.innerHTML = '<img src="assets/img/creedom_logo.png"><span>@write-script</span> fits you';
    const r = document.getElementById('root'); r.appendChild(t); r.appendChild(g);
  });
  await p.waitForTimeout(600);
  await p.screenshot({ path: out });
  await b.close();
  console.log(out);
})();
