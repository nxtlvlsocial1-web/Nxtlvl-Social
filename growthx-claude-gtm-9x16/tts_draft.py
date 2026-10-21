# Placeholder Hinglish voiceover with local Kokoro (sherpa-onnx), phrase by phrase,
# so phrase timings are exact. Writes assets/voiceover.wav + phrases.json.
# Usage: python3 tts_draft.py <kokoro-multi-lang-v1_0 dir>
import json, os, sys, wave
import numpy as np
import sherpa_onnx

D = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SPK = 33  # hm_omega (Hindi male)
GAP = 0.16
PHRASES = [
    "अब तुम अपनी पूरी मार्केटिंग टीम",
    "क्लॉड के अंदर चला सकते हो!",
    "ये तुम्हारी ब्रांड स्ट्रैटेजी बनाएगा,",
    "एस ई ओ ब्लॉग्स लिखेगा,",
    "लिंक्डइन पोस्ट्स बनाएगा,",
    "और प्रोडक्ट वीडियोज़ भी जनरेट करेगा।",
    "सेटअप सिंपल है।",
    "पहले, एक नया क्लॉड प्रोजेक्ट बनाओ",
    "और स्टार्टर प्रॉम्प्ट यूज़ करो, ताकि क्लॉड तुम्हारा बिज़नेस समझे।",
    "फिर फायरक्रॉल एम सी पी कनेक्ट करो,",
    "कॉम्पिटिटर्स एनालाइज़ करने और अपनी ब्रांड वॉइस बनाने के लिए।",
    "उसके बाद, राइटर से एस ई ओ कंटेंट जनरेट करो।",
    "फिर हिग्सफ़ील्ड एम सी पी और रिमोशन से प्रोडक्ट वीडियोज़ बनाओ।",
    "और लास्ट में, टाइपफ़ुली से सब पब्लिश करो,",
    "और सब कुछ एक जी टी एम कमांड सेंटर से मैनेज करो।",
    "कमेंट करो जी टी एम,",
    "और पूरा सेटअप गाइड मैं तुम्हें डी एम कर दूँगा।",
]
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
        model=f"{D}/model.onnx", voices=f"{D}/voices.bin", tokens=f"{D}/tokens.txt",
        data_dir=f"{D}/espeak-ng-data", dict_dir=f"{D}/dict",
        lexicon=f"{D}/lexicon-us-en.txt,{D}/lexicon-zh.txt", lang="hi"),
    num_threads=4))
tts = sherpa_onnx.OfflineTts(cfg)
out, spans, t, sr = [], [], 0.0, None
for p in PHRASES:
    a = tts.generate(p, sid=SPK, speed=1.34)
    sr = a.sample_rate
    x = np.array(a.samples, dtype=np.float32)
    # trim leading/trailing near-silence
    idx = np.where(np.abs(x) > 0.01)[0]
    x = x[max(idx[0] - int(.02 * sr), 0): idx[-1] + int(.04 * sr)] if len(idx) else x
    spans.append([round(t, 3), round(t + len(x) / sr, 3)])
    out += [x, np.zeros(int(GAP * sr), dtype=np.float32)]
    t += len(x) / sr + GAP
y = np.concatenate(out)
y = y / max(1e-6, np.abs(y).max()) * 0.9
os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
with wave.open(os.path.join(HERE, "assets", "voiceover.wav"), "wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes((y * 32767).astype("<i2").tobytes())
json.dump({"duration": round(len(y) / sr, 3), "spans": spans}, open(os.path.join(HERE, "phrases.json"), "w"), indent=1)
print("duration", round(len(y) / sr, 2)); print(spans)
