"""Lightweight recipe importer.

Reads schema.org/Recipe data (JSON-LD) from a page — the same structured data
most major recipe sites publish. Falls back gracefully if not present.
"""
import json
import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RecipeBox/1.0; +https://github.com)"
}


def _iso_duration_to_minutes(value):
    """Convert ISO-8601 duration like 'PT1H30M' to minutes."""
    if not value or not isinstance(value, str) or not value.startswith("PT"):
        return 0
    import re
    h = re.search(r"(\d+)H", value)
    m = re.search(r"(\d+)M", value)
    return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)


def _find_recipe_node(data):
    """Recursively locate a Recipe object inside arbitrary JSON-LD."""
    if isinstance(data, dict):
        t = data.get("@type")
        if t == "Recipe" or (isinstance(t, list) and "Recipe" in t):
            return data
        if "@graph" in data:
            found = _find_recipe_node(data["@graph"])
            if found:
                return found
        for v in data.values():
            found = _find_recipe_node(v)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = _find_recipe_node(item)
            if found:
                return found
    return None


def _as_text_list(value):
    """Normalize instructions/ingredients into a list of strings."""
    out = []
    if isinstance(value, str):
        out.append(value.strip())
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                out.append(item.strip())
            elif isinstance(item, dict):
                # HowToStep / HowToSection
                if item.get("@type") == "HowToSection":
                    out.extend(_as_text_list(item.get("itemListElement", [])))
                else:
                    txt = item.get("text") or item.get("name")
                    if txt:
                        out.append(txt.strip())
    return [x for x in out if x]


def scrape(url: str) -> dict:
    """Return a dict ready to build a Recipe, or raise ValueError."""
    resp = httpx.get(url, headers=HEADERS, timeout=20.0, follow_redirects=True)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    recipe = None
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "{}")
        except (json.JSONDecodeError, TypeError):
            continue
        recipe = _find_recipe_node(data)
        if recipe:
            break

    if not recipe:
        raise ValueError(
            "No structured recipe data (JSON-LD) found on this page."
        )

    image = ""
    img = recipe.get("image")
    if isinstance(img, list) and img:
        image = img[0] if isinstance(img[0], str) else img[0].get("url", "")
    elif isinstance(img, dict):
        image = img.get("url", "")
    elif isinstance(img, str):
        image = img

    yld = recipe.get("recipeYield")
    if isinstance(yld, list):
        yld = yld[0] if yld else 4
    try:
        servings = int("".join(c for c in str(yld) if c.isdigit()) or 4)
    except ValueError:
        servings = 4

    return {
        "title": recipe.get("name", "Imported recipe"),
        "description": (recipe.get("description") or "")[:2000],
        "servings": servings,
        "prep_minutes": _iso_duration_to_minutes(recipe.get("prepTime")),
        "cook_minutes": _iso_duration_to_minutes(recipe.get("cookTime")),
        "image_url": image,
        "ingredients": _as_text_list(recipe.get("recipeIngredient", [])),
        "steps": _as_text_list(recipe.get("recipeInstructions", [])),
        "source_url": url,
    }
