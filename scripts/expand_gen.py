from pathlib import Path
p = Path("scripts/gen_hand_checked.py")
text = p.read_text(encoding="utf-8")
extra = """
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

add_many(items, "fractures", "Citez une complication possible d'une contention externe.", [
    "Macération cutanée", "Garrot", "Oedeme des doigts", "Infection", "Decalage du pansement", "Non consolidation",
], "Complications contention externe")

add_many(items, "fractures", "Citez un critere influencant la strategie therapeutique d'une fracture.", [
    "Signalement de l'animal", "Niveau d'activite", "Morbidites associees", "Os fracture", "Schema fracturaire",
    "Fracture ouverte ou fermee", "Motivations du proprietaire", "Contraintes financieres",
], "Critères strategie therapeutique")

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

add_many(items, "tumeurs_osseuses", "Citez une race predisposee a l'osteosarcome.", [
    "Levrier Ecossais", "Leonberg", "Dogue Allemand", "Rottweiler",
], "Predisposition raciale")

add_many(items, "tumeurs_osseuses", "Citez une option de prise en charge de la douleur osseuse.", [
    "AINS", "Morphiniques", "Gabapentine", "Biphosphonates", "Radiotherapie", "Ablation thermique", "Cimentoplasties",
], "Prise en charge de la douleur")

# --- LCCR from course slides ---
items += [
    q("rupture_lccr", "Quel pourcentage des boiteries OA du membre pelvien correspond a la RLCCr au ChuvA-ENVA ?", "62%", "62% boiteries membre pelvien ChuvA-ENVA"),
    q("rupture_lccr", "Quelle est la principale cause de boiterie du membre pelvien d'origine OA chez le chien ?", "rupture du LCCr", "Principale cause RLCCr"),
    q("rupture_lccr", "Quel ligament est atteint dans la RLCCr ?", "ligament croise cranial", "Ligament croise cranial"),
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

add_many(items, "rupture_lccr", "Citez un facteur etiologique de la rupture du LCCr.", [
    "Obesite", "Sedentarisme", "Predisposition raciale", "Conformation", "Hypercorticisme", "Hypothyroïdie", "Synovite",
], "Etiologie multifactorielle LCCr")

add_many(items, "rupture_lccr", "Citez une consequence physiopathologique de la rupture du LCCr.", [
    "Arthrose", "Lésions méniscales", "Handicap fonctionnel", "Instabilite articulaire", "Synovite",
], "Consequences RLCCr")

"""
text = text.replace("# strict auto extract", extra + "# strict auto extract")
text = text.replace("if not (18 <= len(p) <= 100", "if not (15 <= len(p) <= 100")
p.write_text(text, encoding="utf-8")
print("expanded")
