"""DeepL translation helper (free tier).

Free keys end with ':fx' and use the api-free endpoint. We translate in batches
(DeepL accepts multiple 'text' params) and fail gracefully so a missing key or an
unsupported language never breaks the app.
"""
import httpx

# DeepL target-language codes we support in the UI
# (DeepL uses e.g. FR, AR, EN-US). Arabic support depends on DeepL availability.
DEEPL_TARGET = {
    "fr": "FR",
    "ar": "AR",
    "en": "EN-US",
}


def _endpoint(key: str) -> str:
    # free keys end with ":fx"
    if key.strip().endswith(":fx"):
        return "https://api-free.deepl.com/v2/translate"
    return "https://api.deepl.com/v2/translate"


def translate_debug(texts, target_lang, key, source_lang=None):
    """Like translate_batch but returns the raw DeepL response for diagnosis."""
    target = DEEPL_TARGET.get(target_lang, target_lang)
    data = [("target_lang", target)]
    if source_lang:
        src = DEEPL_TARGET.get(source_lang, source_lang).split("-")[0]
        data.append(("source_lang", src))
    for t in texts:
        data.append(("text", t if t else " "))
    try:
        resp = httpx.post(_endpoint(key), data=data,
                          headers={"Authorization": f"DeepL-Auth-Key {key}"},
                          timeout=30.0)
        return {
            "endpoint": _endpoint(key),
            "sent_target": target,
            "status": resp.status_code,
            "body": resp.text[:500],
        }
    except Exception as e:
        return {"error": str(e), "endpoint": _endpoint(key), "sent_target": target}


def translate_batch(texts, target_lang, key, source_lang=None):
    """Translate a list of strings to target_lang. Returns a list same length.

    On any failure (no key, network, unsupported lang) returns the originals so
    callers can store source text as a safe fallback.
    """
    if not key or not texts:
        return list(texts)
    target = DEEPL_TARGET.get(target_lang)
    if not target:
        return list(texts)
    data = [("target_lang", target)]
    if source_lang:
        src = DEEPL_TARGET.get(source_lang, source_lang).split("-")[0]
        data.append(("source_lang", src))
    for t in texts:
        data.append(("text", t if t else " "))
    try:
        resp = httpx.post(_endpoint(key), data=data,
                          headers={"Authorization": f"DeepL-Auth-Key {key}"},
                          timeout=30.0)
        resp.raise_for_status()
        out = resp.json().get("translations", [])
        result = [o.get("text", "") for o in out]
        if len(result) == len(texts):
            return result
        return list(texts)
    except Exception:
        return list(texts)


def verify_key(key):
    """Return (ok, message). Checks usage endpoint."""
    if not key:
        return False, "No key"
    base = ("https://api-free.deepl.com" if key.strip().endswith(":fx")
            else "https://api.deepl.com")
    try:
        r = httpx.get(f"{base}/v2/usage",
                      headers={"Authorization": f"DeepL-Auth-Key {key}"}, timeout=15.0)
        if r.status_code == 200:
            return True, "OK"
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)
