# Ingredient icon library

Drop image files here and they become selectable in the ingredient editor.

## How it works
- Supported formats: **.svg, .png, .jpg, .jpeg, .webp, .gif**
- The **filename (without extension)** is the icon's name, e.g. `flour.svg` → "flour".
- Use lowercase and underscores for multi-word names, e.g. `olive_oil.png`, `bell_pepper.svg`.
- When you type an ingredient (e.g. "200 g flour"), RecipeBox auto-suggests icons
  whose name appears in the text. You can also browse the full grid and pick any icon.

## Adding your own
1. Add image files to this folder (`recipebox/app/ingredient_icons/`).
2. Commit and push to GitHub.
3. Rebuild/Update the add-on in Home Assistant.

Tip: small square images (around 48×48 to 128×128) look best as ingredient thumbnails.

## Note on copyright
Only add icons you have the right to use (your own, or freely/openly licensed sets).
Do not add proprietary icon sets from commercial apps.
