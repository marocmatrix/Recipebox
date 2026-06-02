# RecipeBox

Your own self-hosted recipe manager — recipes with per-step photos, inline timers,
a guided full-screen cook mode, URL import, shopping lists and meal planning.

## How to use

After starting the add-on, open the Web UI from the add-on page (it appears in the
Home Assistant sidebar as **RecipeBox**).

### Add recipes
- **New** — build a recipe by hand. Each step can have its own photo and a timer.
- **Import** — paste a recipe URL; RecipeBox reads the page's structured data and
  fills in the title, ingredients, steps, time and image. Add step photos/timers after.

### Cook mode
Open any recipe and tap **Cook mode** for a distraction-free, step-by-step view that
keeps the screen awake and runs each step's timer. Great on a tablet in the kitchen.

### Shopping list
From a recipe, tap **Add all to shopping list**, or add items manually. Tap an item
to check it off; **Clear checked** removes the done ones.

### Meal planner
The **Planner** shows the current week. Pick a recipe for any breakfast/lunch/dinner slot.

## Language
On first launch you'll pick a language — **English, French, or Arabic** (Arabic
displays right-to-left). You can change it anytime from the **Settings** page.

## Data & backups
Everything (database + uploaded photos) lives in the add-on's `/data` folder, which
Home Assistant persists across restarts and updates, and includes in HA snapshots.

## Notes
This is an original application. It does not include or connect to Cookidoo /
Thermomix content, which is proprietary to Vorwerk.

## Ingredient photos & icon library
Each ingredient can have a small photo. In the recipe editor, tap the photo square
next to an ingredient to:
- pick from the **icon library** (auto-suggested by the ingredient name),
- **upload** a photo, or
- **paste an image URL** (it's downloaded and stored locally).

To grow the icon library, add image files (.svg/.png/.jpg/.webp) to
`recipebox/app/ingredient_icons/` in your repo and update the add-on. The filename
(without extension) is the icon name used for matching, e.g. `olive_oil.png`.
Only add icons you have the right to use.

## Managing the icon library in-app
Open **Ingredient Icons** from the menu to upload your own ingredient icons
(give each a name like "paprika"). These are saved in /data and survive add-on
updates. Built-in icons that ship with the add-on are shown separately and can't
be deleted. Uploaded icons appear in every recipe's ingredient photo picker.

## Structured ingredients
Ingredients are stored as separate Quantity, Unit and Name fields (e.g. 500 / g / flour).
The editor shows three fields per row. Scaling (½× to 3×) uses the real quantity, so
amounts recalculate correctly. Unparseable lines (e.g. "a pinch of salt") are kept as-is
in the Name field. Existing recipes upgrade automatically the first time you open v1.3.0.

## Remembered ingredient photos
When you set an uploaded or URL photo for an ingredient (e.g. "onion"), RecipeBox
remembers it by name. The next time you add "onion" to any recipe, that photo is
suggested as you type and applied automatically on save if you don't pick another.
Icon-library choices are not auto-remembered (they remain a manual pick).

## Fetching real ingredient photos
On the Ingredient Icons page you can pull real photos from TheMealDB (free):
- "Fetch a photo by ingredient name" — type e.g. "ail" / "garlic" / "ثوم" and it
  fetches a real garlic photo (names are matched to English via the alias map).
- "Auto-fetch all missing" — scans your recipes and fetches a photo for every
  ingredient that doesn't already have an icon, then applies them.
Fetched images are stored in /data and persist across updates. Requires the add-on
to have internet access on your device. Not every ingredient exists in TheMealDB;
those are simply skipped and you can upload your own.

## Translating recipe content
RecipeBox can translate the actual recipe text (title, ingredients, steps), not just
the interface. Get a free DeepL API key (deepl.com/pro-api, the key ends in ":fx"),
paste it in Settings. Imported recipes are then translated automatically into the
other languages and stored, so switching language (FR/EN/AR) instantly shows the
translated content. For recipes added before you set the key, open the recipe and
press "Translate". Requires internet access on the device. Untranslated recipes
simply show their original text.

## What can I cook?
The "What can I cook?" page (in the top nav) lets you list the ingredients you have
on hand. RecipeBox then ranks YOUR saved recipes by how few ingredients are missing,
shows exactly what you'd need to buy, and matches across languages (ail = garlic = ثوم).
Tap the suggestion chips to quickly add ingredients you already use.
