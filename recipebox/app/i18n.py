"""Simple i18n. Three languages; Arabic is RTL.

Usage in templates: {{ t('recipes') }}  (t and lang/dir injected per request)
"""

LANGUAGES = {
    "en": {"name": "English", "dir": "ltr"},
    "fr": {"name": "Français", "dir": "ltr"},
    "ar": {"name": "العربية", "dir": "rtl"},
}

TRANSLATIONS = {
    # ---- nav / general ----
    "app_name":        {"en": "RecipeBox", "fr": "RecipeBox", "ar": "صندوق الوصفات"},
    "recipes":         {"en": "Recipes", "fr": "Recettes", "ar": "الوصفات"},
    "planner":         {"en": "Planner", "fr": "Planning", "ar": "المخطط"},
    "shopping":        {"en": "Shopping", "fr": "Courses", "ar": "التسوق"},
    "import":          {"en": "Import", "fr": "Importer", "ar": "استيراد"},
    "settings":        {"en": "Settings", "fr": "Paramètres", "ar": "الإعدادات"},
    "save":            {"en": "Save", "fr": "Enregistrer", "ar": "حفظ"},
    "cancel":          {"en": "Cancel", "fr": "Annuler", "ar": "إلغاء"},
    "delete":          {"en": "Delete", "fr": "Supprimer", "ar": "حذف"},
    "edit":            {"en": "Edit", "fr": "Modifier", "ar": "تعديل"},
    "add":             {"en": "Add", "fr": "Ajouter", "ar": "إضافة"},
    "new":             {"en": "New", "fr": "Nouveau", "ar": "جديد"},

    # ---- index ----
    "my_recipes":      {"en": "My Recipes", "fr": "Mes recettes", "ar": "وصفاتي"},
    "search_recipes":  {"en": "Search recipes…", "fr": "Rechercher des recettes…", "ar": "ابحث عن وصفات…"},
    "no_recipes":      {"en": "No recipes yet", "fr": "Aucune recette pour l’instant", "ar": "لا توجد وصفات بعد"},
    "create_or_import":{"en": "Create one by hand, or import from a URL.",
                        "fr": "Créez-en une à la main ou importez depuis une URL.",
                        "ar": "أنشئ واحدة يدويًا أو استوردها من رابط."},
    "new_recipe":      {"en": "New recipe", "fr": "Nouvelle recette", "ar": "وصفة جديدة"},
    "import_from_url": {"en": "Import from URL", "fr": "Importer depuis une URL", "ar": "استيراد من رابط"},
    "servings_short":  {"en": "serv.", "fr": "pers.", "ar": "حصص"},
    "min":             {"en": "min", "fr": "min", "ar": "دقيقة"},

    # ---- recipe view ----
    "cook_mode":       {"en": "Cook mode", "fr": "Mode cuisine", "ar": "وضع الطبخ"},
    "ingredients":     {"en": "Ingredients", "fr": "Ingrédients", "ar": "المكونات"},
    "instructions":    {"en": "Instructions", "fr": "Instructions", "ar": "التعليمات"},
    "scale":           {"en": "Scale:", "fr": "Quantité :", "ar": "الكمية:"},
    "add_all_shopping":{"en": "Add all to shopping list", "fr": "Tout ajouter aux courses", "ar": "أضف الكل إلى قائمة التسوق"},
    "prep":            {"en": "Prep", "fr": "Préparation", "ar": "التحضير"},
    "cook":            {"en": "Cook", "fr": "Cuisson", "ar": "الطهي"},
    "serves":          {"en": "Serves", "fr": "Pour", "ar": "يكفي لـ"},
    "source":          {"en": "source", "fr": "source", "ar": "المصدر"},
    "delete_recipe":   {"en": "Delete recipe", "fr": "Supprimer la recette", "ar": "حذف الوصفة"},
    "confirm_delete":  {"en": "Delete this recipe?", "fr": "Supprimer cette recette ?", "ar": "حذف هذه الوصفة؟"},

    # ---- edit ----
    "edit_recipe":     {"en": "Edit recipe", "fr": "Modifier la recette", "ar": "تعديل الوصفة"},
    "title":           {"en": "Title", "fr": "Titre", "ar": "العنوان"},
    "servings":        {"en": "Servings", "fr": "Portions", "ar": "الحصص"},
    "prep_min":        {"en": "Prep (min)", "fr": "Préparation (min)", "ar": "التحضير (دقيقة)"},
    "cook_min":        {"en": "Cook (min)", "fr": "Cuisson (min)", "ar": "الطهي (دقيقة)"},
    "tags_csv":        {"en": "Tags (comma separated)", "fr": "Étiquettes (séparées par des virgules)", "ar": "وسوم (مفصولة بفواصل)"},
    "description":     {"en": "Description", "fr": "Description", "ar": "الوصف"},
    "main_photo":      {"en": "Main photo", "fr": "Photo principale", "ar": "الصورة الرئيسية"},
    "add_ingredient":  {"en": "Add ingredient", "fr": "Ajouter un ingrédient", "ar": "إضافة مكون"},
    "steps":           {"en": "Steps", "fr": "Étapes", "ar": "الخطوات"},
    "step_hint":       {"en": "Each step can have a photo and a timer (in seconds).",
                        "fr": "Chaque étape peut avoir une photo et un minuteur (en secondes).",
                        "ar": "يمكن لكل خطوة أن تحتوي على صورة ومؤقت (بالثواني)."},
    "add_step":        {"en": "Add step", "fr": "Ajouter une étape", "ar": "إضافة خطوة"},
    "timer_sec":       {"en": "Timer (sec)", "fr": "Minuteur (s)", "ar": "المؤقت (ثانية)"},
    "photo":           {"en": "Photo", "fr": "Photo", "ar": "صورة"},
    "save_recipe":     {"en": "Save recipe", "fr": "Enregistrer la recette", "ar": "حفظ الوصفة"},
    "describe_step":   {"en": "Describe this step…", "fr": "Décrivez cette étape…", "ar": "صف هذه الخطوة…"},

    # ---- import ----
    "import_intro":    {"en": "Paste a link from a recipe site. RecipeBox reads the structured recipe data and fills everything in. You can add step photos and timers afterwards.",
                        "fr": "Collez un lien d’un site de recettes. RecipeBox lit les données structurées et remplit tout. Vous pourrez ajouter photos et minuteurs ensuite.",
                        "ar": "الصق رابطًا من موقع وصفات. يقرأ صندوق الوصفات البيانات المنظمة ويملأ كل شيء. يمكنك إضافة الصور والمؤقتات لاحقًا."},
    "recipe_url":      {"en": "Recipe URL", "fr": "URL de la recette", "ar": "رابط الوصفة"},
    "import_btn":      {"en": "Import", "fr": "Importer", "ar": "استيراد"},
    "reliable_sites":  {"en": "Reliable sites:", "fr": "Sites fiables :", "ar": "مواقع موثوقة:"},
    "sites_note":      {"en": "If a site blocks scraping, add the recipe manually instead.",
                        "fr": "Si un site bloque l’extraction, ajoutez la recette manuellement.",
                        "ar": "إذا منع الموقع الاستخراج، أضف الوصفة يدويًا."},

    # ---- shopping ----
    "shopping_list":   {"en": "Shopping List", "fr": "Liste de courses", "ar": "قائمة التسوق"},
    "clear_checked":   {"en": "Clear checked", "fr": "Effacer les cochés", "ar": "مسح المحددة"},
    "add_item":        {"en": "Add an item…", "fr": "Ajouter un article…", "ar": "أضف عنصرًا…"},
    "list_empty":      {"en": "Your shopping list is empty.", "fr": "Votre liste de courses est vide.", "ar": "قائمة التسوق فارغة."},
    "list_empty_hint": {"en": "Open any recipe and tap “Add all to shopping list”.",
                        "fr": "Ouvrez une recette et appuyez sur « Tout ajouter aux courses ».",
                        "ar": "افتح أي وصفة واضغط على «أضف الكل إلى قائمة التسوق»."},

    # ---- planner ----
    "this_week":       {"en": "This Week", "fr": "Cette semaine", "ar": "هذا الأسبوع"},
    "breakfast":       {"en": "breakfast", "fr": "petit-déj", "ar": "الفطور"},
    "lunch":           {"en": "lunch", "fr": "déjeuner", "ar": "الغداء"},
    "dinner":          {"en": "dinner", "fr": "dîner", "ar": "العشاء"},
    "add_recipe_dots": {"en": "+ add recipe…", "fr": "+ ajouter une recette…", "ar": "+ أضف وصفة…"},

    # ---- cook mode ----
    "exit":            {"en": "Exit", "fr": "Quitter", "ar": "خروج"},
    "step":            {"en": "Step", "fr": "Étape", "ar": "خطوة"},
    "of":              {"en": "of", "fr": "sur", "ar": "من"},
    "back":            {"en": "Back", "fr": "Précédent", "ar": "السابق"},
    "next":            {"en": "Next", "fr": "Suivant", "ar": "التالي"},
    "done":            {"en": "Done", "fr": "Terminé", "ar": "تم"},
    "start":           {"en": "Start", "fr": "Démarrer", "ar": "ابدأ"},
    "pause":           {"en": "Pause", "fr": "Pause", "ar": "إيقاف"},
    "reset":           {"en": "Reset", "fr": "Réinitialiser", "ar": "إعادة"},

    # ---- language picker / settings ----
    "choose_language": {"en": "Choose your language", "fr": "Choisissez votre langue", "ar": "اختر لغتك"},
    "pick_lang_hint":  {"en": "You can change this later in Settings.",
                        "fr": "Vous pourrez le modifier plus tard dans les Paramètres.",
                        "ar": "يمكنك تغيير ذلك لاحقًا في الإعدادات."},
    "continue":        {"en": "Continue", "fr": "Continuer", "ar": "متابعة"},
    "language":        {"en": "Language", "fr": "Langue", "ar": "اللغة"},
    "settings_saved":  {"en": "Settings saved.", "fr": "Paramètres enregistrés.", "ar": "تم حفظ الإعدادات."},

    # ---- ingredient photo picker ----
    "set_photo":       {"en": "Set photo", "fr": "Définir la photo", "ar": "تعيين صورة"},
    "suggested":       {"en": "Suggested", "fr": "Suggéré", "ar": "مقترح"},
    "icon_library":    {"en": "Icon library", "fr": "Bibliothèque d’icônes", "ar": "مكتبة الأيقونات"},
    "upload_photo":    {"en": "Upload photo", "fr": "Téléverser une photo", "ar": "رفع صورة"},
    "paste_url":       {"en": "Paste image URL", "fr": "Coller l’URL d’une image", "ar": "لصق رابط صورة"},
    "use_url":         {"en": "Use URL", "fr": "Utiliser l’URL", "ar": "استخدام الرابط"},
    "remove_photo":    {"en": "Remove", "fr": "Retirer", "ar": "إزالة"},
    "no_icons":        {"en": "No icons in the library yet.", "fr": "Aucune icône dans la bibliothèque.", "ar": "لا توجد أيقونات بعد."},

    # ---- icon management page ----
    "manage_icons":    {"en": "Ingredient Icons", "fr": "Icônes d’ingrédients", "ar": "أيقونات المكونات"},
    "icon_name":       {"en": "Name (e.g. paprika)", "fr": "Nom (ex. paprika)", "ar": "الاسم (مثل بابريكا)"},
    "icon_file":       {"en": "Image file", "fr": "Fichier image", "ar": "ملف الصورة"},
    "add_icon":        {"en": "Add icon", "fr": "Ajouter une icône", "ar": "إضافة أيقونة"},
    "builtin":         {"en": "built-in", "fr": "intégrée", "ar": "مدمجة"},
    "your_icons":      {"en": "Your icons", "fr": "Vos icônes", "ar": "أيقوناتك"},
    "builtin_icons":   {"en": "Built-in icons", "fr": "Icônes intégrées", "ar": "الأيقونات المدمجة"},
    "icons_intro":     {"en": "Upload ingredient icons here. They appear in the photo picker for every recipe and persist across updates.",
                        "fr": "Téléversez des icônes d’ingrédients ici. Elles apparaissent dans le sélecteur de photo de chaque recette et persistent après les mises à jour.",
                        "ar": "ارفع أيقونات المكونات هنا. تظهر في منتقي الصور لكل وصفة وتبقى بعد التحديثات."},

    # ---- favorites / recipe meta / shopping ----
    "favorites":       {"en": "Favorites", "fr": "Favoris", "ar": "المفضلة"},
    "all_recipes":     {"en": "All", "fr": "Toutes", "ar": "الكل"},
    "add_favorite":    {"en": "Add to favorites", "fr": "Ajouter aux favoris", "ar": "أضف إلى المفضلة"},
    "remove_favorite": {"en": "Remove from favorites", "fr": "Retirer des favoris", "ar": "أزل من المفضلة"},
    "no_favorites":    {"en": "No favorites yet.", "fr": "Aucun favori pour l’instant.", "ar": "لا توجد مفضلات بعد."},
    "difficulty":      {"en": "Difficulty", "fr": "Difficulté", "ar": "الصعوبة"},
    "cuisine":         {"en": "Cuisine", "fr": "Cuisine", "ar": "المطبخ"},
    "diff_none":       {"en": "—", "fr": "—", "ar": "—"},
    "diff_easy":       {"en": "Easy", "fr": "Facile", "ar": "سهل"},
    "diff_medium":     {"en": "Medium", "fr": "Moyen", "ar": "متوسط"},
    "diff_hard":       {"en": "Hard", "fr": "Difficile", "ar": "صعب"},

    # ---- structured ingredient fields ----
    "qty":             {"en": "Qty", "fr": "Qté", "ar": "كمية"},
    "unit":            {"en": "Unit", "fr": "Unité", "ar": "وحدة"},
    "ingredient_name": {"en": "Ingredient", "fr": "Ingrédient", "ar": "المكون"},
    "or":              {"en": "or", "fr": "ou", "ar": "أو"},
}


def t(key: str, lang: str = "en") -> str:
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get("en") or key


def make_translator(lang: str):
    def _t(key: str) -> str:
        return t(key, lang)
    return _t
