// 2D overlay canvas drawn over the 3D stage each frame from a plain state (seek-safe).
// Modes: "cam" (hidden/door camera: REC, label, timestamp), "photo" (a print with a white border),
// "price" (two price cards), "stamp" (a rubber stamp), "year" (a big year tag for flashbacks).
const W = 1920, H = 1080;
const F = (w, s) => `${w} ${s}px Poppins, sans-serif`;
let lastKey = "";

function rr(g, x, y, w, h, r) {
  g.beginPath();
  g.roundRect(x, y, w, h, r);
}

export function drawHud(canvas, s) {
  const key = s ? JSON.stringify(s) : "";
  if (key === lastKey) return;
  lastKey = key;
  const g = canvas.getContext("2d");
  g.clearRect(0, 0, W, H);
  if (!s) return;
  g.save();
  g.textBaseline = "middle";
  const k = s.k ?? 1; // fade-in amount
  g.globalAlpha = Math.min(1, Math.max(0, k));
  if (s.mode === "cam" || !s.mode) {
    g.fillStyle = "rgba(0,0,0,0.10)";
    for (let y = 0; y < H; y += 5) g.fillRect(0, y, W, 2);
    g.strokeStyle = "rgba(255,255,255,0.8)";
    g.lineWidth = 5;
    const L = 70, x0 = 80, x1 = W - 80, y0 = 70, y1 = H - 70;
    for (const [x, y, dx, dy] of [[x0, y0, 1, 1], [x1, y0, -1, 1], [x0, y1, 1, -1], [x1, y1, -1, -1]]) {
      g.beginPath();
      g.moveTo(x + dx * L, y);
      g.lineTo(x, y);
      g.lineTo(x, y + dy * L);
      g.stroke();
    }
    g.shadowColor = "rgba(0,0,0,0.85)";
    g.shadowBlur = 8;
    g.fillStyle = "#ff3030";
    g.beginPath();
    g.arc(130, 125, 14, 0, Math.PI * 2);
    g.fill();
    g.fillStyle = "#fff";
    g.font = F(800, 40);
    g.textAlign = "left";
    g.fillText(s.live ? "LIVE" : "REC", 156, 127);
    g.font = F(700, 30);
    g.fillStyle = "rgba(255,255,255,0.88)";
    g.fillText(s.label || "CAMERA 1", 118, 178);
    g.textAlign = "right";
    g.font = F(800, 40);
    g.fillStyle = "#fff";
    g.fillText(s.stamp || "", W - 118, 127);
    g.font = F(700, 28);
    g.fillStyle = "rgba(255,255,255,0.8)";
    g.fillText(s.date || "", W - 118, 178);
  } else if (s.mode === "photo") {
    // white print border with a soft drop shadow, slightly rotated
    g.translate(W / 2, H / 2);
    g.rotate(s.rot ?? -0.02);
    const pw = W * 0.74, ph = H * 0.8;
    g.fillStyle = "rgba(0,0,0,0.0)";
    g.lineWidth = 46;
    g.strokeStyle = "#f2efe6";
    g.shadowColor = "rgba(0,0,0,0.6)";
    g.shadowBlur = 40;
    g.strokeRect(-pw / 2, -ph / 2, pw, ph);
    g.shadowBlur = 0;
    // black outside the print
    g.fillStyle = "#0a0a0c";
    g.fillRect(-W, -H, W * 2, H / 2 - ph / 2 + H / 2 - 23);
    g.fillRect(-W, ph / 2 + 23, W * 2, H);
    g.fillRect(-W, -ph / 2 - 23, W / 2 - pw / 2 + W / 2 - 23, ph + 46);
    g.fillRect(pw / 2 + 23, -ph / 2 - 23, W, ph + 46);
    if (s.caption) {
      g.fillStyle = "#3a3630";
      g.font = F(700, 30);
      g.textAlign = "center";
      g.fillText(s.caption, 0, ph / 2 + 2);
    }
  } else if (s.mode === "price") {
    const cards = [["PAID · 2014", "~$1.36M", "#2f6fe0"], ["SOLD · 2019", "~$959K", "#d9452f"]];
    cards.forEach(([a, b, c], i) => {
      const x = W / 2 - 520 + i * 560, y = 300;
      const kk = Math.min(1, Math.max(0, (s.k2 ?? 1) * 2 - i));
      g.globalAlpha = Math.min(k, kk);
      g.fillStyle = "rgba(12,12,16,0.86)";
      rr(g, x, y, 480, 300, 28);
      g.fill();
      g.fillStyle = c;
      rr(g, x, y, 480, 70, [28, 28, 0, 0]);
      g.fill();
      g.fillStyle = "#fff";
      g.font = F(800, 34);
      g.textAlign = "center";
      g.fillText(a, x + 240, y + 37);
      g.font = F(800, 110);
      g.fillText(b, x + 240, y + 190);
    });
    g.globalAlpha = k * Math.min(1, Math.max(0, (s.k2 ?? 1) * 2 - 1.2));
    g.fillStyle = "#ffb020";
    g.font = F(800, 54);
    g.textAlign = "center";
    g.fillText("a loss of about $400,000", W / 2, 690);
  } else if (s.mode === "stamp") {
    g.translate(W / 2 + (s.x ?? 0), H / 2 - 60);
    g.rotate(-0.12);
    const sc = 1 + (1 - Math.min(1, k)) * 0.6;
    g.scale(sc, sc);
    g.strokeStyle = "#e5322d";
    g.lineWidth = 14;
    rr(g, -420, -110, 840, 220, 24);
    g.stroke();
    g.fillStyle = "#e5322d";
    g.font = F(800, 120);
    g.textAlign = "center";
    g.fillText(s.text || "DENIED", 0, 8);
    if (s.sub) {
      g.font = F(800, 34);
      g.fillText(s.sub, 0, 150);
    }
  } else if (s.mode === "year") {
    g.shadowColor = "rgba(0,0,0,0.8)";
    g.shadowBlur = 20;
    g.fillStyle = "rgba(255,240,210,0.92)";
    g.font = F(800, 120);
    g.textAlign = "left";
    g.fillText(s.text || "", 110, H - 170);
    if (s.sub) {
      g.font = F(700, 34);
      g.fillText(s.sub, 116, H - 90);
    }
  }
  g.restore();
}
