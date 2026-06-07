import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IN_PATH = ROOT / "src" / "data" / "questions.json"
OUT_PATH = IN_PATH

CURATED = [
    {"question": "Quel objectif du traitement d'une fracture correspond a l'asepsie ?", "answer": "Absence de germes", "context": "Absence de germes -> Asepsie", "source": "fractures", "type": "curated"},
    {"question": "Quel principe du traitement d'une fracture correspond a la contention des fragments ?", "answer": "stabilisation", "context": "Contention des fragments -> stabilisation", "source": "fractures", "type": "curated"},
    {"question": "Quel objectif du traitement d'une fracture correspond a l'epargne tissulaire ?", "answer": "Respect de la vascularisation et des tissus mous", "context": "Respect de la vascularisation et des tissus mous -> Epargne tissulaire", "source": "fractures", "type": "curated"},
    {"question": "Quelle immobilisation est indiquee pour les fractures sous le coude et le grasset chez le chien en urgence ?", "answer": "bandage de Robert Jones", "context": "Fractures sous le coude et le grasset -> bandage de Robert Jones", "source": "fractures", "type": "curated"},
    {"question": "Quelle immobilisation est indiquee en dehors des fractures sous le coude et le grasset en urgence ?", "answer": "Confinement en cage", "context": "Autres cas -> Confinement en cage", "source": "fractures", "type": "curated"},
    {"question": "Citez une indication du traitement conservateur d'une fracture.", "answer": "Fracture fermee, isolee, non articulaire, situee sous le coude et le grasset", "context": "Indications du traitement conservateur", "source": "fractures", "type": "curated"},
    {"question": "Citez une contre-indication du traitement conservateur d'une fracture.", "answer": "Fracture ouverte", "context": "Indications du traitement chirurgical", "source": "fractures", "type": "curated"},
    {"question": "Combien de temps faut-il attendre apres le traumatisme avant de poser une resine ?", "answer": "48 h", "context": "Attendre 48 h apres le traumatisme", "source": "fractures", "type": "curated"},
    {"question": "Quel pourcentage des tumeurs osseuses sont malignes chez le chien ?", "answer": "95%", "context": "95 % des tumeurs osseuses sont malignes", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quel pourcentage des tumeurs osseuses represente l'osteosarcome ?", "answer": "85%", "context": "Osteosarcome : 85% des tumeurs osseuses", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quelle est l'incidence de l'osteosarcome chez le chien ?", "answer": "13.9 /100 000", "context": "incidence : 13.9 /100 000", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quel pourcentage des tumeurs chez le chien represente l'osteosarcome ?", "answer": "5%", "context": "l'osteosarcome : 5% des tumeurs chez le chien", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quelle proportion des tumeurs osseuses primaires correspond aux osteosarcomes ?", "answer": "> 80%", "context": "Osteosarcomes > 80%", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quel pourcentage des chiens atteints d'osteosarcome presente des metastases au moment de la prise en charge ?", "answer": "90%", "context": "90 % des OSK au moment de la prise en charge", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quelle localisation appendiculaire est typique de l'osteosarcome ?", "answer": "loin du coude, pres du grasset", "context": "Osteosarcome appendiculaire : loin du coude, pres du grasset", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quel pourcentage des cas concerne les races grandes (>25 kg) dans l'osteosarcome ?", "answer": "90%", "context": "90% races grandes (>25kg) a geantes", "source": "tumeurs_osseuses", "type": "curated"},
    {"question": "Quel pourcentage des motifs de consultation pour boiterie d'origine osteoarticulaire correspond a la rupture du LCCR ?", "answer": "60%", "context": "RLCCr : 60 % des motifs de consultation", "source": "rupture_lccr", "type": "curated"},
]

INCOMPLETE = (" non", " a", " de", " du", " des", " et", " ou", " la", " le", " les", " un", " une", " au", " en", " par", " sur", " avec", " sans", " mise")
GENERIC = {"objectif", "autres cas", "articulaires", "traitement", "diagnostic", "enva enva", "situé à distance", "situe a distance", "examen orthopédique orienté", "examen orthopedique oriente", "incorrecte, impactant la qualité de vie (handicap fonctionnel)"}

def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()

def extract_prompt(q):
    m = re.search(r"« (.+?) »", q["question"])
    return m.group(1) if m else q["question"]

def is_logical(q):
    qtext = q["question"]
    ans = q["answer"].strip()
    prompt = extract_prompt(q)
    pl = prompt.lower()
    al = ans.lower()

    if "enva" in qtext.lower() or "enva" in al:
        return False
    if ans.count("(") != ans.count(")"):
        return False
    if any(al.endswith(x) for x in INCOMPLETE):
        return False
    if len(ans) > 70:
        return False
    if q.get("type") == "fill":
        return False
    if q.get("type") == "percent" and "complete l affirmation" in qtext.lower():
        return False
    if pl in GENERIC or len(prompt.split()) < 3:
        return False
    if prompt.endswith("(") or prompt.endswith(",") or prompt.startswith("ou ") or prompt.startswith("l'") or prompt.startswith("situ"):
        return False
    if not (prompt[0].isupper() or prompt[0].isdigit()):
        return False
    if "a quoi correspond" in qtext.lower() and len(prompt) < 18 and q.get("type") == "relation":
        return False
    if re.search(r"[A-Za-z]{45,}", prompt):
        return False
    return True

def dedupe(items):
    seen = set()
    out = []
    for q in items:
        key = (norm(q["question"]), norm(q["answer"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(q)
    return out

raw = json.loads(IN_PATH.read_text(encoding="utf-8"))
filtered = [q for q in raw if is_logical(q)]
final = dedupe(CURATED + filtered)
OUT_PATH.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
print("Before", len(raw), "After", len(final))
from collections import Counter
print("By type", Counter(q["type"] for q in final))
print("By source", Counter(q["source"] for q in final))
