"""Maps an ingredient name (any of FR/EN/AR) to a canonical icon key.

The canonical key is the icon filename stem you keep in the library
(built-in app/ingredient_icons/ or user /data/icons), e.g. "garlic" -> garlic.png.

To extend: add aliases to ALIASES, or drop matching-named icon files in the
library. Matching is case-insensitive and accent-insensitive for latin text.
You can also add your own aliases at runtime via the Ingredient Icons page
(future), or by editing this file and pushing to GitHub.
"""
import unicodedata

# canonical_key: [list of names in any language that mean the same ingredient]
ALIASES = {
    "garlic":      ["garlic", "ail", "ثوم", "الثوم", "fص ثوم", "gousse d'ail", "gousses d'ail"],
    "onion":       ["onion", "onions", "oignon", "oignons", "بصل", "البصل"],
    "tomato":      ["tomato", "tomatoes", "tomate", "tomates", "طماطم", "البندورة", "بندورة"],
    "potato":      ["potato", "potatoes", "pomme de terre", "pommes de terre", "بطاطا", "بطاطس"],
    "egg":         ["egg", "eggs", "oeuf", "œuf", "oeufs", "œufs", "بيض", "بيضة"],
    "flour":       ["flour", "farine", "farine de ble", "farine de blé", "طحين", "دقيق"],
    "salt":        ["salt", "sel", "ملح"],
    "pepper":      ["pepper", "black pepper", "poivre", "poivre moulu", "فلفل", "فلفل أسود"],
    "sugar":       ["sugar", "sucre", "sucre en poudre", "سكر"],
    "milk":        ["milk", "lait", "حليب", "لبن"],
    "butter":      ["butter", "beurre", "زبدة"],
    "olive_oil":   ["olive oil", "huile d'olive", "زيت زيتون", "زيت الزيتون"],
    "oil":         ["oil", "huile", "huile de friture", "زيت"],
    "water":       ["water", "eau", "ماء", "ماء بارد"],
    "carrot":      ["carrot", "carrots", "carotte", "carottes", "جزر"],
    "chicken":     ["chicken", "poulet", "دجاج", "فراخ"],
    "beef":        ["beef", "boeuf", "bœuf", "لحم بقر", "لحم"],
    "lamb":        ["lamb", "agneau", "لحم خروف", "خروف"],
    "fish":        ["fish", "poisson", "سمك"],
    "rice":        ["rice", "riz", "أرز", "رز"],
    "pasta":       ["pasta", "pates", "pâtes", "معكرونة", "مكرونة"],
    "lentils":     ["lentils", "lentille", "lentilles", "lentilles vertes", "عدس"],
    "chickpeas":   ["chickpeas", "pois chiches", "حمص"],
    "parsley":     ["parsley", "persil", "بقدونس", "معدنوس"],
    "cilantro":    ["cilantro", "coriander", "coriandre", "كزبرة", "قزبر"],
    "mint":        ["mint", "menthe", "نعناع"],
    "thyme":       ["thyme", "thym", "زعتر"],
    "rosemary":    ["rosemary", "romarin", "إكليل الجبل", "روزماري"],
    "marjoram":    ["marjoram", "marjolaine", "مردقوش", "بردقوش"],
    "cumin":       ["cumin", "كمون"],
    "paprika":     ["paprika", "paprika doux", "بابريكا", "فلفل أحمر حلو"],
    "ginger":      ["ginger", "gingembre", "زنجبيل"],
    "cinnamon":    ["cinnamon", "cannelle", "قرفة"],
    "saffron":     ["saffron", "safran", "زعفران"],
    "lemon":       ["lemon", "citron", "ليمون", "حامض"],
    "cheese":      ["cheese", "fromage", "جبن", "جبنة"],
    "yogurt":      ["yogurt", "yoghurt", "yaourt", "لبن زبادي", "زبادي", "رايب"],
    "bread":       ["bread", "pain", "خبز"],
    "honey":       ["honey", "miel", "عسل"],
    "cucumber":    ["cucumber", "concombre", "خيار"],
    "eggplant":    ["eggplant", "aubergine", "باذنجان", "بادنجان"],
    "zucchini":    ["zucchini", "courgette", "كوسة", "كوسا"],
    "bell_pepper": ["bell pepper", "poivron", "فلفل حلو", "فليفلة"],
    "chili":       ["chili", "chilli", "piment", "فلفل حار", "هريسة"],
}


def _norm(s: str) -> str:
    """Lowercase, strip accents, collapse spaces — for latin matching.
    Arabic is left mostly as-is (just stripped/lowered)."""
    s = (s or "").strip().lower()
    # strip latin accents but keep arabic
    out = []
    for ch in unicodedata.normalize("NFD", s):
        if unicodedata.category(ch) == "Mn" and ord(ch) < 0x600:
            continue  # drop latin combining marks, keep arabic marks
        out.append(ch)
    s = "".join(out)
    s = s.replace("'", " ").replace("’", " ")
    s = " ".join(s.split())
    return s


# Precompute a reverse lookup: normalized alias -> canonical key
_LOOKUP = {}
for _key, _names in ALIASES.items():
    _LOOKUP[_norm(_key)] = _key
    for _n in _names:
        _LOOKUP[_norm(_n)] = _key


def canonical_key(name: str) -> str:
    """Return the canonical icon key for an ingredient name, or ''."""
    n = _norm(name)
    if not n:
        return ""
    if n in _LOOKUP:
        return _LOOKUP[n]
    # try last word (e.g. "de romarin frais" -> "romarin"? -> handle 'frais' tail)
    words = n.split()
    # try progressively shorter trailing/leading combos
    for w in words:
        if w in _LOOKUP:
            return _LOOKUP[w]
    return ""
