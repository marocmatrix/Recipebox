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

## 1.5.0
- Fetch REAL ingredient photos from TheMealDB (free, no key) on the Ingredient Icons page
- "Fetch by name" for one ingredient, plus "Auto-fetch all missing" for the whole library
- Uses the alias map so French/Arabic names (ail, ثوم) are queried in English (garlic)
- Fetched photos saved to /data and applied to matching ingredients automatically

## 1.6.0
- Recipe content translation (title, description, ingredients, steps) via DeepL
- Add your DeepL API key in Settings; imported recipes auto-translate into FR/EN/AR
- "Translate" button on each recipe for ones added before the key was set
- Switching UI language now also switches recipe content (stored, instant; falls back to original)

## 1.6.4
- Fix translation: corrected DeepL request encoding (multiple text fields) that caused
  a silent local error and made translations return the original text unchanged

## 1.6.5
- Ingredient translation now translates the FULL line (quantity + unit + name), consistent per language
- Curated correct words for known ingredients (ail→ثوم, oignon→بصل) instead of DeepL transliteration
- Units are translated too (gousse→فص, c. à soupe→ملعقة كبيرة, g→غ, etc.)
- Unknown ingredients still fall back to DeepL on the full name

## 1.6.6
- Arabic units use fuller words: جرام (g), كيلوجرام (kg), لتر (l)

## 1.6.7
- More curated ingredients (tuna→تونة, corn→ذرة, peas, mushroom, olive, almond...) so DeepL no longer transliterates them
- "boîte/can", slice, glass, packet, bunch units translated; boîte now parsed as a unit
- Existing "boîte de X" ingredients auto-resplit on update

## 1.6.8
- Auto-detect each recipe's source language (FR/EN/AR) and tell DeepL explicitly,
  fixing transliteration of French terms (e.g. "galette de pomme de terre")
- Added galette de pomme de terre to curated terms

## 1.7.0
- New "What can I cook?" page: list ingredients you have, get your recipes ranked by fewest missing
- Cross-language matching via the alias map (ail/garlic/ثوم all match); shows what's missing
- Tap-to-add ingredient chips from your own recipes

## 1.6.9
- Fix: ingredients with a descriptor (poivron vert/jaune/rouge, farine de blé...) no longer
  collapse to the base word when translated — curated word is used only for exact matches,
  otherwise the full name is translated so colors/qualifiers are preserved

## 1.7.0
- Better volume units: cl, dl translated (سنتيلتر/ديسيلتر); cube recognized as a unit
- More curated ingredients: cream/crème→كريمة, bouillon→مرق, concentré de tomate→معجون طماطم,
  chapelure→بقسماط, vin→نبيذ

## 1.7.1
- Arabic ml now written مللتر

## 1.8.0
- "What can I cook?" page now also DISCOVERS famous recipes (TheMealDB) by your first ingredient
- Tap a discovered recipe to see full details, then Import (auto-translated) into your collection
- Discovery uses the alias map so French/Arabic ingredient names query in English

## 1.9.0
- Editable translations: per-recipe page (✏️) to hand-correct title/description/ingredients/steps in FR/EN/AR
- Export / backup: download all recipes as JSON (Settings), and restore from a JSON backup
- Nutrition: imported recipes now capture & show per-serving calories/protein/fat/carbs/etc. when the site provides it
