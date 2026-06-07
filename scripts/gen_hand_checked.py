"""Generate 200+ hand-checked quiz questions."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from extract_content import SOURCES, SOURCE_LABELS, extract_lines, sanitize

OUT = ROOT / "src" / "data" / "questions.json"

def q(source, question, answer, context):
    return {"question": question, "answer": answer, "context": context, "source": source, "type": "curated"}


def add_multi_select(items, source, question, correct_answers, context, pool_id, wrong_pool_id=None, num_correct=2):
    items.append({
        "question": question,
        "answer": correct_answers[0],
        "context": context,
        "source": source,
        "type": "curated",
        "multiSelect": True,
        "pool_id": pool_id,
        "wrong_pool_id": wrong_pool_id,
        "_correct_pool": correct_answers,
        "num_correct": num_correct,
    })


items: list[dict] = []

# --- FRACTURES: objectifs & urgence ---
items += [
    q("fractures", "Quel objectif du traitement d'une fracture correspond a l'asepsie ?", "Absence de germes", "Absence de germes -> Asepsie"),
    q("fractures", "Quel principe correspond a la contention des fragments ?", "stabilisation", "Contention des fragments -> stabilisation"),
    q("fractures", "Quel objectif correspond a l'epargne tissulaire ?", "Respect de la vascularisation et des tissus mous", "Respect vascularisation et tissus mous -> Epargne tissulaire"),
    q("fractures", "Quel objectif therapeutique vise a supprimer la douleur ?", "Supprimer la douleur", "Objectifs du traitement"),
    q("fractures", "Quelle immobilisation en urgence pour fracture sous le coude ou le grasset chez le chien ?", "bandage de Robert Jones", "Fractures sous coude/grasset -> BRJ"),
    q("fractures", "Quelle immobilisation en urgence dans les autres cas de fracture ?", "Confinement en cage", "Autres cas -> confinement"),
    q("fractures", "Combien de temps attendre avant pose de resine apres traumatisme ?", "48 h", "Attendre 48 h apres traumatisme"),
    q("fractures", "A quelle frequence refaire un bandage sans probleme signale par le proprietaire ?", "4 a 7 jours", "Refection tous les 4 a 7 jours"),
    q("fractures", "Quel recouvrement entre tours de bande crepe dans le Robert Jones ?", "50%", "Recouvrement 50% a chaque tour"),
    q("fractures", "De combien doit depasser le matelassage en bas du pansement Robert Jones ?", "5 mm", "Matelassage depasse de 5 mm en bas"),
    q("fractures", "De combien doit depasser le matelassage en haut du pansement Robert Jones ?", "1,5 cm", "Matelassage depasse de 1,5 cm en haut"),
    q("fractures", "Quel test verifie le serrage du bandage Robert Jones en haut du pansement ?", "introduire l'index", "Introduire l'index en haut du pansement"),
    q("fractures", "Quel risque si pansement trop serre sur les doigts ?", "effet garrot", "Oedeme doigts -> effet garrot"),
    q("fractures", "Quel risque si bande trop serree sur peau humide ou lesee ?", "infection par maceration", "Infection par maceration"),
    q("fractures", "Quelle complication la plus frequente lors de la pose d'une resine ?", "serrage excessif", "Complication la plus frequente: serrage excessif"),
    q("fractures", "L'attelle doit-elle etre placee au contact de la peau ?", "non", "L'attelle n'est jamais placee au contact de la peau"),
    q("fractures", "Quand realiser le premier controle radiographique apres contention externe ?", "48 h", "Controle RX 48 h apres confection"),
    q("fractures", "Quand realiser le second controle radiographique precoce apres contention externe ?", "7 j", "Controle RX 7 j apres confection"),
    q("fractures", "A quelle frequence les radiographies de controle sont-elles ensuite realisees ?", "1 fois / 4 semaines", "Controle RX 1 fois / 4 semaines"),
    q("fractures", "Quel deplacement des fragments impose un traitement chirurgical ?", "deplacement des abouts fracturaires", "Deplacement abouts fracturaires -> chirurgie"),
]

add_multi_select(items, "fractures", "Selectionnez toutes les indications du traitement conservateur d'une fracture.", [
    "Fractures fermees", "Isolees", "Non articulaires", "Situees sous le coude et le grasset",
    "Stables apres reduction", "Contact entre surfaces fracturées > 50%", "Absence de desaxation articulaire",
], "Indications traitement conservateur", pool_id="indication_conservative", wrong_pool_id="indication_surgical", num_correct=2)

add_multi_select(items, "fractures", "Selectionnez toutes les indications du traitement chirurgical d'une fracture.", [
    "Fractures ouvertes", "Non isolees", "Articulaires", "Situees au dessus du coude et du grasset",
    "Instables apres reduction", "Contact entre surfaces fracturées < 50%", "Desaxation articulaire",
], "Indications traitement chirurgical", pool_id="indication_surgical", wrong_pool_id="indication_conservative", num_correct=2)

add_multi_select(items, "fractures", "Selectionnez toutes les forces a neutraliser pour stabiliser une fracture.", [
    "Flexion", "Compression", "Traction", "Rotation", "Cisaillement", "Angulation", "Telescopage", "Ecartement",
], "Forces a neutraliser", pool_id="force", wrong_pool_id="complication_contention", num_correct=2)

add_multi_select(items, "fractures", "Selectionnez toutes les couches du pansement de Robert Jones (theorie).", [
    "Jersey tubulaire", "Velpeau", "Coton ou Sofban", "Vetrap", "Elastoplaste",
], "Pansement Robert Jones - theorie", pool_id="bandage_layer", wrong_pool_id="material_plaster", num_correct=2)

add_multi_select(items, "fractures", "Selectionnez toutes les proprietes du platre de Paris en contention externe.", [
    "Materiau lourd", "Porosite faible", "Radio-opacite", "Permeable", "Resistance moderee et tardive (8 h)",
], "Platre de Paris", pool_id="material_plaster", wrong_pool_id="material_resin", num_correct=2)

add_multi_select(items, "fractures", "Selectionnez toutes les proprietes des resines en polyuréthane en contention externe.", [
    "Materiau leger", "Porosite elevee", "Radio-transparence", "Impermeable", "Resistance importante et precoce",
], "Resines polyuréthane", pool_id="material_resin", wrong_pool_id="material_plaster", num_correct=2)

# --- TUMEURS ---
items += [
    q("tumeurs_osseuses", "Quel pourcentage des tumeurs osseuses sont malignes chez le chien ?", "95%", "95 % malignes"),
    q("tumeurs_osseuses", "Quel pourcentage des tumeurs osseuses represente l'osteosarcome ?", "85%", "85% des tumeurs osseuses"),
    q("tumeurs_osseuses", "Quelle est l'incidence de l'osteosarcome chez le chien ?", "13.9 /100 000", "incidence 13.9 /100 000"),
    q("tumeurs_osseuses", "Quel pourcentage des tumeurs chez le chien represente l'osteosarcome ?", "5%", "5% des tumeurs chez le chien"),
    q("tumeurs_osseuses", "Quelle proportion des tumeurs osseuses primaires correspond aux osteosarcomes ?", "> 80%", "Osteosarcomes > 80%"),
    q("tumeurs_osseuses", "Quel pourcentage correspond aux chondrosarcomes ?", "10%", "Chondrosarcomes 10%"),
    q("tumeurs_osseuses", "Quelle fourchette de pourcentage correspond aux hemangiosarcomes osseux ?", "3-8%", "Hemangiosarcomes 3-8%"),
    q("tumeurs_osseuses", "Quel pourcentage des cas concerne les races grandes (>25 kg) ?", "90%", "90% races grandes"),
    q("tumeurs_osseuses", "Quel pourcentage presente des metastases au moment de la prise en charge ?", "90%", "90% metastases au diagnostic"),
    q("tumeurs_osseuses", "Quelle localisation appendiculaire typique de l'osteosarcome ?", "loin du coude, pres du grasset", "loin du coude, pres du grasset"),
    q("tumeurs_osseuses", "Quelle est la survie mediane sans traitement de l'osteosarcome ?", "1-3 mois", "Sans traitement 1-3 mois"),
    q("tumeurs_osseuses", "Quelle est la survie mediane avec amputation seule ?", "4-6 mois", "Amputation seule 4-6 mois"),
    q("tumeurs_osseuses", "Quelle est la survie mediane avec amputation et chimiotherapie adjuvante ?", "10-14 mois", "Amputation + chimio 10-14 mois"),
    q("tumeurs_osseuses", "Quel traitement de reference pour l'osteosarcome du chien ?", "amputation + chimiotherapie", "Amputation + chimio = traitement de reference"),
    q("tumeurs_osseuses", "Quelle dose de zoledronate est indiquee chez le chien ?", "0,25 mg/kg", "Zoledronate 0,25 mg/kg IV"),
    q("tumeurs_osseuses", "Quel pourcentage de metastases chez le chat atteint d'osteosarcome ?", "5-10%", "Metastases 5-10% chez le chat"),
    q("tumeurs_osseuses", "Quel traitement est utilise chez le chat atteint d'osteosarcome ?", "amputation uniquement", "Traitement par amputation uniquement"),
]

add_multi_select(items, "tumeurs_osseuses", "Selectionnez tous les facteurs pronostiques defavorables de l'osteosarcome.", [
    "Metastases pulmonaires au diagnostic", "Fracture", "Alteration de l'etat general",
    "Douleur severe rapidement evolutive", "Localisation humerale proximale",
    "Augmentation des phosphatases alcalines seriques", "Index mitotique eleve",
], "Facteurs pronostiques defavorables", pool_id="prognosis_bad", wrong_pool_id="prognosis_good", num_correct=2)

add_multi_select(items, "tumeurs_osseuses", "Selectionnez tous les facteurs pronostiques favorables de l'osteosarcome.", [
    "Traitement multimodal complet", "Bonne tolerance a la chimiotherapie", "Controle local chirurgical",
    "Atteinte du radius distal", "Atteinte de l'ulna distal", "Absence de metastases detectables",
], "Facteurs pronostiques favorables", pool_id="prognosis_good", wrong_pool_id="prognosis_bad", num_correct=2)

add_multi_select(items, "tumeurs_osseuses", "Selectionnez toutes les complications frequentes du limb-sparing.", [
    "Infection", "Reintervention", "Defaillance implant", "Conversion en amputation", "Recidive locale",
], "Complications limb-sparing", pool_id="limb_sparing_complication", wrong_pool_id="prognosis_good", num_correct=2)

# --- LCCR ---
items += [
    q("rupture_lccr", "Quel pourcentage des boiteries d'origine osteoarticulaire correspond a la rupture du LCCR ?", "60%", "RLCCr 60% motifs consultation"),
    q("rupture_lccr", "De quel ligament s'agit-il dans la rupture du LCCR ?", "ligament croise cranial", "Rupture du LCCR"),
    q("rupture_lccr", "Quel membre est le plus souvent atteint par la rupture du LCCR ?", "membre pelvien", "Atteinte preferentielle membre pelvien"),
    q("rupture_lccr", "Quel signe clinique evoque une rupture du LCCR ?", "boiterie", "Boiterie d'origine osteoarticulaire"),
    q("rupture_lccr", "Quel test clinique est utilise pour le diagnostic du LCCR ?", "tiroir cranial", "Test du tiroir cranial"),
    q("rupture_lccr", "Quelle technique chirurgicale de reference est citee pour le LCCR chez le chien de grande race ?", "TPLO", "TPLO chez grands chiens"),
    q("rupture_lccr", "Quelle technique alternative au TPLO peut etre utilisee ?", "TTA", "TTA"),
    q("rupture_lccr", "Quel examen d'imagerie confirme souvent la rupture du LCCR ?", "radiographie", "Radiographie"),
    q("rupture_lccr", "Quelle articulation est atteinte dans la rupture du LCCR ?", "genou", "Atteinte du genou"),
    q("rupture_lccr", "Quel facteur predispose a la rupture du LCCR ?", "obesite", "Obesite facteur de risque"),
]


# --- MORE FRACTURES ---
items += [
    q("fractures", "Quel traitement specifique de la douleur en urgence fracture ?", "analgésie (morphiniques), AINS", "Prise en charge douleur urgence"),
    q("fractures", "Le chat tolere-t-il bien les contentions externes ?", "non", "Chat tolere mal contentions externes"),
    q("fractures", "Faut-il porter des gants pour la pose de resine ?", "oui", "Pose resine: porter des gants"),
    q("fractures", "Quelle forme de resine est confectionnee chez les carnivores ?", "bi-valve", "Confectionner une bi-valve"),
    q("fractures", "Que doit-on laisser apparents chez le chien lors d'une resine ?", "coussinets des doigts porteurs", "Coussinets doigts porteurs apparents"),
    q("fractures", "Quelle est la consequence dramatique du serrage excessif d'une resine ?", "amputation", "Serrage excessif peut conduire a amputation"),
    q("fractures", "Par quoi debute un bandage avec attelle ?", "bandage de Robert Jones modifie", "Debut par Robert Jones modifie"),
    q("fractures", "Quelle bande cohesive maintient l'attelle en place ?", "bande cohésive", "Bande cohésive pour maintenir attelle"),
    q("fractures", "Quelle recommandation essentielle au proprietaire apres contention externe ?", "confinement de l'animal", "Confinement de l'animal"),
    q("fractures", "Quelle est la cause la plus frequente de complication du Robert Jones modifie ?", "serrage excessif", "Complication frequente serrage"),
    q("fractures", "Quels proeminences osseuses matelasser sur membre anterieur ?", "os pisiforme et extremite distale de l'ulna", "Matelassage proeminences MA"),
    q("fractures", "Quels reliefs osseux matelasser sur membre pelvien ?", "pointe du jarret et malleoles", "Matelassage jarret et malleoles"),
    q("fractures", "Combien de bandes de ouate pour le matelassage Robert Jones ?", "2", "Application de 2 bandes de ouate"),
    q("fractures", "Quand faut-il mettre une collerette avec un bandage ?", "en presence d'une plaie", "Collerette si plaie"),
    q("fractures", "Quel contact minimum entre surfaces fracturées pour traitement conservateur ?", "> 50%", "Contact > 50%"),
    q("fractures", "Quel contact maximum entre surfaces fracturées pour indication chirurgicale ?", "< 50%", "Contact < 50%"),
    q("fractures", "Les contentions externes doivent-elles inclure l'articulation proximale a la fracture ?", "oui", "Doit inclure articulation proximale"),
]

add_multi_select(items, "fractures", "Selectionnez toutes les complications possibles d'une contention externe.", [
    "Macération cutanée", "Garrot", "Oedeme des doigts", "Infection", "Decalage du pansement", "Non consolidation",
], "Complications contention externe", pool_id="complication_contention", wrong_pool_id="force", num_correct=2)

add_multi_select(items, "fractures", "Selectionnez tous les criteres influencant la strategie therapeutique d'une fracture.", [
    "Signalement de l'animal", "Niveau d'activite", "Morbidites associees", "Age de l'animal", "Schema fracturaire",
    "Fracture ouverte ou fermee", "Motivations du proprietaire", "Contraintes financieres",
], "Critères strategie therapeutique", pool_id="strategy_criterion", wrong_pool_id="indication_surgical", num_correct=2)

# --- MORE TUMEURS ---
items += [
    q("tumeurs_osseuses", "Quelle est la frequence approximative d'un resultat fonctionnel satisfaisant apres amputation ?", "75-90%", "Resultat fonctionnel satisfaisant ~75-90%"),
    q("tumeurs_osseuses", "Quelle frequence de recidive locale apres limb-sparing ?", "10-25%", "Recidive locale ~10-25%"),
    q("tumeurs_osseuses", "Quelle frequence d'infection apres limb-sparing ?", "20-60%", "Infection ~20-60%"),
    q("tumeurs_osseuses", "Quelle frequence de conversion en amputation apres limb-sparing ?", "15-35%", "Conversion amputation ~15-35%"),
    q("tumeurs_osseuses", "Quelle frequence d'amelioration antalgique avec radiotherapie palliative ?", "70-90%", "Amelioration antalgique ~70-90%"),
    q("tumeurs_osseuses", "Quelle frequence de fracture pathologique malgre radiotherapie ?", "15-35%", "Fracture pathologique ~15-35%"),
    q("tumeurs_osseuses", "Quelle proportion de survies longues a 2 ans ?", "15-20%", "Survies longues ~15-20% a 2 ans"),
    q("tumeurs_osseuses", "Quelle proportion de survie a 2 ans avec chimio adjuvante ?", "< 25%", "Moins de 25% a 2 ans"),
    q("tumeurs_osseuses", "Quelle localisation osseuse preferentielle de la tumeur ?", "zones de croissance (metaphyses)", "Localisation metaphysaire"),
    q("tumeurs_osseuses", "Quelle dissémination metastatique est la plus frequente ?", "pulmonaire", "Dissémination principalement pulmonaire"),
    q("tumeurs_osseuses", "Quel signe clinique majeur evoque un osteosarcome ?", "boiterie douloureuse persistante", "Boiterie douloureuse persistante"),
    q("tumeurs_osseuses", "Quelle alteration biologique est un mauvais pronostic independant ?", "phosphatases alcalines seriques elevees", "Phosphatases alcalines elevees"),
]

add_multi_select(items, "tumeurs_osseuses", "Selectionnez toutes les races predisposees a l'osteosarcome.", [
    "Levrier Ecossais", "Leonberg", "Dogue Allemand", "Rottweiler",
], "Predisposition raciale", pool_id="breed", wrong_pool_id="prognosis_bad", num_correct=2)

add_multi_select(items, "tumeurs_osseuses", "Selectionnez toutes les options de prise en charge de la douleur osseuse.", [
    "AINS", "Morphiniques", "Gabapentine", "Biphosphonates", "Radiotherapie", "Ablation thermique", "Cimentoplasties",
], "Prise en charge de la douleur", pool_id="pain_option", wrong_pool_id="prognosis_bad", num_correct=2)

# --- LCCR from course slides ---
items += [
    q("rupture_lccr", "Quel pourcentage des boiteries OA du membre pelvien correspond a la RLCCr au ChuvA-ENVA ?", "62%", "62% boiteries membre pelvien ChuvA-ENVA"),
    q("rupture_lccr", "Quelle est la principale cause de boiterie du membre pelvien d'origine OA chez le chien ?", "rupture du LCCr", "Principale cause RLCCr"),
    q("rupture_lccr", "Quel mouvement le LCCr limite-t-il principalement ?", "glissement cranial du tibia", "Limite glissement cranial du tibia"),
    q("rupture_lccr", "Quel autre mouvement le LCCr limite-t-il ?", "rotation interne du tibia", "Controle rotation interne du tibia"),
    q("rupture_lccr", "Quel mouvement articulaire le LCCr limite-t-il ?", "hyperextension", "Limite hyperextension"),
    q("rupture_lccr", "Quel pourcentage de lésions méniscales accompagne une rupture du LCCr ?", "50%", "Lésions méniscales dans 50% des cas"),
    q("rupture_lccr", "Quel ménisque est particulierement atteint ?", "ménisque médial", "Ménisque médial en particulier"),
    q("rupture_lccr", "Quel pourcentage de rupture controlaterale décalée dans le temps ?", "50%", "Rupture controlaterale 50% des cas"),
    q("rupture_lccr", "Quelle pente tibiale est un facteur de risque ?", "> 30°", "Pente tibiale > 30°"),
    q("rupture_lccr", "Quelle est l'etiologie dominante de la rupture du LCCr ?", "degenerescence ligamentaire", "Degenerescence ligamentaire"),
    q("rupture_lccr", "La rupture traumatique isolée est-elle frequente ?", "non", "Traumatique rarement cause isolee"),
    q("rupture_lccr", "Existe-t-il une cicatrisation spontanée du LCCr ?", "non", "Absence de cicatrisation spontanée"),
    q("rupture_lccr", "Quel pourcentage de ruptures apres reparation par suture isolee ?", "90%", "Reparation suture isolee -> 90% ruptures"),
    q("rupture_lccr", "Quelles instabilités suivent la rupture du LCCr ?", "tiroir anterieur et rotatoire", "Instabilites tiroir anterieur et rotatoire"),
    q("rupture_lccr", "Quels sont les deux enjeux majeurs du traitement du LCCr ?", "stabilité articulaire et limiter l'arthrose", "Stabilite + limiter arthrose"),
    q("rupture_lccr", "Quel type de boiterie est prototypique d'une rupture complete du LCCr ?", "boiterie de soutien", "Boiterie de soutien"),
    q("rupture_lccr", "Quelle prise en charge est systematique pour la RLCCr chez le chien ?", "chirurgicale", "Prise en charge chirurgicale systematique"),
    q("rupture_lccr", "La RLCCr est-elle un modele de pathologie spontanee chez l'homme ?", "oui", "Modele pathologie spontanee homme"),
    q("rupture_lccr", "Quel coût annuel USA est cite pour la prise en charge RLCCr (2003) ?", "1 milliard $", "Cout 1 milliard $ USA 2003"),
]

add_multi_select(items, "rupture_lccr", "Selectionnez tous les facteurs etiologiques de la rupture du LCCr.", [
    "Obesite", "Sedentarisme", "Predisposition raciale", "Conformation", "Hypercorticisme", "Hypothyroïdie", "Synovite",
], "Etiologie multifactorielle LCCr", pool_id="lccr_etiology", wrong_pool_id="lccr_consequence", num_correct=2)

add_multi_select(items, "rupture_lccr", "Selectionnez toutes les consequences physiopathologiques de la rupture du LCCr.", [
    "Arthrose", "Lésions méniscales", "Handicap fonctionnel", "Instabilite articulaire", "Synovite",
], "Consequences RLCCr", pool_id="lccr_consequence", wrong_pool_id="lccr_etiology", num_correct=2)

# Auto-extract disabled: PDF pairings produced illogical questions.

seen=set(); final=[]
for item in items:
    key=item['question'].lower()
    if key in seen:
        continue
    seen.add(key)
    final.append(item)

from add_mcq_choices import add_choices
final = add_choices(final)
OUT.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding='utf-8')
from collections import Counter
print('Total', len(final))
print('By source', Counter(x['source'] for x in final))

