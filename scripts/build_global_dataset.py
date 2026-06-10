from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
ES_DIR = BASE_DIR / "ES_MARKET"
PT_DIR = BASE_DIR / "PT_MARKET"

OUT_XLSX = BASE_DIR / "STOCK_UNIFICADO_GLOBAL.xlsx"
OUT_CSV = BASE_DIR / "STOCK_UNIFICADO_GLOBAL.csv"
MASTER_XLSX = BASE_DIR / "FICHERO_MAESTRO.xlsx"

UNIFIED_COLUMNS = [
    "Market",
    "Brand",
    "Model",
    "Body_Type",
    "Fuel_Type",
    "Year",
    "Available_Date",
    "Published_Date",
    "Dealer",
    "City",
    "Province",
    "Type",
    "Version",
    "Ext_Color",
    "Int_Color",
    "RRP_EUR",
    "Monthly_EUR",
    "APR_pct",
    "Availability",
    "Engine_Raw",
    "Segment",
    "High_Performance",
    "URL",
]


BRAND_PREFIX = re.compile(r"^(Mercedes(?:-Benz)?|BMW|Audi|MINI)\s+", re.IGNORECASE)
BMW_SERIES_KEY_RE = re.compile(
    r"^(?:serie|series)\s+([1-8])\b|^([1-8])\s+(?:series?|active tourer|gran tourer|gran coupe|coup[eé]|cabrio|berlina|touring)\b",
    re.IGNORECASE,
)
MERCEDES_CLASS_MAP = {
    "a": "Clase A",
    "b": "Clase B",
    "c": "Clase C",
    "e": "Clase E",
    "s": "Clase S",
    "g": "Clase G",
    "t": "Clase T",
    "v": "Clase V",
    "cla": "Clase CLA",
    "cle": "Clase CLE",
    "cls": "Clase CLS",
    "gla": "Clase GLA",
    "glb": "Clase GLB",
    "glc": "Clase GLC",
    "gle": "Clase GLE",
    "gls": "Clase GLS",
    "sl": "Clase SL",
}
MERCEDES_CLASS_RE = re.compile(
    r"^(?:clase|class)\s+([a-z0-9]+)$|^([a-z0-9]+)\s*[- ]?\s*class$",
    re.IGNORECASE,
)
AUDI_MODEL_PREFIXES = [
    "A1 Sportback", "A1 allstreet", "A3 Sportback", "A3 Limousine", "A3 allstreet",
    "A5 Avant", "A5 Limousine", "A5", "A6 Avant e-tron", "A6 Sportback e-tron",
    "A6 Avant", "A6 Limousine", "Q2", "Q3 Sportback e-hybrid", "Q3 SUV e-hybrid",
    "Q3 Sportback", "Q3 SUV", "Q3", "Q4 Sportback e-tron", "Q4 SUV e-tron",
    "Q5 Sportback", "Q5 SUV", "Q5", "Q6 Sportback e-tron", "Q6 SUV e-tron", "Q7", "Q8",
]


ES_PROVINCES_BY_CITY = {
    "madrid": "Madrid",
    "barcelona": "Barcelona",
    "valencia": "Valencia",
    "sevilla": "Sevilla",
    "zaragoza": "Zaragoza",
    "malaga": "Malaga",
    "murcia": "Murcia",
    "palma": "Baleares",
    "bilbao": "Vizcaya",
    "alicante": "Alicante",
    "cordoba": "Cordoba",
    "valladolid": "Valladolid",
    "vigo": "Pontevedra",
    "gijon": "Asturias",
    "hospitalet": "Barcelona",
    "vitoria": "Alava",
    "coruna": "A Coruna",
    "granada": "Granada",
    "elche": "Alicante",
    "oviedo": "Asturias",
    "badalona": "Barcelona",
    "cartagena": "Murcia",
    "terrassa": "Barcelona",
    "jerez": "Cadiz",
    "sabadell": "Barcelona",
    "santander": "Cantabria",
    "burgos": "Burgos",
    "castellon": "Castellon",
    "almeria": "Almeria",
    "salamanca": "Salamanca",
    "logrono": "La Rioja",
    "huelva": "Huelva",
    "leon": "Leon",
    "tarragona": "Tarragona",
    "cadiz": "Cadiz",
    "jaen": "Jaen",
    "ourense": "Ourense",
    "girona": "Girona",
    "lugo": "Lugo",
    "caceres": "Caceres",
    "toledo": "Toledo",
    "badajoz": "Badajoz",
    "pamplona": "Navarra",
    "pontevedra": "Pontevedra",
    "guadalajara": "Guadalajara",
    "segovia": "Segovia",
    "lerida": "Lleida",
    "lleida": "Lleida",
    "guipuzcoa": "Guipuzcoa",
    "san sebastian": "Guipuzcoa",
    "sant boi de llobregat": "Barcelona",
    "jerez de la frontera": "Cadiz",
    "leganes": "Madrid",
    "rivas vaciamadrid": "Madrid",
    "quart de poblet": "Valencia",
    "albacete": "Albacete",
    "san juan de alicante": "Alicante",
    "xativa": "Valencia",
    "perillo oleiros": "A Coruna",
    "colmenar viejo": "Madrid",
    "algeciras": "Cadiz",
    "lugones": "Asturias",
    "vera": "Almeria",
    "santiago de compostela": "A Coruna",
    "a coruna": "A Coruna",
    "ibiza": "Baleares",
    "avila": "Avila",
    "alcazar de san juan": "Ciudad Real",
    "trobajo del camino": "Leon",
    "alcorcon": "Madrid",
    "villares de la reina": "Salamanca",
    "orkoien": "Navarra",
    "motril": "Granada",
    "orense": "Ourense",
    "eibar": "Guipuzcoa",
    "sant cugat": "Barcelona",
    "palma de mallorca": "Baleares",
    "torrevieja": "Alicante",
    "castellon de la plana": "Castellon",
    "getafe": "Madrid",
    "huesca": "Huesca",
    "leioa": "Vizcaya",
    "tolosa": "Guipuzcoa",
    "tortosa": "Tarragona",
    "tudela": "Navarra",
    "marbella": "Malaga",
    "zamora": "Zamora",
    "braga": "Braga",
    "lisboa": "Lisboa",
    "sintra": "Lisboa",
    "maia": "Porto",
    "porto": "Porto",
    "coimbra": "Coimbra",
    "matosinhos": "Porto",
    "vila nova de gaia": "Porto",
    "carnaxide": "Lisboa",
    "setubal": "Setubal",
    "cascais": "Lisboa",
    "aveiro": "Aveiro",
    "varzea de santarem": "Santarem",
    "faro": "Faro",
    "almada": "Setubal",
    "guarda": "Guarda",
    "torres vedras": "Lisboa",
    "amadora": "Lisboa",
    "penafiel": "Porto",
    "montijo": "Setubal",
    "loures": "Lisboa",
    "funchal": "Madeira",
    "santarem": "Santarem",
    "ponta delgada": "Azores",
    "guimaraes": "Braga",
    "leiria": "Leiria",
    "evora": "Evora",
    "gaia": "Porto",
    "vila real": "Vila Real",
}


def norm_key(value: object) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^0-9A-Za-z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def clean_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).replace("\xa0", " ").strip()
    return re.sub(r"\s+", " ", text).strip()


def normalize_offer_url(url: object, brand: str, market: str) -> str:
    clean_url = clean_text(url)
    if brand == "Audi" and market == "ES" and "entry.audi.com" in clean_url:
        vehicle_id = parse_qs(urlparse(clean_url).query).get("id", [""])[0]
        if vehicle_id:
            return "https://www.audi.es/es/buscador-de-stock-nuevo/details/?vehicleid=" + vehicle_id
    return clean_url


def clean_model(value: object, brand: str = "") -> str:
    model = clean_text(value)
    if not model:
        return ""
    model = BRAND_PREFIX.sub("", model).strip()
    key = norm_key(model)

    bm = BMW_SERIES_KEY_RE.match(key)
    if bm:
        return f"Serie {bm.group(1) or bm.group(2)}"
    if brand == "BMW":
        bmw = re.match(r"^(i?x[1-7]|m[1-8])\b", key, re.IGNORECASE)
        if bmw:
            return bmw.group(1).upper()

    mc = MERCEDES_CLASS_RE.match(key)
    if mc:
        code = (mc.group(1) or mc.group(2) or "").lower()
        return MERCEDES_CLASS_MAP.get(code, f"Clase {code.upper()}")
    if key in MERCEDES_CLASS_MAP:
        return MERCEDES_CLASS_MAP[key]
    if brand == "Mercedes-Benz":
        for code in sorted(MERCEDES_CLASS_MAP, key=len, reverse=True):
            if key == code or key.startswith(code + " "):
                return MERCEDES_CLASS_MAP[code]
        eq = re.match(r"^(eqa|eqb|eqc|eqe|eqs)\b", key, re.IGNORECASE)
        if eq:
            return eq.group(1).upper()

    if brand == "Audi":
        model_key = norm_key(model)
        for prefix in sorted(AUDI_MODEL_PREFIXES, key=len, reverse=True):
            if model_key == norm_key(prefix) or model_key.startswith(norm_key(prefix) + " "):
                return prefix

    return model.replace("Série", "Serie")


def normalize_fuel(*values: object) -> str:
    key = norm_key(" ".join(clean_text(value) for value in values if clean_text(value)))
    if not key:
        return ""
    if any(x in key for x in [
        "plug", "phev", "hibrido enchufable", "hybrid plug", "tfsi e", "tfsie",
        "e hybrid", "ehybrid", "e hybrid", "e hibrid", "300 de", "300 e",
        "350 de", "400 e", "450 e", "500 e", "550 e", "580 e", "250 e",
        "45 tfsie", "50 tfsie", "55 tfsie", "60 tfsie",
    ]):
        return "PHEV"
    if any(x in key for x in ["electric", "electrico", "eletrico", "elctrico", "bev", "e tron", "etron"]):
        return "BEV"
    if "mhev" in key or "mild" in key or "hibrido suave" in key:
        return "ICE"
    if "hybrid" in key or "hibrid" in key or "hev" in key:
        return "ICE"
    return "ICE"


def normalize_brand(value: object) -> str:
    key = norm_key(value)
    if key in {"mercedes", "mercedes benz", "mercedes-benz"}:
        return "Mercedes"
    if key == "bmw":
        return "BMW"
    if key == "audi":
        return "Audi"
    return clean_text(value)


def master_model(value: object, brand: str = "", version: object = "") -> str:
    model = clean_model(value, "Mercedes-Benz" if normalize_brand(brand) == "Mercedes" else normalize_brand(brand))
    key = norm_key(model)
    version_key = norm_key(version)
    full_key = f"{key} {version_key}".strip()
    brand = normalize_brand(brand)

    if brand == "Audi":
        if "etron gt" in full_key or "e tron gt" in full_key:
            return "e-tron GT"
        if key.startswith(("rs 3", "rs3", "s3")):
            return "A3"
        if key.startswith(("s5", "rs5")):
            return "A5"
        if key.startswith(("sq5")):
            return "Q5"
        if "q3 sportback" in full_key:
            return "Q3 Sportback"
        if "q5 sportback" in full_key:
            return "Q5 Sportback"
        if "q6 sportback" in full_key:
            return "Q6 e-tron Sportback"
        if "q4 sportback" in full_key:
            return "Q4 Sportback e-tron"
        if key.startswith(("q6", "sq6")):
            return "Q6 e-tron"
        if key.startswith("q4"):
            return "Q4 e-tron"
        for prefix in ["A1", "A3", "A4", "A5", "A6", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT"]:
            if key.startswith(norm_key(prefix)):
                return prefix

    if brand == "BMW":
        if key == "ix3":
            return "iX3"
        if key == "ix2":
            return "iX2"
        if key == "ix1":
            return "iX1"
        if key == "ix":
            return "iX"
        m = re.match(r"^m([1-8])\b", key)
        if m:
            return f"Serie {m.group(1)}"
        for prefix in ["Serie 1", "Serie 2", "Serie 3", "Serie 4", "Serie 5", "Serie 7", "Serie 8", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "XM", "Z4", "i4", "i5", "i7"]:
            if key.startswith(norm_key(prefix)):
                return prefix

    if brand == "Mercedes":
        if "amg gt" in full_key:
            return "AMG GT"
        if "mercedes amg a" in full_key:
            return "Clase A"
        if "mercedes amg c" in full_key:
            return "Clase C"
        if "mercedes amg e" in full_key or re.match(r"^e\d", key):
            return "Clase E"
        if "mercedes amg g " in f"{full_key} ":
            return "Clase G"
        if "glc" in full_key and ("coupe" in full_key or "coupe" in version_key or "coup" in full_key):
            return "Clase GLC Coupe"
        if "gle" in full_key and ("coupe" in full_key or "coupe" in version_key or "coup" in full_key):
            return "Clase GLE Coupe"
        for code, out in [
            ("cla", "Clase CLA"), ("cle", "Clase CLE"), ("gla", "Clase GLA"),
            ("glb", "Clase GLB"), ("glc", "Clase GLC"), ("gle", "Clase GLE"),
            ("gls", "Clase GLS"), ("eqa", "EQA"), ("eqb", "EQB"),
            ("eqe", "EQE"), ("eqs", "EQS"), ("eqt", "EQT"), ("eqv", "EQV"),
        ]:
            if key == code or key.startswith(code + " ") or version_key.startswith(code + " ") or re.match(rf"^{code}\d", key) or re.match(rf"^{code}\d", version_key) or f" {code} " in f" {full_key} ":
                return out
        for prefix in ["Clase A", "Clase B", "Clase C", "Clase E", "Clase G", "Clase S", "Clase SL", "Clase T", "Clase V", "Citan", "Vito", "Marco Polo", "Sprinter 200", "Sprinter 300", "Sprinter 400", "Sprinter 500", "e-Sprinter", "eCitan", "eVito"]:
            if key.startswith(norm_key(prefix)) or version_key.startswith(norm_key(prefix)):
                return prefix
        if re.match(r"^[acegst]\b", version_key):
            return {"a": "Clase A", "c": "Clase C", "e": "Clase E", "g": "Clase G", "s": "Clase S", "t": "Clase T"}[version_key[0]]

    return model


def normalize_body(model: object, body: object = "", version: object = "") -> str:
    model_key = norm_key(model)
    body_key = norm_key(body)
    version_key = norm_key(version)
    key = " ".join([model_key, body_key, version_key]).strip()

    suv_tokens = [
        "suv", "sport activity vehicle", "sports activity vehicle", "sav",
        "all terrain", "all-terrain", "off road", "off-road",
    ]
    suv_prefixes = (
        "q2", "q3", "q4", "q5", "q6", "q7", "q8",
        "x1", "x2", "x3", "x4", "x5", "x6", "x7", "xm", "ix",
        "gla", "glb", "glc", "gle", "gls", "eqa", "eqb", "eqc",
        "clase gla", "clase glb", "clase glc", "clase gle", "clase gls", "clase g",
        "mercedes-amg gla", "mercedes-amg glc", "mercedes-amg gle", "mercedes-amg gls", "mercedes-amg g",
    )

    if any(x in key for x in ["roadster"]):
        return "ROADSTER"
    if any(x in key for x in ["cabrio", "convertible"]):
        return "CABRIO"
    if any(x in key for x in suv_tokens) or model_key.startswith(suv_prefixes):
        return "SAV"
    if any(x in key for x in ["furgon", "furgao", "furgón", "van", "sprinter", "citan", "vito", "marco polo", "chasis cabina"]):
        return "TRANSPORTER"
    if any(x in key for x in ["avant", "touring", "estate", "familiar", "station", "shooting brake", "allstreet", "wagon", "break"]):
        return "ESTATE"
    if any(x in key for x in ["coupe", "coup", "gran turismo", "gran_turismo"]):
        return "COUPE"
    if any(x in key for x in ["sedan", "berlina", "limousine", "saloon"]):
        return "SEDAN"
    if any(x in key for x in ["sportback", "sportshatch", "sports hatch", "sports_hatch", "hatch", "hach", "compact", "5-door", "5 door", "compacto"]):
        return "HACH 5P"

    if model_key.startswith(("clase b", "clase v", "eqv", "serie 2")) and any(x in key for x in ["active tourer", "gran tourer", "tourer", "mpv"]):
        return "MPV"
    if model_key.startswith(("a1", "a3", "serie 1", "clase a")):
        return "HACH 5P"
    if model_key.startswith(("a5 avant", "a6 avant", "i5 touring")):
        return "ESTATE"
    if model_key.startswith(("a3 limousine", "a5 limousine", "a6", "serie 3", "serie 5", "clase c", "clase e", "clase s", "eqe", "eqs")):
        return "SEDAN"
    if model_key.startswith(("a5", "s e-tron gt", "serie 2", "serie 4", "serie 8", "clase cla", "clase cle", "clase cls", "clase sl")):
        return "COUPE"
    if model_key.startswith(("q2", "q3", "q4", "q5", "q6", "q7", "q8", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "xm", "ix", "clase g", "clase gla", "clase glb", "clase glc", "clase gle", "clase gls", "eqa", "eqb")):
        return "SAV"

    return "SEDAN"


def to_number(value: object):
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = re.sub(r"[^\d,.-]", "", str(value)).strip()
    if not text:
        return None
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def first(row: pd.Series, *cols: str):
    for col in cols:
        if col in row and pd.notna(row[col]) and str(row[col]).strip() != "":
            return row[col]
    return ""


def province_from_city(city: object) -> str:
    return ES_PROVINCES_BY_CITY.get(norm_key(city), "")


def read_excel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_excel(path, engine="openpyxl")


def _mode(values: list[str]) -> str:
    clean = [v for v in values if v]
    if not clean:
        return ""
    return pd.Series(clean).mode().iloc[0]


_BMW_CHASSIS_CODE_RE = re.compile(r"^[a-z]\d{2,3}(lci)?$")
_DRIVETRAIN_PREFIX_RE = re.compile(r"^(x|s)drive(\w+)$")
_DRIVETRAIN_TOKENS = {"xdrive", "sdrive", "quattro", "4matic"}


def _strip_internal_codes(key: str) -> str:
    """Drop internal chassis codes (e.g. U11, F48LCI, E84) and drivetrain
    prefixes (xDrive/sDrive/quattro/4MATIC) so version strings compare on the
    meaningful engine/trim tokens only."""
    out = []
    for token in key.split():
        if _BMW_CHASSIS_CODE_RE.match(token):
            continue
        m = _DRIVETRAIN_PREFIX_RE.match(token)
        if m:
            out.append(m.group(2))
            continue
        if token in _DRIVETRAIN_TOKENS:
            continue
        out.append(token)
    return " ".join(out)


def _version_match_score(source_version: str, master_version: str) -> int:
    source_key = _strip_internal_codes(norm_key(source_version))
    master_key = _strip_internal_codes(norm_key(master_version))
    if not source_key or not master_key:
        return 0
    if source_key == master_key:
        return 10000 + len(master_key)
    if master_key in source_key or source_key in master_key:
        return 1000 + min(len(source_key), len(master_key))
    source_tokens = set(source_key.split())
    master_tokens = set(master_key.split())
    if len(master_tokens) >= 2 and master_tokens.issubset(source_tokens):
        return 100 + len(master_tokens)
    return 0


def load_master_catalog():
    if not MASTER_XLSX.exists():
        print(f"Warning: master catalog not found: {MASTER_XLSX}")
        return {}, {}, {}, {}

    master = pd.read_excel(MASTER_XLSX, engine="openpyxl")
    exact: dict[tuple[str, str, str], dict[str, str]] = {}
    by_model: dict[tuple[str, str], list[tuple[str, dict[str, str]]]] = {}
    segment_values: dict[tuple[str, str], list[str]] = {}
    hp_values: dict[tuple[str, str], list[str]] = {}

    for _, row in master.iterrows():
        brand = normalize_brand(row.get("Brand", ""))
        model = master_model(row.get("Model", ""), brand, row.get("Version", ""))
        model_key = norm_key(model)
        version = clean_text(row.get("Version", ""))
        version_key = norm_key(version)
        if not brand or not model_key:
            continue
        entry = {
            "Segment": clean_text(row.get("Segment", "")),
            "High_Performance": clean_text(row.get("High_Performance", "")),
        }
        exact[(brand, model_key, version_key)] = entry
        by_model.setdefault((brand, model_key), []).append((version, entry))
        segment_values.setdefault((brand, model_key), []).append(entry["Segment"])
        hp_values.setdefault((brand, model_key), []).append(entry["High_Performance"])

    model_segment = {key: _mode(values) for key, values in segment_values.items()}
    model_hp = {key: _mode(values) for key, values in hp_values.items()}
    print(f"Loaded master catalog: {len(master)} rows from {MASTER_XLSX.name}")
    return exact, by_model, model_segment, model_hp


def enrich_from_master(df: pd.DataFrame) -> pd.DataFrame:
    exact, by_model, model_segment, model_hp = load_master_catalog()
    if not exact:
        df["Segment"] = ""
        df["High_Performance"] = ""
        return df

    segments: list[str] = []
    high_perf: list[str] = []
    for _, row in df.iterrows():
        brand = normalize_brand(row.get("Brand", ""))
        model_key = norm_key(row.get("Model", ""))
        version = clean_text(row.get("Version", ""))
        version_key = norm_key(version)
        model_lookup = (brand, model_key)
        entry = exact.get((brand, model_key, version_key))

        best_entry = entry
        if best_entry is None:
            best_score = 0
            for master_version, candidate in by_model.get(model_lookup, []):
                score = _version_match_score(version, master_version)
                if score > best_score:
                    best_score = score
                    best_entry = candidate

        segments.append(
            clean_text((best_entry or {}).get("Segment", ""))
            or model_segment.get(model_lookup, "")
        )
        high_perf.append(
            clean_text((best_entry or {}).get("High_Performance", ""))
            or model_hp.get(model_lookup, "")
            or "Standard"
        )

    df["Segment"] = segments
    df["High_Performance"] = high_perf
    return df


_PLACEHOLDER_VERSION_RE = re.compile(r"^\d+(\.\d+)?$")


def _derive_version(row: pd.Series, brand_norm: str, raw_version: str) -> str:
    """Some Audi ES rows have meaningless numeric placeholders ("1", "2", "0")
    in the Versión column. The real descriptor (trim + engine + body) lives in
    the Modelo column instead, e.g. "Audi A1 Sportback Advanced 30 TFSI 85 kW
    (116 CV) 6 vel." -> "A1 Sportback Advanced 30 TFSI 85 kW (116 CV) 6 vel."
    """
    if brand_norm != "Audi" or not _PLACEHOLDER_VERSION_RE.match(str(raw_version).strip()):
        return raw_version
    modelo = clean_text(first(row, "Modelo", "Model"))
    modelo = re.sub(r"^audi\s+", "", modelo, flags=re.IGNORECASE)
    return modelo or raw_version


def normalize_rows(path: Path, brand: str, market: str) -> list[dict]:
    df = read_excel(path)
    rows: list[dict] = []
    for _, row in df.iterrows():
        raw_model = first(row, "Carline", "Model Group", "Modelo_norm", "Model", "Modelo", "model")
        brand_norm = normalize_brand(brand)
        version = clean_text(_derive_version(row, brand_norm, first(row, "Version", "Versión", "version")))
        model = master_model(raw_model, brand_norm, version)
        if not model:
            continue

        body = normalize_body(model, first(row, "Body_Type", "Carrocería", "Carroceria", "Body", "body"), version)
        engine = first(row, "Fuel_Type", "Fuel_type", "Fuel", "Combustible", "Motor/Combustible", "Engine_Raw", "Engine")
        city = clean_text(first(row, "City", "Ciudad", "city"))
        province = clean_text(first(row, "Province", "Provincia", "province")) or province_from_city(city)
        rrp = to_number(first(row, "RRP_EUR", "PVP (€)", "PVP (EUR)", "RRP (EUR)", "Base Price (EUR)", "Price (EUR)"))
        monthly = to_number(first(row, "Monthly_EUR", "Cuota/mes (€)", "Cuota/mes (EUR)", "Monthly Rate (EUR)", "Monthly (EUR)"))
        apr = to_number(first(row, "APR_pct", "TAE (%)", "APR (%)"))
        year = to_number(first(row, "Year", "Año", "Ano"))

        url = normalize_offer_url(first(row, "URL", "URL Coche", "Car URL"), brand_norm, market)

        rows.append(
            {
                "Market": market,
                "Brand": brand_norm,
                "Model": model,
                "Body_Type": body,
                "Fuel_Type": normalize_fuel(engine, version, model),
                "Year": int(year) if year else None,
                "Available_Date": clean_text(first(row, "Available_Date", "Fecha", "Fecha Disponible", "Date")),
                "Published_Date": clean_text(first(row, "Published_Date", "Published Date", "Publication_Date", "Fecha Publicacion", "Fecha Publicación", "Listing_Date", "Online_Since")),
                "Dealer": clean_text(first(row, "Dealer", "Concesionario")),
                "City": city,
                "Province": province,
                "Type": clean_text(first(row, "Type", "Tipo")),
                "Version": version,
                "Ext_Color": clean_text(first(row, "Ext_Color", "Color", "Color Ext.", "Color")),
                "Int_Color": clean_text(first(row, "Int_Color", "Color Int.", "Int. Color")),
                "RRP_EUR": rrp,
                "Monthly_EUR": monthly,
                "APR_pct": apr,
                "Availability": clean_text(first(row, "Availability", "Estado", "Disponibilidad")),
                "Engine_Raw": clean_text(engine),
                "URL": url,
            }
        )
    print(f"{market} {brand}: {len(rows)} rows from {path.relative_to(BASE_DIR)}")
    return rows


def deduplicate_stock(df: pd.DataFrame) -> pd.DataFrame:
    """Remove only true duplicate listings, preserving identical cars with different URLs."""
    has_url = df["URL"].notna() & df["URL"].astype(str).str.strip().ne("")
    duplicate_url = has_url & df.duplicated(["Market", "Brand", "URL"], keep="first")
    duplicate_exact_no_url = ~has_url & df.duplicated(keep="first")
    duplicate_mask = duplicate_url | duplicate_exact_no_url
    removed = int(duplicate_mask.sum())
    if removed:
        print(f"Removed {removed} duplicate stock rows by Market+Brand+URL")
    return df.loc[~duplicate_mask].reset_index(drop=True)


def build() -> pd.DataFrame:
    sources = [
        (ES_DIR / "STOCK_BMW.xlsx", "BMW", "ES"),
        (ES_DIR / "STOCK_AUDI.xlsx", "Audi", "ES"),
        (ES_DIR / "STOCK_MERCEDES.xlsx", "Mercedes-Benz", "ES"),
        (PT_DIR / "STOCK_BMW_PT.xlsx", "BMW", "PT"),
        (PT_DIR / "STOCK_AUDI_PT.xlsx", "Audi", "PT"),
        (PT_DIR / "STOCK_MERCEDES_PT.xlsx", "Mercedes-Benz", "PT"),
    ]
    rows: list[dict] = []
    for path, brand, market in sources:
        rows.extend(normalize_rows(path, brand, market))

    df = pd.DataFrame(rows, columns=UNIFIED_COLUMNS)
    df = enrich_from_master(df)
    df = deduplicate_stock(df)
    if len(df) < 1000:
        raise RuntimeError(f"Refusing to write dataset with too few rows: {len(df)}")
    if df["Brand"].nunique() < 3 or df["Market"].nunique() < 2:
        raise RuntimeError("Refusing to write dataset missing brands or markets")
    return df


def main() -> None:
    df = build()
    df.to_excel(OUT_XLSX, index=False)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"Wrote {len(df)} rows")
    print(df.groupby(["Market", "Brand"]).size().to_string())
    print(f"Excel: {OUT_XLSX}")
    print(f"CSV  : {OUT_CSV}")


if __name__ == "__main__":
    main()
