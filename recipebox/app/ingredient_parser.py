"""Parse a free-text ingredient line into (quantity, unit, name).

Best-effort: returns ("", "", text) when it can't parse confidently, so the
original text is always preserved by the caller.
"""
import re

# Multi-word units checked first (longest phrase wins). Include common
# misspelling "cueillère/cueillir" for "cuillère".
MULTI_UNITS = [
    "cuillère à soupe", "cuillères à soupe", "cuillere a soupe", "cuilleres a soupe",
    "cuillère à café", "cuillères à café", "cuillere a cafe", "cuilleres a cafe",
    "cueillère à soupe", "cueillères à soupe", "cueillir à soupe", "cueillir a soupe",
    "cueillère à café", "cueillères à café", "cueillir à café", "cueillir a cafe",
    # abbreviated forms: "c. à café", "c à café", "cc", "cs", "c. à s.", etc.
    "c. à soupe", "c à soupe", "c. à s.", "c à s", "c.à.s", "c.a.s",
    "c. à café", "c à café", "c. à c.", "c à c", "c.à.c", "c.a.c",
    "fluid ounce", "fluid ounces", "fl oz",
]

# Single-word units (longest first so 'tbsp' matches before 'tb', etc.)
UNITS = [
    "kg", "g", "mg", "l", "ml", "cl", "dl",
    "tbsp", "tablespoon", "tablespoons", "tbsps",
    "tsp", "teaspoon", "teaspoons", "tsps",
    "cup", "cups", "oz", "lb", "lbs", "pound", "pounds",
    "pinch", "pinches", "clove", "cloves", "slice", "slices",
    "can", "cans", "tin", "tins", "bunch", "bunches",
    "piece", "pieces", "handful", "stick", "sticks",
    # French
    "kilo", "kilos", "gramme", "grammes", "litre", "litres",
    "cuillère", "cuillères", "cuillere", "cuilleres",
    "cueillère", "cueillir",
    "càs", "càc", "pincée", "pincées", "pincee", "pincees",
    "gousse", "gousses", "tranche", "tranches", "tasse", "tasses",
    "verre", "verres", "sachet", "sachets", "botte", "bottes",
    "boîte", "boîtes", "boite", "boites", "barquette", "barquettes",
    "cube", "cubes", "cl", "dl",
    # Arabic (common)
    "كوب", "ملعقة", "غرام", "كيلو", "حبة", "رشة", "فص",
]
_UNIT_SET = {u.lower() for u in UNITS}
_MULTI_SORTED = sorted(MULTI_UNITS, key=len, reverse=True)

# connectors to strip from the start of the name ("de l'", "d'", "of", etc.)
_CONNECTOR = re.compile(r"^(?:de\s+l['’]|de\s+la\s+|de\s+|du\s+|des\s+|d['’]|of\s+|the\s+)",
                        re.IGNORECASE)

# quantity: integer, decimal, fraction, range, or unicode fraction
_QTY = r"\d+\s*/\s*\d+|\d+[.,]\d+|\d+\s*-\s*\d+|\d+|[½¼¾⅓⅔⅛]"
_LEAD_QTY = re.compile(rf"^\s*({_QTY})\s*(.*)$")


def parse_ingredient(text: str):
    """Return dict {quantity, unit, name, text}."""
    text = (text or "").strip()
    if not text:
        return {"quantity": "", "unit": "", "name": "", "text": ""}

    quantity = ""
    rest = text
    m = _LEAD_QTY.match(text)
    if m:
        quantity = re.sub(r"\s+", "", m.group(1))
        rest = m.group(2).strip()

    unit = ""
    if rest:
        low = rest.lower()
        matched_multi = None
        for mu in _MULTI_SORTED:
            if low.startswith(mu + " ") or low == mu:
                matched_multi = mu
                break
        if matched_multi:
            unit = rest[:len(matched_multi)]
            rest = rest[len(matched_multi):].strip()
        else:
            first, _, after = rest.partition(" ")
            cand = first.strip(".,").lower()
            if cand in _UNIT_SET:
                unit = first.strip(".,")
                rest = after.strip()

    # strip a leading connector ("de", "d'", "of"...) from the name
    name = _CONNECTOR.sub("", rest).strip()
    if not name:
        name = rest
    return {"quantity": quantity, "unit": unit, "name": name, "text": text}


def compose_text(quantity: str, unit: str, name: str) -> str:
    """Build a display string from parts."""
    parts = [p for p in [str(quantity).strip(), str(unit).strip(), str(name).strip()] if p]
    return " ".join(parts)


# Fraction/unicode handling for scaling
_UNI = {"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1/3, "⅔": 2/3, "⅛": 0.125}


def quantity_to_float(q: str):
    """Best-effort numeric value of a quantity string, or None."""
    if q is None:
        return None
    q = str(q).strip()
    if not q:
        return None
    if q in _UNI:
        return _UNI[q]
    if "/" in q:
        try:
            a, b = q.split("/")
            return float(a) / float(b)
        except (ValueError, ZeroDivisionError):
            return None
    if "-" in q:  # range like 2-3 -> take the lower bound
        q = q.split("-")[0]
    q = q.replace(",", ".")
    try:
        return float(q)
    except ValueError:
        return None


def format_quantity(value: float) -> str:
    """Format a scaled number cleanly (drop trailing .0)."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 2))
