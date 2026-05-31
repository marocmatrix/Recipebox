# RecipeBox — Home Assistant Add-on

A self-hosted recipe manager with **per-step photos**, **inline step timers**, a full-screen
**guided cook mode**, **URL import**, **shopping lists**, and **meal planning** — inspired by
Mealie and the Cookidoo guided-cooking experience, but fully your own and self-hosted.

> Note: This is an original app. It does **not** include or connect to Cookidoo/Thermomix
> content, which is proprietary to Vorwerk.

## Features

- 📖 Recipes with ingredients, steps, tags, servings, images
- 📸 A photo per instruction step (guided-cooking style)
- ⏱️ Inline timers attached to steps
- 👨‍🍳 Full-screen Cook Mode (keeps screen awake, step-by-step)
- 🔗 Import recipes from a URL (schema.org/Recipe JSON-LD)
- 🛒 Shopping list (add ingredients straight from a recipe)
- 🗓️ Weekly meal planner
- 🌍 Multi-language UI: English, French, Arabic (RTL) — picked on first launch
- 💾 SQLite storage in `/data` (persists across restarts/updates)

## Install (Home Assistant)

1. Push this whole repository to GitHub (public or private).
2. In Home Assistant: **Settings → Add-ons → Add-on Store**.
3. Top-right **⋮ → Repositories**, paste your repo URL, click **Add**.
4. Find **RecipeBox** in the store, click it, then **Install**.
5. Start the add-on. Open the Web UI (Ingress) from the add-on page.

## Repository layout

```
.
├── README.md
├── repository.yaml          # makes this a valid HA add-on repo
└── recipebox/               # the add-on itself
    ├── config.yaml          # add-on manifest
    ├── Dockerfile
    ├── build.yaml           # base images per architecture
    ├── run.sh               # startup script
    ├── requirements.txt
    ├── icon.png             # (add your own 256x256 png)
    ├── logo.png             # (add your own png)
    └── app/                 # FastAPI application
        ├── main.py
        ├── database.py
        ├── models.py
        ├── scraper.py
        ├── templates/
        └── static/
```

## Development (run locally without HA)

```bash
cd recipebox
pip install -r requirements.txt
DATA_DIR=./data uvicorn app.main:app --host 0.0.0.0 --port 8099 --reload
```
Then open http://localhost:8099
