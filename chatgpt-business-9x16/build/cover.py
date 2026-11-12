"""The cover: the hook frame (ChatGPT recommending two verified businesses, "YOUR BUSINESS?" missing) with a bottom
banner. python3 build/cover.py (from the project root; needs node + the preinstalled Playwright).
Writes renders/nxtlvl_chatgpt-business_reels_9x16_cover.png (1080x1920)."""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "renders", "nxtlvl_chatgpt-business_reels_9x16_cover.png")
JS = r"""
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--disable-gpu'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(process.argv[1], 'index.html'), { waitUntil: 'commit' }); await p.waitForTimeout(3000);
  await p.evaluate(() => { window.__timelines.main.seek(2.6, false); document.getElementById('caps').style.display = 'none';
    const d = document.createElement('div'); d.style.cssText = 'position:absolute;left:70px;right:70px;top:1420px;text-align:center;font:800 54px/1.2 Montserrat;color:#fff';
    d.innerHTML = 'Claim it free <span style="font:italic 400 66px/1 Serif;color:#b687f9">in 4 steps</span>'; document.getElementById('root').appendChild(d); });
  await p.waitForTimeout(200); await p.screenshot({ path: process.argv[2] }); await b.close(); })();
"""
subprocess.run(["node", "-e", JS, ROOT, OUT], check=True)
print("wrote", OUT)
