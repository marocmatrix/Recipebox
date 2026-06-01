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
    "tuna":        ["tuna", "thon", "تونة", "تونا"],
    "corn":        ["corn", "maize", "maïs", "mais", "ذرة"],
    "peas":        ["peas", "petits pois", "pois", "بازلاء", "بزاليا"],
    "green_beans": ["green beans", "haricots verts", "فاصوليا خضراء", "لوبيا"],
    "mushroom":    ["mushroom", "mushrooms", "champignon", "champignons", "فطر", "مشروم"],
    "spinach":     ["spinach", "épinard", "épinards", "epinards", "سبانخ"],
    "broccoli":    ["broccoli", "brocoli", "بروكلي"],
    "vinegar":     ["vinegar", "vinaigre", "خل"],
    "mustard":     ["mustard", "moutarde", "خردل"],
    "coconut":     ["coconut", "noix de coco", "جوز الهند"],
    "almond":      ["almond", "almonds", "amande", "amandes", "لوز"],
    "walnut":      ["walnut", "walnuts", "noix", "جوز عين الجمل", "جوز"],
    "raisin":      ["raisin", "raisins", "raisins secs", "زبيب"],
    "olive":       ["olive", "olives", "زيتون"],
    "potato_cake": ["galette de pomme de terre", "galette de pommes de terre",
                    "galettes de pommes de terre", "potato cake", "potato patty",
                    "أقراص البطاطس", "كعكة البطاطس"],
}


# Curated correct display name per language for each canonical key.
# Used INSTEAD of machine translation for the ingredient name, so we get
# "ثوم" not the transliteration "أيل". Order: fr, en, ar.
DISPLAY = {
    "garlic":      {"fr": "ail", "en": "garlic", "ar": "ثوم"},
    "onion":       {"fr": "oignon", "en": "onion", "ar": "بصل"},
    "tomato":      {"fr": "tomate", "en": "tomato", "ar": "طماطم"},
    "potato":      {"fr": "pomme de terre", "en": "potato", "ar": "بطاطا"},
    "egg":         {"fr": "œuf", "en": "egg", "ar": "بيض"},
    "flour":       {"fr": "farine", "en": "flour", "ar": "طحين"},
    "salt":        {"fr": "sel", "en": "salt", "ar": "ملح"},
    "pepper":      {"fr": "poivre", "en": "pepper", "ar": "فلفل أسود"},
    "sugar":       {"fr": "sucre", "en": "sugar", "ar": "سكر"},
    "milk":        {"fr": "lait", "en": "milk", "ar": "حليب"},
    "butter":      {"fr": "beurre", "en": "butter", "ar": "زبدة"},
    "olive_oil":   {"fr": "huile d'olive", "en": "olive oil", "ar": "زيت الزيتون"},
    "oil":         {"fr": "huile", "en": "oil", "ar": "زيت"},
    "water":       {"fr": "eau", "en": "water", "ar": "ماء"},
    "carrot":      {"fr": "carotte", "en": "carrot", "ar": "جزر"},
    "chicken":     {"fr": "poulet", "en": "chicken", "ar": "دجاج"},
    "beef":        {"fr": "bœuf", "en": "beef", "ar": "لحم بقر"},
    "lamb":        {"fr": "agneau", "en": "lamb", "ar": "لحم خروف"},
    "fish":        {"fr": "poisson", "en": "fish", "ar": "سمك"},
    "rice":        {"fr": "riz", "en": "rice", "ar": "أرز"},
    "pasta":       {"fr": "pâtes", "en": "pasta", "ar": "معكرونة"},
    "lentils":     {"fr": "lentilles", "en": "lentils", "ar": "عدس"},
    "chickpeas":   {"fr": "pois chiches", "en": "chickpeas", "ar": "حمص"},
    "parsley":     {"fr": "persil", "en": "parsley", "ar": "بقدونس"},
    "cilantro":    {"fr": "coriandre", "en": "cilantro", "ar": "كزبرة"},
    "mint":        {"fr": "menthe", "en": "mint", "ar": "نعناع"},
    "thyme":       {"fr": "thym", "en": "thyme", "ar": "زعتر"},
    "rosemary":    {"fr": "romarin", "en": "rosemary", "ar": "إكليل الجبل"},
    "marjoram":    {"fr": "marjolaine", "en": "marjoram", "ar": "مردقوش"},
    "cumin":       {"fr": "cumin", "en": "cumin", "ar": "كمون"},
    "paprika":     {"fr": "paprika", "en": "paprika", "ar": "بابريكا"},
    "ginger":      {"fr": "gingembre", "en": "ginger", "ar": "زنجبيل"},
    "cinnamon":    {"fr": "cannelle", "en": "cinnamon", "ar": "قرفة"},
    "saffron":     {"fr": "safran", "en": "saffron", "ar": "زعفران"},
    "lemon":       {"fr": "citron", "en": "lemon", "ar": "ليمون"},
    "cheese":      {"fr": "fromage", "en": "cheese", "ar": "جبن"},
    "yogurt":      {"fr": "yaourt", "en": "yogurt", "ar": "زبادي"},
    "bread":       {"fr": "pain", "en": "bread", "ar": "خبز"},
    "honey":       {"fr": "miel", "en": "honey", "ar": "عسل"},
    "cucumber":    {"fr": "concombre", "en": "cucumber", "ar": "خيار"},
    "eggplant":    {"fr": "aubergine", "en": "eggplant", "ar": "باذنجان"},
    "zucchini":    {"fr": "courgette", "en": "zucchini", "ar": "كوسة"},
    "bell_pepper": {"fr": "poivron", "en": "bell pepper", "ar": "فلفل حلو"},
    "chili":       {"fr": "piment", "en": "chili", "ar": "فلفل حار"},
    "tuna":        {"fr": "thon", "en": "tuna", "ar": "تونة"},
    "corn":        {"fr": "maïs", "en": "corn", "ar": "ذرة"},
    "peas":        {"fr": "petits pois", "en": "peas", "ar": "بازلاء"},
    "green_beans": {"fr": "haricots verts", "en": "green beans", "ar": "فاصوليا خضراء"},
    "mushroom":    {"fr": "champignon", "en": "mushroom", "ar": "فطر"},
    "spinach":     {"fr": "épinards", "en": "spinach", "ar": "سبانخ"},
    "broccoli":    {"fr": "brocoli", "en": "broccoli", "ar": "بروكلي"},
    "vinegar":     {"fr": "vinaigre", "en": "vinegar", "ar": "خل"},
    "mustard":     {"fr": "moutarde", "en": "mustard", "ar": "خردل"},
    "coconut":     {"fr": "noix de coco", "en": "coconut", "ar": "جوز الهند"},
    "almond":      {"fr": "amandes", "en": "almonds", "ar": "لوز"},
    "walnut":      {"fr": "noix", "en": "walnuts", "ar": "جوز"},
    "raisin":      {"fr": "raisins secs", "en": "raisins", "ar": "زبيب"},
    "olive":       {"fr": "olives", "en": "olives", "ar": "زيتون"},
    "potato_cake": {"fr": "galette de pomme de terre", "en": "potato cake", "ar": "أقراص البطاطس"},
}


# Unit translations per language (so the whole line is consistent).
UNIT_DISPLAY = {
    "g":   {"fr": "g", "en": "g", "ar": "جرام"},
    "kg":  {"fr": "kg", "en": "kg", "ar": "كيلوجرام"},
    "ml":  {"fr": "ml", "en": "ml", "ar": "مل"},
    "l":   {"fr": "l", "en": "l", "ar": "لتر"},
    "gousse":  {"fr": "gousse", "en": "clove", "ar": "فص"},
    "gousses": {"fr": "gousses", "en": "cloves", "ar": "فصوص"},
    "clove":   {"fr": "gousse", "en": "clove", "ar": "فص"},
    "cloves":  {"fr": "gousses", "en": "cloves", "ar": "فصوص"},
    "pincée":  {"fr": "pincée", "en": "pinch", "ar": "رشة"},
    "pincées": {"fr": "pincées", "en": "pinches", "ar": "رشات"},
    "pinch":   {"fr": "pincée", "en": "pinch", "ar": "رشة"},
    "tasse":   {"fr": "tasse", "en": "cup", "ar": "كوب"},
    "cup":     {"fr": "tasse", "en": "cup", "ar": "كوب"},
    "cups":    {"fr": "tasses", "en": "cups", "ar": "أكواب"},
    "tbsp":    {"fr": "c. à soupe", "en": "tbsp", "ar": "ملعقة كبيرة"},
    "tbsps":   {"fr": "c. à soupe", "en": "tbsp", "ar": "ملعقة كبيرة"},
    "tablespoon":  {"fr": "c. à soupe", "en": "tablespoon", "ar": "ملعقة كبيرة"},
    "tablespoons": {"fr": "c. à soupe", "en": "tablespoons", "ar": "ملعقة كبيرة"},
    "tsp":     {"fr": "c. à café", "en": "tsp", "ar": "ملعقة صغيرة"},
    "tsps":    {"fr": "c. à café", "en": "tsp", "ar": "ملعقة صغيرة"},
    "teaspoon":  {"fr": "c. à café", "en": "teaspoon", "ar": "ملعقة صغيرة"},
    "teaspoons": {"fr": "c. à café", "en": "teaspoons", "ar": "ملعقة صغيرة"},
    "boîte":   {"fr": "boîte", "en": "can", "ar": "علبة"},
    "boite":   {"fr": "boîte", "en": "can", "ar": "علبة"},
    "boîtes":  {"fr": "boîtes", "en": "cans", "ar": "علب"},
    "can":     {"fr": "boîte", "en": "can", "ar": "علبة"},
    "cans":    {"fr": "boîtes", "en": "cans", "ar": "علب"},
    "tranche": {"fr": "tranche", "en": "slice", "ar": "شريحة"},
    "tranches":{"fr": "tranches", "en": "slices", "ar": "شرائح"},
    "slice":   {"fr": "tranche", "en": "slice", "ar": "شريحة"},
    "slices":  {"fr": "tranches", "en": "slices", "ar": "شرائح"},
    "verre":   {"fr": "verre", "en": "glass", "ar": "كوب"},
    "sachet":  {"fr": "sachet", "en": "packet", "ar": "كيس"},
    "botte":   {"fr": "botte", "en": "bunch", "ar": "حزمة"},
    "bunch":   {"fr": "botte", "en": "bunch", "ar": "حزمة"},
}

# spoon units (multi-word) — keyed by lowercased text
UNIT_DISPLAY_MULTI = {
    "c. à café":  {"fr": "c. à café", "en": "tsp", "ar": "ملعقة صغيرة"},
    "c. à soupe": {"fr": "c. à soupe", "en": "tbsp", "ar": "ملعقة كبيرة"},
    "cuillère à café":  {"fr": "cuillère à café", "en": "tsp", "ar": "ملعقة صغيرة"},
    "cuillère à soupe": {"fr": "cuillère à soupe", "en": "tbsp", "ar": "ملعقة كبيرة"},
}


def display_name(canonical: str, lang: str) -> str:
    """Curated ingredient name in a language, or '' if unknown."""
    d = DISPLAY.get(canonical)
    return d.get(lang, "") if d else ""


def display_unit(unit: str, lang: str) -> str:
    """Translate a unit to a language; falls back to the original unit."""
    if not unit:
        return ""
    u = unit.strip().lower()
    if u in UNIT_DISPLAY_MULTI:
        return UNIT_DISPLAY_MULTI[u].get(lang, unit)
    if u in UNIT_DISPLAY:
        return UNIT_DISPLAY[u].get(lang, unit)
    return unit


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
