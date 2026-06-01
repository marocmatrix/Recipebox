import os
import uuid
import io
from datetime import date, datetime, timedelta

import httpx
from fastapi import FastAPI, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from PIL import Image

from .database import engine, Base, get_db, DATA_DIR, SessionLocal
from . import models, scraper
from .i18n import LANGUAGES, make_translator
from .ingredient_parser import (parse_ingredient, compose_text,
                                quantity_to_float, format_quantity)

Base.metadata.create_all(bind=engine)


def _ensure_column(table: str, column: str, ddl: str):
    """Add a column if an older database is missing it (simple SQLite migration)."""
    from sqlalchemy import text
    with engine.connect() as conn:
        cols = [row[1] for row in conn.execute(text(f"PRAGMA table_info({table})"))]
        if column not in cols:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))
            conn.commit()


# Migrations for databases created before a column existed
_ensure_column("ingredients", "image", "image VARCHAR DEFAULT ''")
_ensure_column("ingredients", "quantity", "quantity VARCHAR DEFAULT ''")
_ensure_column("ingredients", "unit", "unit VARCHAR DEFAULT ''")
_ensure_column("ingredients", "name", "name VARCHAR DEFAULT ''")
_ensure_column("recipes", "favorite", "favorite BOOLEAN DEFAULT 0")
_ensure_column("recipes", "difficulty", "difficulty VARCHAR DEFAULT ''")
_ensure_column("recipes", "cuisine", "cuisine VARCHAR DEFAULT ''")
_ensure_column("shopping_items", "category", "category VARCHAR DEFAULT ''")
_ensure_column("shopping_items", "quantity", "quantity INTEGER DEFAULT 1")


def _upgrade_ingredient_structure():
    """Parse legacy free-text ingredients into qty/unit/name once.

    Also re-parses rows that were split by an older parser version (detected by
    the name still beginning with a known unit word, e.g. 'cuillère à café de ...').
    """
    db = SessionLocal()
    try:
        from .ingredient_parser import _UNIT_SET, _MULTI_SORTED
        rows = db.query(models.Ingredient).all()
        changed = 0
        for ing in rows:
            needs = False
            if not (ing.name or "").strip():
                needs = True
            else:
                low = (ing.name or "").lower()
                # old mis-split: name starts with a unit word/phrase
                first = low.split(" ", 1)[0]
                if first in _UNIT_SET or any(low.startswith(m) for m in _MULTI_SORTED):
                    needs = True
            if not needs or not (ing.text or "").strip():
                continue
            p = parse_ingredient(ing.text)
            ing.quantity = p["quantity"]
            ing.unit = p["unit"]
            ing.name = p["name"] or ing.text
            changed += 1
        if changed:
            db.commit()
    finally:
        db.close()


def _backfill_ingredient_images():
    """Populate the image memory from ingredients that already have a photo,
    then apply remembered photos to any existing ingredients that lack one.

    This makes previously-set photos auto-apply across all existing recipes,
    not just newly-saved ones. Icon-library picks are not auto-remembered.
    """
    db = SessionLocal()
    try:
        rows = (db.query(models.Ingredient)
                .filter(models.Ingredient.image != "")
                .filter(models.Ingredient.image.isnot(None))
                .order_by(models.Ingredient.id).all())
        # 1) build/refresh memory from photographed ingredients
        for ing in rows:
            nm = (ing.name or "").strip().lower()
            img = ing.image or ""
            if not nm or not img or img.startswith(("icon:", "usericon:")):
                continue
            rec = db.get(models.IngredientImage, nm)
            if rec:
                rec.image = img
            else:
                db.add(models.IngredientImage(name=nm, image=img))
        db.flush()

        # 2) apply remembered photos to ingredients that have none
        memory = {m.name: m.image for m in db.query(models.IngredientImage).all()}
        if memory:
            blanks = (db.query(models.Ingredient)
                      .filter((models.Ingredient.image == "")
                              | (models.Ingredient.image.is_(None))).all())
            for ing in blanks:
                nm = (ing.name or "").strip().lower()
                if nm in memory and memory[nm]:
                    ing.image = memory[nm]
        db.commit()
    finally:
        db.close()


def get_setting(db: Session, key: str, default: str = "") -> str:
    s = db.get(models.Setting, key)
    return s.value if s else default


def set_setting(db: Session, key: str, value: str):
    s = db.get(models.Setting, key)
    if s:
        s.value = value
    else:
        db.add(models.Setting(key=key, value=value))
    db.commit()


def remember_ingredient_image(db: Session, name: str, image: str):
    """Store/refresh the remembered image for an ingredient name."""
    key = (name or "").strip().lower()
    if not key or not image:
        return
    rec = db.get(models.IngredientImage, key)
    if rec:
        rec.image = image
    else:
        db.add(models.IngredientImage(name=key, image=image))


def recall_ingredient_image(db: Session, name: str) -> str:
    key = (name or "").strip().lower()
    if not key:
        return ""
    rec = db.get(models.IngredientImage, key)
    return rec.image if rec else ""

BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ensure the static dir exists even if it wasn't shipped (e.g. empty folders
# dropped during upload), so StaticFiles doesn't fail at startup.
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Built-in ingredient icon library (shipped in the repo, read-only)
ICONS_DIR = os.path.join(BASE_DIR, "ingredient_icons")
os.makedirs(ICONS_DIR, exist_ok=True)
# User-managed icon library (persists in /data across updates)
USER_ICONS_DIR = os.path.join(DATA_DIR, "icons")
os.makedirs(USER_ICONS_DIR, exist_ok=True)
ICON_EXTS = (".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif")


def list_icons():
    """Return [{name, file, source}] from both built-in and user libraries.

    source is 'builtin' (served at /icons/) or 'user' (served at /usericons/).
    User icons with the same filename override built-in ones.
    """
    seen = {}
    for fn in sorted(os.listdir(ICONS_DIR)):
        if fn.lower().endswith(ICON_EXTS):
            seen[fn] = {"name": os.path.splitext(fn)[0], "file": fn, "source": "builtin"}
    for fn in sorted(os.listdir(USER_ICONS_DIR)):
        if fn.lower().endswith(ICON_EXTS):
            seen[fn] = {"name": os.path.splitext(fn)[0], "file": fn, "source": "user"}
    return sorted(seen.values(), key=lambda x: x["name"].lower())


def icon_ref(file: str, source: str) -> str:
    """Build the stored image reference for an icon."""
    return f"usericon:{file}" if source == "user" else f"icon:{file}"


app = FastAPI(title="RecipeBox")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/icons", StaticFiles(directory=ICONS_DIR), name="icons")
app.mount("/usericons", StaticFiles(directory=USER_ICONS_DIR), name="usericons")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# One-time upgrade of any legacy free-text ingredients
_upgrade_ingredient_structure()
# Backfill image memory from already-photographed ingredients
_backfill_ingredient_images()


# ---- Ingress base-path handling -------------------------------------------
# Home Assistant serves the add-on behind a path prefix. We read the
# X-Ingress-Path header and expose it to templates so links work.
@app.middleware("http")
async def ingress_base(request: Request, call_next):
    request.state.base = request.headers.get("X-Ingress-Path", "")
    # First-run gate: force language choice before using the app
    path = request.url.path
    exempt = path.startswith(("/welcome", "/set-language", "/static", "/uploads", "/health"))
    if not exempt:
        db = SessionLocal()
        try:
            chosen = get_setting(db, "language", "")
        finally:
            db.close()
        if not chosen:
            base = request.state.base
            return RedirectResponse(f"{base}/welcome", status_code=303)
    response = await call_next(request)
    # Prevent ingress/browser from caching HTML so language/content changes show immediately
    ctype = response.headers.get("content-type", "")
    if ctype.startswith("text/html"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


def ctx(request: Request, **kwargs):
    base = getattr(request.state, "base", "")
    # resolve current language from settings
    db = SessionLocal()
    try:
        lang = get_setting(db, "language", "en")
    finally:
        db.close()
    if lang not in LANGUAGES:
        lang = "en"

    def img_url(value: str) -> str:
        """Resolve a stored image value to a URL (handles icon/usericon prefixes)."""
        if not value:
            return ""
        if value.startswith("icon:"):
            return f"{base}/icons/{value[5:]}"
        if value.startswith("usericon:"):
            return f"{base}/usericons/{value[9:]}"
        return f"{base}/uploads/{value}"

    def scale_qty(quantity: str, factor: float) -> str:
        """Scale a quantity string by a factor, preserving non-numeric ones."""
        if not quantity:
            return ""
        val = quantity_to_float(quantity)
        if val is None or factor == 1:
            return quantity
        return format_quantity(val * factor)

    return {
        "request": request,
        "base": base,
        "lang": lang,
        "dir": LANGUAGES[lang]["dir"],
        "languages": LANGUAGES,
        "t": make_translator(lang),
        "img_url": img_url,
        "scale_qty": scale_qty,
        **kwargs,
    }


# ---- Image helpers ---------------------------------------------------------
def _save_image_bytes(data: bytes) -> str:
    """Resize + save an image, return its filename."""
    try:
        img = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        raise HTTPException(400, "Invalid image file")
    img.thumbnail((1280, 1280))
    fname = f"{uuid.uuid4().hex}.jpg"
    img.save(os.path.join(UPLOAD_DIR, fname), "JPEG", quality=85)
    return fname


async def _save_upload(file: UploadFile | None) -> str:
    if not file or not file.filename:
        return ""
    return _save_image_bytes(await file.read())


async def _download_image(url: str) -> str:
    if not url:
        return ""
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            r = await client.get(url, headers=scraper.HEADERS)
            r.raise_for_status()
            ctype = r.headers.get("content-type", "").lower()
            path_ext = os.path.splitext(url.split("?")[0])[1].lower()
            # SVG can't go through Pillow; save it as-is to uploads
            if "svg" in ctype or path_ext == ".svg":
                import uuid as _uuid
                fname = f"{_uuid.uuid4().hex}.svg"
                with open(os.path.join(UPLOAD_DIR, fname), "wb") as f:
                    f.write(r.content)
                return fname
            return _save_image_bytes(r.content)
    except Exception:
        return ""


# ============================  RECIPES  ====================================
@app.get("/", response_class=HTMLResponse)
def index(request: Request, q: str = "", fav: int = 0, db: Session = Depends(get_db)):
    query = db.query(models.Recipe)
    if q:
        like = f"%{q}%"
        query = query.filter(models.Recipe.title.ilike(like))
    if fav:
        query = query.filter(models.Recipe.favorite == True)
    recipes = query.order_by(models.Recipe.created_at.desc()).all()
    return templates.TemplateResponse("index.html", ctx(request, recipes=recipes, q=q, fav=fav))


@app.get("/recipe/{rid}", response_class=HTMLResponse)
def view_recipe(rid: int, request: Request, scale: float = 1.0, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, rid)
    if not r:
        raise HTTPException(404)
    return templates.TemplateResponse("recipe.html", ctx(request, r=r, scale=scale))


@app.get("/recipe/{rid}/cook", response_class=HTMLResponse)
def cook_mode(rid: int, request: Request, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, rid)
    if not r:
        raise HTTPException(404)
    return templates.TemplateResponse("cook.html", ctx(request, r=r))


@app.get("/new", response_class=HTMLResponse)
def new_recipe(request: Request):
    return templates.TemplateResponse("edit.html", ctx(request, r=None, icons=list_icons()))


@app.get("/recipe/{rid}/edit", response_class=HTMLResponse)
def edit_recipe(rid: int, request: Request, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, rid)
    if not r:
        raise HTTPException(404)
    return templates.TemplateResponse("edit.html", ctx(request, r=r, icons=list_icons()))


@app.post("/recipe/save")
async def save_recipe(
    request: Request,
    db: Session = Depends(get_db),
    rid: str = Form(""),
    title: str = Form(...),
    description: str = Form(""),
    servings: int = Form(4),
    prep_minutes: int = Form(0),
    cook_minutes: int = Form(0),
    tags: str = Form(""),
    difficulty: str = Form(""),
    cuisine: str = Form(""),
    main_image: UploadFile = File(None),
):
    form = await request.form()
    if rid:
        r = db.get(models.Recipe, int(rid))
        if not r:
            raise HTTPException(404)
    else:
        r = models.Recipe()
        db.add(r)

    r.title = title
    r.description = description
    r.servings = servings
    r.prep_minutes = prep_minutes
    r.cook_minutes = cook_minutes
    r.tags = tags
    r.difficulty = difficulty
    r.cuisine = cuisine

    new_img = await _save_upload(main_image)
    if new_img:
        r.image = new_img

    db.flush()

    # Rebuild ingredients (structured: qty/unit/name + photo)
    r.ingredients.clear()
    db.flush()
    names = form.getlist("ingredient_name")
    qtys = form.getlist("ingredient_qty")
    units = form.getlist("ingredient_unit")
    out_i = 0
    for i, nm in enumerate(names):
        nm = (nm or "").strip()
        qty = (qtys[i].strip() if i < len(qtys) else "")
        unit = (units[i].strip() if i < len(units) else "")
        # skip a fully empty row
        if not nm and not qty and not unit:
            continue
        text = compose_text(qty, unit, nm) or nm

        existing = form.get(f"ingredient_img_existing_{i}") or ""
        icon = (form.get(f"ingredient_icon_{i}") or "").strip()
        url = (form.get(f"ingredient_url_{i}") or "").strip()
        upload = form.get(f"ingredient_image_{i}")

        img = existing
        chose_new = False
        if upload is not None and hasattr(upload, "filename") and upload.filename:
            new = await _save_upload(upload)
            if new:
                img = new
                chose_new = True
        elif url:
            dl = await _download_image(url)
            if dl:
                img = dl
                chose_new = True
        elif icon:
            if icon.startswith("usericon:"):
                safe = os.path.basename(icon[9:])
                if os.path.exists(os.path.join(USER_ICONS_DIR, safe)):
                    img = f"usericon:{safe}"
                    chose_new = True
            else:
                safe = os.path.basename(icon[5:] if icon.startswith("icon:") else icon)
                if os.path.exists(os.path.join(ICONS_DIR, safe)):
                    img = f"icon:{safe}"
                    chose_new = True

        # Memory: if no image at all, try the remembered photo for this name.
        # Only saved (uploaded/url) photos auto-apply — not icon-library matches.
        if not img and nm:
            img = recall_ingredient_image(db, nm)
        # Remember an explicitly chosen upload/url photo for this name.
        # (Icons are a manual choice and are not remembered for auto-apply.)
        if chose_new and nm and img and not img.startswith(("icon:", "usericon:")):
            remember_ingredient_image(db, nm, img)

        db.add(models.Ingredient(recipe_id=r.id, position=out_i, text=text,
                                 quantity=qty, unit=unit, name=nm, image=img))
        out_i += 1

    # Rebuild steps (text + optional timer + optional photo)
    r.steps.clear()
    db.flush()
    step_texts = form.getlist("step_text")
    step_timers = form.getlist("step_timer")
    out_pos = 0
    for i, txt in enumerate(step_texts):
        if not txt.strip():
            continue
        try:
            timer = int(step_timers[i]) if i < len(step_timers) and step_timers[i] else 0
        except ValueError:
            timer = 0
        photo = form.get(f"step_image_{i}")
        fname = ""
        if photo is not None and hasattr(photo, "filename") and photo.filename:
            fname = await _save_upload(photo)
        db.add(models.Step(recipe_id=r.id, position=out_pos, text=txt.strip(),
                           timer_seconds=timer, image=fname))
        out_pos += 1

    db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/recipe/{r.id}", status_code=303)


@app.post("/recipe/{rid}/delete")
def delete_recipe(rid: int, request: Request, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, rid)
    if r:
        db.delete(r)
        db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/", status_code=303)


# ============================  IMPORT  =====================================
@app.get("/import", response_class=HTMLResponse)
def import_form(request: Request):
    return templates.TemplateResponse("import.html", ctx(request, error=None))


@app.post("/import")
async def import_url(request: Request, url: str = Form(...), db: Session = Depends(get_db)):
    try:
        data = scraper.scrape(url)
    except Exception as e:
        return templates.TemplateResponse("import.html", ctx(request, error=str(e)))

    r = models.Recipe(
        title=data["title"], description=data["description"],
        servings=data["servings"], prep_minutes=data["prep_minutes"],
        cook_minutes=data["cook_minutes"], source_url=data["source_url"],
    )
    r.image = await _download_image(data.get("image_url", ""))
    db.add(r)
    db.flush()
    for i, txt in enumerate(data["ingredients"]):
        p = parse_ingredient(txt)
        db.add(models.Ingredient(recipe_id=r.id, position=i, text=txt,
                                 quantity=p["quantity"], unit=p["unit"],
                                 name=p["name"] or txt))
    for i, txt in enumerate(data["steps"]):
        db.add(models.Step(recipe_id=r.id, position=i, text=txt))
    db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/recipe/{r.id}/edit", status_code=303)


# ========================  SHOPPING LIST  ==================================
SHOPPING_CATEGORIES = {
    "produce": ["tomato", "onion", "garlic", "potato", "carrot", "pepper", "lemon",
                "lime", "apple", "banana", "lettuce", "spinach", "herb", "parsley",
                "cilantro", "coriander", "mint", "cucumber", "courgette", "zucchini",
                "aubergine", "eggplant", "olive", "fruit", "vegetable"],
    "meat & fish": ["chicken", "beef", "lamb", "pork", "fish", "shrimp", "prawn",
                    "meat", "turkey", "sausage", "bacon", "kefta", "merguez"],
    "dairy & eggs": ["milk", "butter", "cheese", "cream", "yogurt", "yoghurt",
                     "egg", "eggs"],
    "bakery": ["bread", "flour", "baguette", "bun", "dough", "pastry"],
    "pantry": ["sugar", "salt", "pepper", "oil", "vinegar", "rice", "pasta",
               "spice", "paprika", "cumin", "cinnamon", "saffron", "stock",
               "broth", "tomato paste", "honey", "couscous", "lentil", "chickpea",
               "bean", "can", "tin"],
}


def _categorize(text: str) -> str:
    low = text.lower()
    for cat, words in SHOPPING_CATEGORIES.items():
        if any(w in low for w in words):
            return cat
    return "other"


def _add_shopping(db: Session, text: str, qty: int = 1):
    """Add an item, merging with an existing unchecked item of the same text."""
    text = text.strip()
    if not text:
        return
    existing = (db.query(models.ShoppingItem)
                .filter(models.ShoppingItem.checked == False)
                .filter(models.ShoppingItem.text.ilike(text))
                .first())
    if existing:
        existing.quantity = (existing.quantity or 1) + qty
    else:
        db.add(models.ShoppingItem(text=text, quantity=qty, category=_categorize(text)))


@app.get("/shopping", response_class=HTMLResponse)
def shopping(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.ShoppingItem).order_by(
        models.ShoppingItem.checked, models.ShoppingItem.created_at).all()
    # group unchecked by category; checked go in their own bucket
    order = ["produce", "meat & fish", "dairy & eggs", "bakery", "pantry", "other"]
    groups = {}
    checked = []
    for it in items:
        if it.checked:
            checked.append(it)
        else:
            groups.setdefault(it.category or "other", []).append(it)
    ordered_groups = [(c, groups[c]) for c in order if c in groups]
    # any categories not in the known order
    for c in groups:
        if c not in order:
            ordered_groups.append((c, groups[c]))
    return templates.TemplateResponse(
        "shopping.html", ctx(request, groups=ordered_groups, checked=checked))


@app.post("/shopping/add")
def shopping_add(request: Request, text: str = Form(...), db: Session = Depends(get_db)):
    _add_shopping(db, text)
    db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/shopping", status_code=303)


@app.post("/shopping/{iid}/toggle")
def shopping_toggle(iid: int, request: Request, db: Session = Depends(get_db)):
    it = db.get(models.ShoppingItem, iid)
    if it:
        it.checked = not it.checked
        db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/shopping", status_code=303)


@app.post("/shopping/clear")
def shopping_clear(request: Request, db: Session = Depends(get_db)):
    db.query(models.ShoppingItem).filter(models.ShoppingItem.checked == True).delete()
    db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/shopping", status_code=303)


@app.post("/recipe/{rid}/to-shopping")
def add_recipe_to_shopping(rid: int, request: Request, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, rid)
    if r:
        for ing in r.ingredients:
            _add_shopping(db, ing.text)
        db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/shopping", status_code=303)


# =========================  MEAL PLANNER  ==================================
@app.get("/planner", response_class=HTMLResponse)
def planner(request: Request, db: Session = Depends(get_db)):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    days = [monday + timedelta(days=i) for i in range(7)]
    plans = db.query(models.MealPlan).filter(
        models.MealPlan.day >= monday,
        models.MealPlan.day <= monday + timedelta(days=6)).all()
    grid = {}
    for d in days:
        grid[d] = {m: [] for m in ("breakfast", "lunch", "dinner")}
    for p in plans:
        if p.day in grid:
            grid[p.day][p.meal_type].append(p)
    recipes = db.query(models.Recipe).order_by(models.Recipe.title).all()
    return templates.TemplateResponse(
        "planner.html",
        ctx(request, days=days, grid=grid, recipes=recipes),
    )


@app.post("/planner/add")
def planner_add(
    request: Request,
    day: str = Form(...),
    meal_type: str = Form(...),
    recipe_id: str = Form(""),
    db: Session = Depends(get_db),
):
    p = models.MealPlan(
        day=datetime.strptime(day, "%Y-%m-%d").date(),
        meal_type=meal_type,
        recipe_id=int(recipe_id) if recipe_id else None,
    )
    db.add(p)
    db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/planner", status_code=303)


@app.post("/planner/{pid}/delete")
def planner_delete(pid: int, request: Request, db: Session = Depends(get_db)):
    p = db.get(models.MealPlan, pid)
    if p:
        db.delete(p)
        db.commit()
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/planner", status_code=303)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recipe/{rid}/favorite")
def toggle_favorite(rid: int, request: Request, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, rid)
    if r:
        r.favorite = not bool(r.favorite)
        db.commit()
    base = getattr(request.state, "base", "")
    ref = request.headers.get("referer", "")
    # return to where the user was if possible, else the recipe
    target = f"{base}/recipe/{rid}"
    return RedirectResponse(target, status_code=303)


@app.get("/api/debug-ingredients")
def api_debug_ingredients(db: Session = Depends(get_db)):
    """Diagnostic: show stored ingredient names/images and the memory table."""
    ings = []
    for ing in db.query(models.Ingredient).order_by(models.Ingredient.id).all():
        ings.append({
            "recipe_id": ing.recipe_id,
            "name": ing.name,
            "name_repr": repr(ing.name),     # reveals hidden spaces/case
            "image": ing.image,
            "text": ing.text,
        })
    memory = [{"name": m.name, "name_repr": repr(m.name), "image": m.image}
              for m in db.query(models.IngredientImage).all()]
    return {"ingredients": ings, "memory": memory}


@app.get("/api/state")
def api_state(db: Session = Depends(get_db)):
    """Summary for Home Assistant sensors."""
    import datetime as _dt
    total = db.query(models.Recipe).count()
    favs = db.query(models.Recipe).filter(models.Recipe.favorite == True).count()
    shop_open = (db.query(models.ShoppingItem)
                 .filter(models.ShoppingItem.checked == False).count())
    today = _dt.date.today()
    meals_today = (db.query(models.MealPlan)
                   .filter(models.MealPlan.day == today).count())
    fav_titles = [r.title for r in db.query(models.Recipe)
                  .filter(models.Recipe.favorite == True)
                  .order_by(models.Recipe.title).limit(50)]
    return {
        "recipes": total,
        "favorites": favs,
        "favorite_titles": fav_titles,
        "shopping_open": shop_open,
        "meals_today": meals_today,
    }


@app.get("/api/icons")
def api_icons():
    return {"icons": list_icons()}


@app.get("/api/ingredient-image")
def api_ingredient_image(request: Request, name: str = "", db: Session = Depends(get_db)):
    """Return the remembered photo for an ingredient name, as a resolvable URL."""
    ref = recall_ingredient_image(db, name)
    if not ref:
        return {"found": False}
    base = getattr(request.state, "base", "")
    if ref.startswith("icon:"):
        url = f"{base}/icons/{ref[5:]}"
    elif ref.startswith("usericon:"):
        url = f"{base}/usericons/{ref[9:]}"
    else:
        url = f"{base}/uploads/{ref}"
    return {"found": True, "url": url, "ref": ref}


# ====================  ICON LIBRARY MANAGEMENT  ============================
import re as _re


def _safe_icon_name(name: str, original_filename: str) -> str:
    """Build a safe filename: sanitized name + original extension."""
    ext = os.path.splitext(original_filename)[1].lower()
    if ext not in ICON_EXTS:
        ext = ".png"
    base = _re.sub(r"[^a-z0-9_]+", "_", (name or "").strip().lower()).strip("_")
    if not base:
        base = os.path.splitext(os.path.basename(original_filename))[0].lower()
        base = _re.sub(r"[^a-z0-9_]+", "_", base).strip("_") or "icon"
    return base + ext


@app.get("/icons-manage", response_class=HTMLResponse)
def icons_manage(request: Request):
    return templates.TemplateResponse(
        "icons.html", ctx(request, icons=list_icons()))


@app.post("/icons-manage/upload")
async def icons_upload(
    request: Request,
    name: str = Form(""),
    url: str = Form(""),
    icon_file: UploadFile = File(None),
):
    data = None
    src_ext = ""
    src_name = "icon"
    # Prefer an uploaded file; otherwise fetch from URL
    if icon_file is not None and getattr(icon_file, "filename", ""):
        data = await icon_file.read()
        src_ext = os.path.splitext(icon_file.filename)[1].lower()
        src_name = icon_file.filename
    elif url.strip():
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                resp = await client.get(url.strip(), headers=scraper.HEADERS)
                resp.raise_for_status()
                data = resp.content
            path_ext = os.path.splitext(url.split("?")[0])[1].lower()
            ctype = resp.headers.get("content-type", "")
            if path_ext in ICON_EXTS:
                src_ext = path_ext
            elif "svg" in ctype:
                src_ext = ".svg"
            else:
                src_ext = ".png"
            src_name = os.path.basename(url.split("?")[0]) or "icon"
        except Exception:
            data = None

    if data:
        fname = _safe_icon_name(name, src_name)
        if src_ext == ".svg":
            with open(os.path.join(USER_ICONS_DIR, os.path.splitext(fname)[0] + ".svg"), "wb") as f:
                f.write(data)
        else:
            try:
                img = Image.open(io.BytesIO(data)).convert("RGBA")
                img.thumbnail((256, 256))
                save_name = os.path.splitext(fname)[0] + ".png"
                img.save(os.path.join(USER_ICONS_DIR, save_name), "PNG")
            except Exception:
                pass
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/icons-manage", status_code=303)


@app.post("/icons-manage/delete")
def icons_delete(request: Request, file: str = Form(...)):
    # only user icons can be deleted (built-in ship with the add-on)
    safe = os.path.basename(file)
    path = os.path.join(USER_ICONS_DIR, safe)
    if os.path.exists(path):
        os.remove(path)
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/icons-manage", status_code=303)


# ====================  LANGUAGE / SETTINGS  ================================
@app.get("/welcome", response_class=HTMLResponse)
def welcome(request: Request):
    # default-preview language for the picker itself
    return templates.TemplateResponse("welcome.html", ctx(request))


@app.post("/set-language")
def set_language(request: Request, language: str = Form(...), db: Session = Depends(get_db)):
    if language not in LANGUAGES:
        language = "en"
    set_setting(db, "language", language)
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/", status_code=303)


@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, saved: int = 0):
    return templates.TemplateResponse("settings.html", ctx(request, saved=bool(saved)))


@app.post("/settings")
def settings_save(request: Request, language: str = Form(...), db: Session = Depends(get_db)):
    if language not in LANGUAGES:
        language = "en"
    set_setting(db, "language", language)
    base = getattr(request.state, "base", "")
    return RedirectResponse(f"{base}/settings?saved=1", status_code=303)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8099,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
