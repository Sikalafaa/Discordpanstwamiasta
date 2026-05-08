"""
Walidacja odpowiedzi — zewnętrzne API + lokalna lista dla imion.

Państwo  → REST Countries (dokładne dopasowanie polskiej nazwy)
Miasto   → Nominatim/OpenStreetMap (dokładne dopasowanie nazwy miejsca)
Zwierzę  → Polska Wikipedia — kategorie (Ssaki, Ptaki, Gady, ...)
Roślina  → Polska Wikipedia — kategorie (Rośliny, Drzewa, Kwiaty, ...)
Imię     → lokalna lista names_pl.py (brak dobrego API dla polskich imion)

Timeout / błąd sieci → zawsze False (nigdy nie zaliczamy na kredyt).
Każdy wynik trafia do cache — to samo słowo nie jest sprawdzane dwa razy.
"""

import re
import unicodedata
import asyncio
import logging
import aiohttp

from bot.countries_pl import PANSTWA
from bot.cities_pl    import MIASTA
from bot.names_pl     import IMIONA
from bot.animals_pl   import ZWIERZETA
from bot.plants_pl    import ROSLINY

logger = logging.getLogger("panstwa_bot.validator")

API_TIMEOUT = 5          # sekundy na odpowiedź API
_nominatim_sem = asyncio.Semaphore(1)   # Nominatim wymaga max 1 req/s

_cache: dict[tuple[str, str, str], tuple[bool, str]] = {}


# ── Helpers ────────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    """Małe litery + usuń ogonki. 'ł' obsługiwane ręcznie bo nie dekompozycjonuje przez NFKD."""
    text = text.lower().replace("ł", "l")
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def _is_valid_text(text: str) -> bool:
    cleaned = re.sub(r"['\-\s]", "", text)
    return bool(cleaned) and all(c.isalpha() for c in cleaned)


def _starts_with_letter(text: str, letter: str) -> bool:
    return bool(text) and _norm(text)[0] == _norm(letter)[0]


def _basic_check(name: str, letter: str) -> tuple[bool, str] | None:
    name = name.strip()
    if len(name) < 3:
        return False, "Za krótkie (minimum 3 znaki)"
    if not _starts_with_letter(name, letter):
        return False, f"Nie zaczyna się od '{letter.upper()}'"
    if not _is_valid_text(name):
        return False, "Dozwolone tylko litery"
    return None


def _lookup(name: str, word_set: set[str]) -> bool:
    return _norm(name) in word_set


# ── Zewnętrzne API ─────────────────────────────────────────────────────────

def _exact_match(user_input: str, candidate: str) -> bool:
    """Dokładne dopasowanie po normalizacji — jedyna akceptowalna zgodność."""
    return bool(candidate) and _norm(user_input) == _norm(candidate)


async def _restcountries_check(name: str) -> bool:
    """
    REST Countries — akceptuje tylko jeśli polska nazwa zwróconego kraju
    DOKŁADNIE odpowiada wpisanej nazwie (po normalizacji).
    """
    norm_input = _norm(name)
    headers = {"User-Agent": "PanstwaBot/1.0"}
    timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)

    def _pol_names(country: dict) -> list[str]:
        pol = country.get("translations", {}).get("pol", {})
        return [
            _norm(pol.get("common", "")),
            _norm(pol.get("official", "")),
            _norm(country.get("name", {}).get("common", "")),
            _norm(country.get("name", {}).get("official", "")),
        ]

    try:
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as s:
            # Szukaj po tłumaczeniu
            async with s.get(f"https://restcountries.com/v3.1/translation/{name}") as r:
                if r.status == 200:
                    for country in await r.json():
                        if norm_input in _pol_names(country):
                            return True
            # Szukaj po angielskiej nazwie (pełne dopasowanie)
            async with s.get(
                f"https://restcountries.com/v3.1/name/{name}",
                params={"fullText": "true"}
            ) as r:
                if r.status == 200:
                    for country in await r.json():
                        if norm_input in _pol_names(country):
                            return True
    except Exception as e:
        logger.debug(f"[API] RestCountries błąd dla '{name}': {e}")
    return False


async def _nominatim_check(name: str) -> bool:
    """
    Nominatim (OpenStreetMap) — akceptuje tylko jeśli pierwsza część
    display_name DOKŁADNIE odpowiada wpisanej nazwie (po normalizacji).
    Semaforem ograniczamy do 1 req/s zgodnie z polityką użytkowania.
    """
    params = {
        "q": name,
        "format": "json",
        "limit": 5,
        "accept-language": "pl",
        "namedetails": "1",
    }
    headers = {"User-Agent": "PanstwaBot/1.0 (Discord game bot)"}
    timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)
    norm_input = _norm(name)

    async with _nominatim_sem:
        try:
            async with aiohttp.ClientSession(headers=headers, timeout=timeout) as s:
                async with s.get(
                    "https://nominatim.openstreetmap.org/search",
                    params=params
                ) as r:
                    if r.status != 200:
                        return False
                    data = await r.json()
                    for item in data:
                        place_class = item.get("class", "")
                        place_type  = item.get("type", "")

                        # Zbierz wszystkie warianty nazwy
                        namedetails = item.get("namedetails", {})
                        candidates = {
                            _norm(v) for v in [
                                item.get("name", ""),
                                namedetails.get("name", ""),
                                namedetails.get("name:pl", ""),
                                namedetails.get("name:en", ""),
                                namedetails.get("alt_name", ""),
                                namedetails.get("official_name", ""),
                                namedetails.get("official_name:pl", ""),
                                item.get("display_name", "").split(",")[0].strip(),
                            ] if v
                        }

                        # Wymagamy dokładnego dopasowania do co najmniej jednej nazwy
                        if norm_input not in candidates - {""}:
                            continue

                        if place_class == "place" and place_type in {
                            "city", "town", "village", "municipality",
                            "borough", "suburb", "quarter", "hamlet",
                            "administrative",
                        }:
                            return True
                        if place_class == "boundary" and place_type == "administrative":
                            return True
        except Exception as e:
            logger.debug(f"[API] Nominatim błąd dla '{name}': {e}")
        await asyncio.sleep(1)
    return False


_ANIMAL_CAT_KEYWORDS = {
    "ssaki", "ptaki", "gady", "płazy", "ryby", "owady", "pajęczaki",
    "zwierzęta", "kręgowce", "bezkręgowce", "mięczaki", "skorupiaki",
    "robaki", "pierścienice", "szkarłupnie", "gąbki",
}

_PLANT_CAT_KEYWORDS = {
    "rośliny", "drzewa", "krzewy", "kwiaty", "zioła", "trawy",
    "grzyby", "glony", "mchy", "paprocie", "drzewa owocowe",
    "rośliny ozdobne", "rośliny lecznicze", "rośliny jadalne",
}


async def _wikipedia_category_check(name: str, cat_keywords: set[str]) -> bool:
    """
    Polska Wikipedia — pobiera kategorie artykułu i sprawdza
    czy któraś zawiera słowo kluczowe dla zwierzęcia/rośliny.

    Sprawdza też że tytuł artykułu (po ewentualnym redirect) zaczyna się
    od wpisanej nazwy — zapobiega fałszywym trafień przez redirect.
    """
    params = {
        "action": "query",
        "titles": name,
        "prop": "categories|info",
        "format": "json",
        "redirects": 1,
        "cllimit": 50,
        "inprop": "displaytitle",
    }
    headers = {"User-Agent": "PanstwaBot/1.0"}
    timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)
    norm_input = _norm(name)
    try:
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as s:
            async with s.get(
                "https://pl.wikipedia.org/w/api.php",
                params=params,
            ) as r:
                if r.status != 200:
                    return False
                data = await r.json()
                query = data.get("query", {})

                # Sprawdź czy Wikipedia przekierowała z wpisanej nazwy
                redirects = {r["from"].lower(): r["to"] for r in query.get("redirects", [])}
                has_redirect_from_input = name.lower() in redirects

                pages = query.get("pages", {})
                for page in pages.values():
                    if page.get("pageid", -1) == -1:
                        return False  # strona nie istnieje

                    # Jeśli był redirect z wpisanej nazwy (np. "Panda" → "Panda wielka"),
                    # to Wikipedia potwierdza że ta nazwa jest poprawna — nie sprawdzamy tytułu.
                    # Jeśli nie było redirecta, tytuł musi pasować dokładnie.
                    if not has_redirect_from_input:
                        page_title = _norm(page.get("title", ""))
                        if page_title != norm_input and not page_title.startswith(norm_input + " "):
                            return False

                    for cat in page.get("categories", []):
                        cat_name = cat.get("title", "").lower()
                        if any(kw in cat_name for kw in cat_keywords):
                            return True
    except Exception as e:
        logger.debug(f"[API] Wikipedia categories błąd dla '{name}': {e}")
    return False


# ── Walidatory ─────────────────────────────────────────────────────────────

async def validate_country(name: str, letter: str) -> tuple[bool, str]:
    fail = _basic_check(name, letter)
    if fail:
        return fail
    if _lookup(name, PANSTWA):
        return True, f"✓ {name}"
    if await _restcountries_check(name):
        return True, f"✓ {name}"
    return False, f"'{name}' nie jest rozpoznawanym państwem"


async def validate_city(name: str, letter: str) -> tuple[bool, str]:
    fail = _basic_check(name, letter)
    if fail:
        return fail
    if _lookup(name, MIASTA):
        return True, f"✓ {name}"
    if await _nominatim_check(name):
        return True, f"✓ {name}"
    return False, f"'{name}' nie jest rozpoznawanym miastem"


async def validate_name(name: str, letter: str) -> tuple[bool, str]:
    fail = _basic_check(name, letter)
    if fail:
        return fail
    # Imiona — brak API, lokalna lista zawsze aktywna
    if _lookup(name, IMIONA):
        return True, f"✓ {name}"
    return False, f"'{name}' nie jest polskim imieniem"


async def validate_animal(name: str, letter: str) -> tuple[bool, str]:
    fail = _basic_check(name, letter)
    if fail:
        return fail
    # Lokalna lista — potoczne polskie nazwy (błyskawiczne, bez sieci)
    if _lookup(name, ZWIERZETA):
        return True, f"✓ {name}"
    # Fallback — Wikipedia (nazwy spoza lokalnej listy)
    if await _wikipedia_category_check(name, _ANIMAL_CAT_KEYWORDS):
        return True, f"✓ {name}"
    return False, f"'{name}' nie jest rozpoznawanym zwierzęciem"


async def validate_plant(name: str, letter: str) -> tuple[bool, str]:
    fail = _basic_check(name, letter)
    if fail:
        return fail
    # Lokalna lista — potoczne polskie nazwy (błyskawiczne, bez sieci)
    if _lookup(name, ROSLINY):
        return True, f"✓ {name}"
    # Fallback — Wikipedia (nazwy spoza lokalnej listy)
    if await _wikipedia_category_check(name, _PLANT_CAT_KEYWORDS):
        return True, f"✓ {name}"
    return False, f"'{name}' nie jest rozpoznawaną rośliną"


# ── Dispatcher z cache ─────────────────────────────────────────────────────

_HANDLERS = {
    "Państwo": validate_country,
    "Miasto":  validate_city,
    "Imię":    validate_name,
    "Zwierzę": validate_animal,
    "Roślina": validate_plant,
}


async def validate_answer(category: str, answer: str, letter: str) -> tuple[bool, str]:
    answer = answer.strip()
    if not answer:
        return False, "Brak odpowiedzi"

    fail = _basic_check(answer, letter)
    if fail:
        return fail

    cache_key = (category, _norm(answer), _norm(letter))
    if cache_key in _cache:
        return _cache[cache_key]

    handler = _HANDLERS.get(category)
    if handler is None:
        return False, f"Nieznana kategoria: '{category}'"

    result = await handler(answer, letter)
    _cache[cache_key] = result
    return result


def clear_cache() -> None:
    _cache.clear()


async def validate_all_answers(raw_answers: dict, letter: str) -> dict:
    """
    raw_answers : {discord_id: {category: answer_str}}
    returns     : {discord_id: {category: (answer_str, is_valid, reason)}}
    """
    tasks: list = []
    keys:  list = []

    for discord_id, cat_answers in raw_answers.items():
        for category, answer in cat_answers.items():
            tasks.append(validate_answer(category, answer, letter))
            keys.append((discord_id, category, answer))

    results = await asyncio.gather(*tasks)

    validated: dict = {}
    for (discord_id, category, answer), (is_valid, reason) in zip(keys, results):
        validated.setdefault(discord_id, {})[category] = (answer, is_valid, reason)

    return validated
