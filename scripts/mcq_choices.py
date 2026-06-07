"""Generate plausible same-domain MCQ distractors with strict semantic categories."""
from __future__ import annotations

import random
import re
import unicodedata
from typing import Iterable

STOPWORDS = {
    "citer", "citez", "quel", "quelle", "quels", "quelles", "une", "des", "les", "du", "de", "la", "le",
    "dans", "pour", "avec", "sans", "chez", "est", "sont", "par", "sur", "apres", "avant", "entre",
    "objectif", "objectifs", "apprentissage", "cours", "traitement", "fracture", "fractures",
}

MOVEMENT_TERMS = (
    "rotation", "glissement", "hyperextension", "flexion", "extension", "tibia", "femur", "femur",
    "abduction", "adduction", "valgus", "varus", "tiroir anterieur", "tiroir rotatoire", "angula",
    "telescopage", "ecartement", "compression", "traction", "cisaillement",
)
CLINICAL_TEST_TERMS = ("tiroir", "test", "manoeuvre", "introduire l'index", "palpation", "lachman", "compression du grasset")
TECHNIQUE_TERMS = ("stabilite articulaire", "limiter l'arthrose", "tplo", "tta", "osteotom", "extra-articul", "suture", "fixation", "chirurg", "technique", "limb-sparing")
IMAGING_TERMS = ("radiograph", "scanner", "echograph", "irm", "tomodensit", "scintigraph", "imagerie", "arthroscop")
PROCEDURE_TERMS = ("bandage", "attelle", "resine", "platre", "confinement", "robert jones", "velpeau", "vetrap", "immobil")
SIGN_TERMS = ("boiterie", "douleur", "signe", "synovite", "handicap", "instabilite", "arthrose", "oedeme")
FACTOR_TERMS = ("obesite", "conformation", "sedentarisme", "hypothyroid", "hypercortic", "predisposition", "genetique")
TREATMENT_TERMS = ("amputation", "chimiotherapie", "zoledronate", "radiotherap", "traitement", "surveillance")
CONSEQUENCE_TERMS = ("arthrose", "meniscal", "meniscale", "handicap", "instabilite", "synovite", "lesion", "lésion")
ANATOMY_BONE_TERMS = ("os ", "pisiforme", "jarret", "malleole", "olecrane", "tuberosite", "processus", "relief", "prominence", "extremite distale")


ANSWER_POOLS: dict[str, list[str]] = {
    "indication_conservative": [
        "Fractures fermees", "Isolees", "Non articulaires", "Situees sous le coude et le grasset",
        "Stables apres reduction", "Contact entre surfaces fracturées > 50%", "Absence de desaxation articulaire",
    ],
    "indication_surgical": [
        "Fractures ouvertes", "Non isolees", "Articulaires", "Situees au dessus du coude et du grasset",
        "Instables apres reduction", "Contact entre surfaces fracturées < 50%", "Desaxation articulaire",
    ],
    "force": ["Flexion", "Compression", "Traction", "Rotation", "Cisaillement", "Angulation", "Telescopage", "Ecartement"],
    "bandage_layer": ["Jersey tubulaire", "Velpeau", "Coton ou Sofban", "Vetrap", "Elastoplaste"],
    "material_plaster": ["Materiau lourd", "Porosite faible", "Radio-opacite", "Permeable", "Resistance moderee et tardive (8 h)"],
    "material_resin": ["Materiau leger", "Porosite elevee", "Radio-transparence", "Impermeable", "Resistance importante et precoce"],
    "complication_contention": ["Macération cutanée", "Garrot", "Oedeme des doigts", "Infection", "Decalage du pansement", "Non consolidation"],
    "strategy_criterion": [
        "Signalement de l'animal", "Niveau d'activite", "Morbidites associees", "Age de l'animal", "Schema fracturaire",
        "Fracture ouverte ou fermee", "Motivations du proprietaire", "Contraintes financieres",
    ],
    "prognosis_bad": [
        "Metastases pulmonaires au diagnostic", "Fracture", "Alteration de l'etat general",
        "Douleur severe rapidement evolutive", "Localisation humerale proximale",
        "Augmentation des phosphatases alcalines seriques", "Index mitotique eleve",
    ],
    "prognosis_good": [
        "Traitement multimodal complet", "Bonne tolerance a la chimiotherapie", "Controle local chirurgical",
        "Atteinte du radius distal", "Atteinte de l'ulna distal", "Absence de metastases detectables",
    ],
    "limb_sparing_complication": ["Infection", "Reintervention", "Defaillance implant", "Conversion en amputation", "Recidive locale"],
    "breed": ["Levrier Ecossais", "Leonberg", "Dogue Allemand", "Rottweiler"],
    "pain_option": ["AINS", "Morphiniques", "Gabapentine", "Biphosphonates", "Radiotherapie", "Ablation thermique", "Cimentoplasties"],
    "lccr_etiology": ["Obesite", "Sedentarisme", "Predisposition raciale", "Conformation", "Hypercorticisme", "Hypothyroïdie", "Synovite"],
    "lccr_consequence": ["Arthrose", "Lésions méniscales", "Handicap fonctionnel", "Instabilite articulaire", "Synovite"],
}

OPPOSITE_POOLS: dict[str, str] = {
    "indication_conservative": "indication_surgical",
    "indication_surgical": "indication_conservative",
    "material_plaster": "material_resin",
    "material_resin": "material_plaster",
    "prognosis_bad": "prognosis_good",
    "prognosis_good": "prognosis_bad",
}


def build_multi_select_choices(
    correct_pool: list[str],
    wrong_pool: list[str],
    num_correct: int,
    seed: int,
) -> tuple[list[str], list[str]]:
    rng = random.Random(seed)
    pool = list(dict.fromkeys(correct_pool))
    wrong = [item for item in wrong_pool if answer_key(item) not in {answer_key(x) for x in pool}]
    pick_correct = min(num_correct, len(pool))
    if pick_correct < 1:
        raise ValueError("Multi-select needs at least one correct answer")
    correct = rng.sample(pool, pick_correct)
    correct_keys = {answer_key(item) for item in correct}
    wrong_unique: list[str] = []
    seen_wrong = set()
    for candidate in wrong:
        key = answer_key(candidate)
        if key in correct_keys or key in seen_wrong:
            continue
        wrong_unique.append(candidate)
        seen_wrong.add(key)
    rng.shuffle(wrong_unique)
    need_wrong = 4 - len(correct)
    if len(wrong_unique) < need_wrong:
        for candidate in pool:
            if len(wrong_unique) >= need_wrong:
                break
            key = answer_key(candidate)
            if key in correct_keys or key in seen_wrong:
                continue
            wrong_unique.append(candidate)
            seen_wrong.add(key)
    choices = correct + wrong_unique[:need_wrong]
    if len(choices) < 4:
        raise ValueError("Could not build 4 multi-select choices")
    rng.shuffle(choices)
    return choices[:4], correct



CURATED: dict[str, dict[str, list[str]]] = {
    "fractures": {
        "movement": ["Flexion", "Compression", "Traction", "Rotation", "Angulation", "Telescopage", "Ecartement", "Cisaillement"],
        "procedure": ["bandage de Robert Jones", "Confinement en cage", "bandage de Robert Jones modifie", "Velpeau", "Vetrap", "Elastoplaste"],
        "clinical_test": ["introduire l'index", "compression du grasset", "mobilisation passive", "verification du serrage distal", "mobilisation des doigts"],
        "concept": ["stabilisation", "Absence de germes", "Supprimer la douleur", "Non consolidation", "effet garrot"],
        "percent": ["50%", "< 50%", "> 50%", "Contact entre surfaces fracturees > 50%", "Contact entre surfaces fracturees < 50%"],
        "duration": ["48 h", "7 j", "4 a 7 jours", "1 fois / 4 semaines"],
        "measure": ["5 mm", "1,5 cm", "2 cm", "3 mm"],
        "count": ["1", "2", "3", "4"],
        "anatomy_bone": [
            "os pisiforme et extremite distale de l'ulna",
            "pointe du jarret et malleoles",
            "tuberosite du radius et olecrane",
            "processus styloide du radius et olecrane",
        ],
        "list_item": ["Fractures fermees", "Fractures ouvertes", "Non articulaires", "Articulaires", "Situees sous le coude et le grasset"],
    },
    "tumeurs_osseuses": {
        "percent": ["95%", "85%", "90%", "10%", "5%", "3-8%", "5-10%", "> 80%", "< 25%"],
        "duration": ["1-3 mois", "4-6 mois", "10-14 mois"],
        "dose": ["0,25 mg/kg", "0,5 mg/kg", "0,1 mg/kg"],
        "treatment": ["amputation + chimiotherapie", "amputation uniquement", "Radiotherapie", "Ablation thermique", "Biphosphonates"],
        "concept": ["Metastases pulmonaires au diagnostic", "Fracture pathologique", "Index mitotique eleve", "Controle local chirurgical"],
        "list_item": ["Infection", "Reintervention", "Defaillance implant", "Recidive locale", "Conversion en amputation"],
    },
    "rupture_lccr": {
        "movement": ["glissement cranial du tibia", "rotation interne du tibia", "hyperextension", "tiroir anterieur et rotatoire"],
        "clinical_test": ["tiroir cranial", "tiroir anterieur et rotatoire", "compression du grasset", "test de Tibial thrust"],
        "technique": ["TPLO", "TTA", "technique extra-articulaire", "stabilite articulaire et limiter l'arthrose"],
        "imaging": ["radiographie", "scanner", "echographie", "IRM"],
        "percent": ["50%", "62%", "60%", "90%", "90% de ruptures"],
        "angle": ["> 30°", "< 15°", "20-25°", "35-40°", "45°"],
        "sign": ["boiterie", "Instabilite articulaire", "Arthrose", "Handicap fonctionnel", "boiterie de soutien"],
        "consequence": ["Arthrose", "Lesions meniscales", "Lésions méniscales", "Handicap fonctionnel", "Instabilite articulaire", "Synovite"],
        "factor": ["obesite", "Conformation", "Sedentarisme", "Hypothyroïdie", "Hypercorticisme", "Predisposition raciale"],
        "anatomy": ["ligament croise cranial", "menisque medial", "Lesions meniscales", "genou", "membre pelvien"],
        "anatomy_bone": ["echancrure femorale etroite", "pente tibiale moderee", "conformation valgus du grasset"],
        "cost": ["1 milliard $", "6 milliards $", "500 millions $", "2 milliards $"],
        "concept": ["degenerescence ligamentaire", "rupture du LCCr", "Synovite", "boiterie de soutien"],
        "treatment_goal": [
            "stabilite articulaire et limiter l'arthrose",
            "restaurer la fonction meniscale",
            "eviter toute chirurgie invasive",
            "immobilisation platre prolongee",
        ],
    },
}

YESNO_WRONG: dict[str, list[str]] = {
    "fractures": [
        "oui",
        "non",
        "Uniquement pour les fractures ouvertes",
        "Jamais en pratique courante",
        "Seulement au contact direct de la peau",
        "Toujours au-dessus du coude",
        "Reserve aux chats uniquement",
    ],
    "tumeurs_osseuses": [
        "oui",
        "non",
        "Dans moins de 10% des cas",
        "Systematique apres amputation",
        "Uniquement chez le chat",
    ],
    "rupture_lccr": [
        "oui",
        "non",
        "Dans la majorite des cas isoles",
        "Plus frequente que la degenerescence",
        "Observee dans plus de 50% des traumatismes",
        "Tres rare, quasi exceptionnelle",
        "Systematique apres entorse benigne",
    ],
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def answer_key(text: str) -> str:
    normalized = unicodedata.normalize("NFD", norm(text))
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-zàâäéèêëïîôùûüç0-9°$]+", norm(text)) if len(t) > 2 and t not in STOPWORDS}


def answer_kind(text: str) -> str:
    value = norm(text)
    if value in {"non", "oui"}:
        return "yesno"
    if re.search(r"\d", text):
        if "$" in text or "milliard" in value or "million" in value:
            return "cost"
        if "%" in text:
            return "percent"
        if "°" in text:
            return "angle"
        if re.search(r"\b(h|j|sem|semaine|semaines|mois|jour|jours|heure|heures)\b", value):
            return "duration"
        if re.search(r"mg/kg|mg|ml/kg", value):
            return "dose"
        if "/100" in text or re.search(r"\d+\s*/\s*\d+", text):
            return "rate"
        if re.search(r"\d+\s*-\s*\d+", text):
            return "range"
        if re.search(r"\d+\s*(fois|mm|cm)", value):
            return "measure"
        if len(value) <= 2:
            return "count"
        return "number"
    if len(text.split()) <= 4:
        return "short"
    if len(text.split()) <= 10:
        return "medium"
    return "long"


def classify_answer(text: str) -> set[str]:
    value = norm(text)
    categories: set[str] = set()
    if any(term in value for term in MOVEMENT_TERMS):
        categories.add("movement")
    if any(term in value for term in CLINICAL_TEST_TERMS):
        categories.add("clinical_test")
    if any(term in value for term in TECHNIQUE_TERMS):
        categories.add("technique")
    if any(term in value for term in IMAGING_TERMS):
        categories.add("imaging")
    if any(term in value for term in PROCEDURE_TERMS):
        categories.add("procedure")
    if any(term in value for term in SIGN_TERMS):
        categories.add("sign")
    if any(term in value for term in CONSEQUENCE_TERMS):
        categories.add("consequence")
    if any(term in value for term in FACTOR_TERMS):
        categories.add("factor")
    if any(term in value for term in TREATMENT_TERMS):
        categories.add("treatment")
    if any(term in value for term in ANATOMY_BONE_TERMS):
        categories.add("anatomy_bone")

    kind = answer_kind(text)
    if kind == "angle":
        categories.add("angle")
    if kind == "cost":
        categories.add("cost")
    if kind == "count":
        categories.add("count")
    if kind == "percent":
        categories.add("percent")
    elif kind in {"duration", "range"} or "fois /" in value:
        categories.add("duration")
    elif kind in {"measure", "dose", "rate", "number"}:
        categories.add("measure" if kind == "measure" else kind)
    elif kind == "yesno":
        categories.add("yesno")
    elif "citez" not in value and len(text.split()) <= 6:
        categories.add("concept")
    else:
        categories.add("list_item")
    return categories


def required_category(question: str, answer: str) -> str:
    q = norm(question)

    rules: list[tuple[str, str]] = [
        (r"est-elle|est-il|existe-t|doivent-elles|faut-il|doit-elle|doit-il|tolere-t|porte-t", "yesno"),
        (r"proeminence|relief osseux|matelasser.*membre|prominence osseuse", "anatomy_bone"),
        (r"pente|inclinaison|\bangle\b|echancrure", "angle"),
        (r"cout|coût|milliard|million", "cost"),
        (r"mouvement", "movement"),
        (r"quel test|test (clinique|du|de|verifie)", "clinical_test"),
        (r"technique (chirurgicale|alternative)|alternative au tplo|tplo|tta", "technique"),
        (r"examen d.?imagerie|imagerie confirme|quel examen", "imaging"),
        (r"enjeux|objectifs majeurs", "treatment_goal"),
        (r"pourcent|proportion|recouvrement", "percent"),
        (r"combien de bandes|combien.*ouate", "count"),
        (r"combien|frequence|temps|delai|attendre|duree|quand realiser", "duration"),
        (r"\b(mm|cm)\b|depasse|recouvrement entre", "measure"),
        (r"immobilisation|bandage|attelle|resine|platre|confinement|pansement", "procedure"),
        (r"consequence physiopatholog", "consequence"),
        (r"critere.*strategie|strategie therapeutique", "strategy_criterion"),
        (r"citez|cite ", "list_item"),
        (r"force a neutraliser|couche du pansement|propriete", "list_item"),
        (r"facteur|predispose|etiolog", "factor"),
        (r"signe|sympt|boiterie", "sign"),
        (r"traitement|therap|chimiotherap|amputation", "treatment"),
        (r"ligament|menisque|articulation", "anatomy"),
        (r"objectif", "concept"),
    ]
    for pattern, category in rules:
        if re.search(pattern, q):
            return category

    a_cats = classify_answer(answer)
    for cat in ("movement", "angle", "cost", "count", "percent", "duration", "measure", "clinical_test", "technique", "imaging", "anatomy_bone", "procedure"):
        if cat in a_cats:
            return cat
    if answer_kind(answer) in {"short", "medium"}:
        return "concept"
    return "list_item"


def fits_category(text: str, category: str) -> bool:
    return category in classify_answer(text)


def score_candidate(correct: str, candidate: str, question: str, category: str) -> float:
    if norm(candidate) == norm(correct):
        return -1.0
    if not fits_category(candidate, category):
        return -1.0

    score = 0.0
    score += len(tokens(question) & tokens(candidate)) * 12.0
    score += len(tokens(correct) & tokens(candidate)) * 8.0
    score -= abs(len(candidate) - len(correct)) * 0.06
    if category == answer_kind(correct) or category in classify_answer(candidate):
        score += 20.0
    return score


def category_pool(source: str, category: str, source_answers: Iterable[str], correct: str) -> list[str]:
    pool: list[str] = []
    seen = {norm(correct)}
    for candidate in source_answers:
        key = answer_key(candidate)
        if key in seen:
            continue
        if fits_category(candidate, category):
            pool.append(candidate)
            seen.add(key)
    for candidate in CURATED.get(source, {}).get(category, []):
        key = answer_key(candidate)
        if key in seen:
            continue
        pool.append(candidate)
        seen.add(key)
    return pool


def pick_yesno_distractors(correct: str, source: str, seed: int) -> list[str]:
    rng = random.Random(seed)
    opposite = "oui" if norm(correct) == "non" else "non"
    pool = [c for c in YESNO_WRONG.get(source, ["oui", "non"]) if norm(c) != norm(correct)]
    rng.shuffle(pool)
    distractors = [opposite]
    for candidate in pool:
        if len(distractors) >= 3:
            break
        if candidate not in distractors and norm(candidate) != norm(correct):
            distractors.append(candidate)
    return distractors[:3]


def pick_distractors(correct: str, question: str, source: str, source_answers: Iterable[str], preset: list[str] | None, seed: int, strict_pool: bool = False) -> list[str]:
    category = required_category(question, correct)
    if strict_pool:
        pool = [candidate for candidate in source_answers if answer_key(candidate) != answer_key(correct)]
        rng = random.Random(seed)
        rng.shuffle(pool)
        return pool[:3]
    if category == "yesno":
        return pick_yesno_distractors(correct, source, seed)

    pool = category_pool(source, category, source_answers, correct)
    rng = random.Random(seed)

    ranked = [(score_candidate(correct, c, question, category), c) for c in (preset or []) + pool]
    ranked = [(s, c) for s, c in ranked if s >= 0]
    ranked.sort(key=lambda item: item[0], reverse=True)

    distractors: list[str] = []
    for _, candidate in ranked:
        if len(distractors) >= 3:
            break
        if candidate not in distractors:
            distractors.append(candidate)

    if len(distractors) < 3:
        extras = [c for c in pool if c not in distractors and norm(c) != norm(correct)]
        rng.shuffle(extras)
        for candidate in extras:
            if len(distractors) >= 3:
                break
            distractors.append(candidate)

    if len(distractors) < 3:
        for candidate in CURATED.get(source, {}).get(category, []):
            if len(distractors) >= 3:
                break
            if candidate not in distractors and norm(candidate) != norm(correct):
                distractors.append(candidate)

    return distractors[:3]


def ensure_four_unique_choices(correct: str, distractors: list[str], source: str, question: str, seed: int, source_answers: list[str] | None = None) -> list[str]:
    rng = random.Random(seed)
    category = required_category(question, correct)
    unique: list[str] = []
    seen = set()
    for item in distractors + [correct]:
        key = answer_key(item)
        if key in seen:
            continue
        unique.append(item)
        seen.add(key)

    if len(unique) < 4:
        filler_pool = category_pool(source, category, [], correct)
        filler_pool += CURATED.get(source, {}).get(category, [])
        if category == "yesno":
            filler_pool += YESNO_WRONG.get(source, ["oui", "non"])
        rng.shuffle(filler_pool)
        for candidate in filler_pool:
            if len(unique) >= 4:
                break
            key = answer_key(candidate)
            if key not in seen:
                unique.append(candidate)
                seen.add(key)

    if len(unique) < 4 and source_answers:
        rng.shuffle(source_answers)
        for candidate in source_answers:
            if len(unique) >= 4:
                break
            key = answer_key(candidate)
            if key not in seen:
                unique.append(candidate)
                seen.add(key)

    if len(unique) < 4:
        raise ValueError(f"Could not build 4 choices for: {question[:80]}")

    rng.shuffle(unique)
    return unique[:4]


def add_choices(questions: list[dict]) -> list[dict]:
    by_source: dict[str, list[str]] = {}
    for question in questions:
        answers = question.get("answers") or [question["answer"]]
        for value in answers:
            by_source.setdefault(question["source"], []).append(value)

    for question in questions:
        source = question["source"]
        seed = hash(question["question"] + question.get("pool_id", "")) & 0xFFFFFFFF
        if question.get("_distractors") and len(str(question.get("answer", ""))) <= 3 and str(question.get("answer", "")).upper() in {"A", "B", "A+", "B+"}:
            correct = question["answer"]
            distractors = list(question.pop("_distractors", []))
            extras = ["A", "B", "A+", "B+"]
            for extra in extras:
                if len(distractors) >= 3:
                    break
                if extra != correct and extra not in distractors:
                    distractors.append(extra)
            question["choices"] = ensure_four_unique_choices(correct, distractors[:3], source, question["question"], seed, extras)
            question.pop("pool_id", None)
            continue

        if question.get("multiSelect"):
            pool_id = question.get("pool_id")
            correct_pool = question.get("_correct_pool") or (ANSWER_POOLS.get(pool_id, []) if pool_id else [])
            wrong_pool_id = question.get("wrong_pool_id") or (OPPOSITE_POOLS.get(pool_id or "", "") if pool_id else "")
            wrong_pool = list(question.get("_wrong_pool") or [])
            if wrong_pool_id and wrong_pool_id in ANSWER_POOLS:
                wrong_pool += ANSWER_POOLS[wrong_pool_id]
            if not wrong_pool:
                wrong_pool = [a for a in by_source.get(source, []) if answer_key(a) not in {answer_key(x) for x in correct_pool}]
            num_correct = min(question.get("num_correct", 2), len(correct_pool))
            choices, correct = build_multi_select_choices(correct_pool, wrong_pool, num_correct, seed)
            question["choices"] = choices
            question["answers"] = correct
            question["answer"] = correct[0]
            question.pop("_correct_pool", None)
            question.pop("_wrong_pool", None)
            question.pop("wrong_pool_id", None)
            question.pop("num_correct", None)
            question.pop("pool_id", None)
            continue

        correct = question["answer"]
        preset = question.pop("_distractors", None)
        seed = hash(question["question"] + correct) & 0xFFFFFFFF
        pool_id = question.get("pool_id")
        answer_pool = ANSWER_POOLS[pool_id] if pool_id and pool_id in ANSWER_POOLS else by_source.get(source, [])
        strict = bool(pool_id and pool_id in ANSWER_POOLS)
        distractors = pick_distractors(correct, question["question"], source, answer_pool, preset, seed, strict_pool=strict)
        question["choices"] = ensure_four_unique_choices(correct, distractors, source, question["question"], seed, answer_pool if strict else by_source.get(source, []))
        question.pop("pool_id", None)

    return questions

