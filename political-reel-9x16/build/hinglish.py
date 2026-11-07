"""Devanagari -> Hinglish (Roman) for the captions, the way the speaker would type it. Used by build/generate.py."""
import re

MAP = {
    "दिवाली": "Diwali", "के": "ke", "लिए": "liye", "आप": "aap", "सामान": "saamaan", "केवल": "keval", "उन": "un",
    "लोगों": "logon", "से": "se", "खरीदिए": "khareediye", "जो": "jo", "अपने": "apne", "सिर": "sir", "पर": "par",
    "तिलक": "tilak", "लगाते": "lagaate", "हैं": "hain", "और": "aur", "जय": "Jai", "श्री": "Shri", "राम": "Ram",
    "बोलते": "bolte", "ये": "ye", "मैं": "main", "नहीं": "nahi", "कह": "keh", "रही": "rahi", "हूँ": "hoon",
    "कहा": "kaha", "है": "hai", "महाराष्ट्र": "Maharashtra", "नितेश": "Nitesh", "राणे": "Rane", "ने": "ne",
    "आज": "aaj", "उनकी": "unki", "बात": "baat", "को": "ko", "करना": "karna", "चाहती": "chahti", "समय": "samay",
    "हर": "har", "एक": "ek", "इंसान": "insaan", "पटाखे": "pataakhe", "जलाता": "jalaata", "अगर": "agar", "हम": "hum",
    "मुंबई": "Mumbai", "की": "ki", "करें": "karein", "तो": "toh", "में": "mein", "पटाखों": "pataakhon", "का": "ka",
    "सबसे": "sabse", "बड़ा": "bada", "मोहम्मद": "Mohammad", "अली": "Ali", "रोड": "Road", "ज्यादातर": "zyaadatar",
    "मुसलमान": "Musalmaan", "ही": "hi", "करते": "karte", "उसके": "uske", "अलावा": "alaawa", "सब": "sab",
    "घरों": "gharon", "बाहर": "baahar", "कंदील": "kandeel", "जलाते": "jalaate", "पुणे": "Pune", "अत्तर": "Attar",
    "पिछले": "pichhle", "कितनी": "kitni", "सारी": "saari", "पीढ़ियों": "peedhiyon", "बनाती": "banaati",
    "रहते": "rehte", "मुंबईकर": "Mumbaikar", "आपको": "aapko", "पता": "pata", "होगा": "hoga", "आधा": "aadha",
    "ज्यादा": "zyaada", "उधर": "udhar", "करता": "karta", "कि": "ki", "उसमें": "usmein", "लोग": "log",
    "धनतेरस": "Dhanteras", "लेते": "lete", "खरीदते": "khareedte", "कौन": "kaun", "सा": "sa", "भी": "bhi", "वो": "woh",
    "कहाँ": "kahaan", "होती": "hoti", "नए": "naye", "कपड़े": "kapde", "आने": "aane", "बनते": "bante", "अब": "ab",
    "मैंने": "maine", "जितने": "jitne", "सारे": "saare", "नाम": "naam", "थी": "thi", "पारसी": "Parsi", "इन": "in",
    "सबके": "sabke", "बिना": "bina", "हमारे": "hamaare", "भाइयों": "bhaiyon", "बहनों": "behnon", "हमारी": "hamaari",
    "अधूरी": "adhoori", "खैर": "khair", "समझाए": "samjhaaye", "खिलाफ": "khilaaf", "जाती": "jaati", "बस": "bas",
    "यही": "yahi", "कहना": "kehna", "चाहूँगी": "chaahungi", "मेरे": "mere", "हिंदू": "Hindu", "मुस्लिम": "Muslim",
    "सिख": "Sikh", "ईसाई": "Isaai", "जैन": "Jain", "बहन": "behen",
}


def roman(word):
    """One Scribe word (may carry punctuation) -> Roman, punctuation kept (। becomes .)."""
    m = re.match(r"^(.*?)([।,.?!\-]*)$", word)
    core, punct = m.group(1), m.group(2).replace("।", ".").replace("--", "")
    if not re.search("[ऀ-ॿ]", core):
        return core + punct
    if core not in MAP:
        raise KeyError(f"no Hinglish for {core!r}")
    return MAP[core] + punct
