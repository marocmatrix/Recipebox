# Changelog

## 1.0.0
- Initial release
- Recipes with ingredients, tags, servings, main photo
- Per-step photos and inline timers
- Full-screen guided Cook Mode (wake-lock + countdowns)
- Import recipes from a URL (schema.org/Recipe JSON-LD)
- Shopping list (manual + add-all-from-recipe)
- Weekly meal planner
- SQLite storage in /data, Ingress-enabled

## 1.1.0
- Multi-language support: English, French, Arabic (with full RTL layout)
- First-run language picker; change anytime in Settings

## 1.1.1
- Fix Docker build: COPY paths are now relative to the add-on build context

## 1.1.2
- Fix startup crash: run from /app and launch via `python3 -m uvicorn`

## 1.1.3
- Launch server via `python3 -m app.main` (programmatic uvicorn)
- run.sh now import-tests first and prints a full traceback on failure

## 1.1.4
- Fix startup crash when app/static folder was missing (auto-create it; also mkdir in Dockerfile)

## 1.1.5
- Add a photo per ingredient (thumbnail in editor + recipe view); reused wherever the ingredient appears
- Fix: form-uploaded photos were ignored due to UploadFile class mismatch (also fixes step photos)
- Auto-migrate older databases to add the new ingredient image column

## 1.1.6
- Ingredient photo picker: choose from a built-in icon library, upload, or paste an image URL
- Icon library lives in app/ingredient_icons/ (add your own files + push to GitHub)
- Auto-suggests library icons whose filename matches the ingredient text
- Ships 12 sample icons; URL images are downloaded and stored locally

## 1.1.7
- New "Ingredient Icons" page: upload/delete your own ingredient icons in-app (no GitHub needed)
- User icons stored in /data/icons (persist across updates & included in snapshots)
- Picker now offers both built-in and your uploaded icons

## 1.2.0
- Fix: language change now applies immediately (no-cache headers on HTML)
- Favorites: star any recipe, filter the list to favorites only
- Recipe fields: difficulty (easy/medium/hard) and cuisine
- Shopping intelligence: duplicate items merge into a quantity (e.g. Tomatoes × 3)
- Shopping list grouped by category (produce, meat & fish, dairy, bakery, pantry, other)
- Home Assistant sensors via /api/state (recipes, favorites, shopping, meals today) — see HOME_ASSISTANT_SENSORS.md

## 1.3.0
- Structured ingredients: separate Quantity / Unit / Name fields per ingredient
- Editor now has three fields per ingredient row (photo picker unchanged)
- Accurate scaling using the real quantity (½× / 1× / 2× / 3×), incl. fractions & ranges
- Existing free-text ingredients auto-parse into structured fields on update (original text kept as fallback)
- Imported recipes are parsed into structured fields too

## 1.3.1
- Ingredient photos are remembered per name and reused across recipes
- Typing a known ingredient name suggests its saved photo; also auto-fills on save if none chosen
- Only uploaded/URL photos are remembered (icon-library picks stay manual)

## 1.3.2
- New app icon and logo (recipe book + utensils, terracotta theme); SVG sources included

## 1.3.3
- Ingredient Icons page: add an icon by pasting an image URL (in addition to file upload)

## 1.3.4
- Better French ingredient parsing: recognizes "cuillère à café/soupe" (and common misspellings), gousse, pincée, verre, sachet...
- Strips connectors ("de", "d'", "of") so names come out clean (e.g. "oignon", "huile d'olive")
- Existing recipes with mis-split ingredients are auto-corrected on update

## 1.3.5
- Recognize abbreviated French units: "c. à café", "c. à soupe" (and variants c à c, c.à.s, etc.)
- Existing imported recipes with these units auto-correct on update

## 1.3.6
- Backfill ingredient image memory from existing recipes on update, so previously-set photos
  (incl. ones set before the memory feature) auto-apply to new recipes

## 1.3.7
- Backfill now also fills remembered photos into existing recipes that were missing them
  (applies across all old recipes on update, not just newly-saved ones)

## 1.3.8
- Add /api/debug-ingredients diagnostic (shows stored ingredient names/images + memory)
- Fix: SVG images added by URL are now saved correctly (previously failed silently via Pillow)

## 1.4.0
- Cross-language ingredient icons: a multilingual alias map (FR/EN/AR) matches
  e.g. "ail" / "garlic" / "ثوم" to the same icon, so imports from any-language sites match
- Auto-apply priority: library icon (by alias) first, then remembered photo
- Backfill and the "suggest while typing" lookup both use the alias map
- ~45 common ingredients seeded; extend via app/ingredient_aliases.py
