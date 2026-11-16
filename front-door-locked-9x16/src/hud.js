// Door-camera overlay drawn on its own 2D canvas over the 3D stage, from a plain state each frame
// (seek-safe). state: { live, stamp, date, label, motion (0..1), zoom } or null for no overlay.
const W = 1080, H = 1920;
const F = (w, s) => `${w} ${s}px Poppins, sans-serif`;
let lastKey = "";

export function drawHud(canvas, s) {
  const key = s ? JSON.stringify(s) : "";
  if (key === lastKey) return;
  lastKey = key;
  const g = canvas.getContext("2d");
  g.clearRect(0, 0, W, H);
  if (!s) return;
  g.save();
  // faint scanlines over the whole picture
  g.fillStyle = "rgba(0,0,0,0.10)";
  for (let y = 0; y < H; y += 6) g.fillRect(0, y, W, 2);
  // corner brackets, inside the platform-safe area
  g.strokeStyle = "rgba(255,255,255,0.75)";
  g.lineWidth = 6;
  const L = 70, x0 = 70, x1 = W - 70, y0 = 270, y1 = 1600;
  for (const [x, y, dx, dy] of [[x0, y0, 1, 1], [x1, y0, -1, 1], [x0, y1, 1, -1], [x1, y1, -1, -1]]) {
    g.beginPath();
    g.moveTo(x + dx * L, y);
    g.lineTo(x, y);
    g.lineTo(x, y + dy * L);
    g.stroke();
  }
  g.textBaseline = "middle";
  g.shadowColor = "rgba(0,0,0,0.85)";
  g.shadowBlur = 8;
  // REC / LIVE
  g.fillStyle = "#ff3030";
  g.beginPath();
  g.arc(118, 330, 15, 0, Math.PI * 2);
  g.fill();
  g.fillStyle = "#ffffff";
  g.font = F(800, 44);
  g.textAlign = "left";
  g.fillText(s.live ? "LIVE" : "REC", 146, 332);
  g.font = F(700, 32);
  g.fillStyle = "rgba(255,255,255,0.88)";
  g.fillText(s.label || "FRONT DOOR", 104, 386);
  // timestamp
  g.textAlign = "right";
  g.font = F(800, 44);
  g.fillStyle = "#ffffff";
  g.fillText(s.stamp || "03:12:04 AM", W - 104, 332);
  g.font = F(700, 30);
  g.fillStyle = "rgba(255,255,255,0.8)";
  g.fillText(s.date || "11/14/2026", W - 104, 386);
  // bottom row: IR + zoom
  g.textAlign = "left";
  g.font = F(700, 30);
  g.fillStyle = "rgba(255,255,255,0.8)";
  g.fillText("IR  ON", 104, 1548);
  if (s.zoom) {
    g.textAlign = "right";
    g.fillText(`ZOOM ${s.zoom}`, W - 104, 1548);
  }
  // motion tag
  if (s.motion > 0) {
    g.globalAlpha = Math.min(1, s.motion);
    g.shadowBlur = 0;
    g.fillStyle = "rgba(255,196,40,0.95)";
    const w = 430, x = (W - w) / 2, y = 1440;
    g.beginPath();
    g.roundRect(x, y, w, 70, 14);
    g.fill();
    g.fillStyle = "#151515";
    g.textAlign = "center";
    g.font = F(800, 34);
    g.fillText("MOTION DETECTED", W / 2, y + 37);
  }
  g.restore();
}
