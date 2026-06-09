from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
ES_DIR = BASE_DIR / "ES_MARKET"
PT_DIR = BASE_DIR / "PT_MARKET"

OUT_XLSX = BASE_DIR / "STOCK_UNIFICADO_GLOBAL.xlsx"
OUT_CSV = BASE_DIR / "STOCK_UNIFICADO_GLOBAL.csv"

UNIFIED_COLUMNS = [
    "Market",
    "Brand",
    "Model",
    "Body_Type",
    "Fuel_Type",
    "Year",
    "Available_Date",
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
}


def norm_key(value: object) -> str:
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text).strip().lower()


def clean_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).replace("\xa0", " ").strip()
    return re.sub(r"\s+", " ", text).strip()


def clean_model(value: object) -> str:
    model = clean_text(value)
    if not model:
        return ""
    model = BRAND_PREFIX.sub("", model).strip()
    key = norm_key(model)

    bm = BMW_SERIES_KEY_RE.match(key)
    if bm:
        return f"Serie {bm.group(1) or bm.group(2)}"

    mc = MERCEDES_CLASS_RE.match(key)
    if mc:
        code = (mc.group(1) or mc.group(2) or "").lower()
        return MERCEDES_CLASS_MAP.get(code, f"Clase {code.upper()}")
    if key in MERCEDES_CLASS_MAP:
        return MERCEDES_CLASS_MAP[key]

    return model.replace("Série", "Serie")


def normalize_fuel(value: object) -> str:
    key = norm_key(value)
    if not key:
        return ""
    if any(x in key for x in ["electric", "electrico", "elctrico", "bev", "e-tron"]) and "hybrid" not in key and "hibrid" not in key:
        return "BEV"
    if any(x in key for x in ["plug", "phev", "hibrido enchufable", "hybrid plug", "tfsi e", "e-hybrid"]):
        return "PHEV"
    if "mhev" in key or "mild" in key or "hibrido suave" in key:
        return "MHEV"
    if "hybrid" in key or "hibrid" in key or "hev" in key:
        return "HEV"
    return "ICE"


def normalize_body(model: object, body: object = "", version: object = "") -> str:
    text = " ".join([clean_text(model), clean_text(body), clean_text(version)])
    key = norm_key(text)
    if any(x in key for x in ["sportback", "hatch", "hach", "compact"]):
        return "HATCH"
    if any(x in key for x in ["avant", "touring", "estate", "familiar"]):
        return "TOURING"
    if any(x in key for x in ["cabrio", "convertible"]):
        return "CABRIO"
    if "coupe" in key or "coup" in key:
        return "COUPE"
    if any(x in key for x in ["suv", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "gla", "glb", "glc", "gle", "gls", "eqa", "eqb", "eqc", "eqe", "eqs"]):
        return "SUV"
    if any(x in key for x in ["sedan", "berlina", "limousine"]):
        return "SEDAN"
    return clean_text(body)


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


def normalize_rows(path: Path, brand: str, market: str) -> list[dict]:
    df = read_excel(path)
    rows: list[dict] = []
    for _, row in df.iterrows():
        raw_model = first(row, "Model", "Modelo_norm", "Modelo", "Carline", "model")
        model = clean_model(raw_model)
        if not model:
            continue

        version = clean_text(first(row, "Version", "Versión", "version"))
        body = normalize_body(model, first(row, "Body_Type", "Carrocería", "Carroceria", "Body", "body"), version)
        engine = first(row, "Fuel_Type", "Fuel_type", "Fuel", "Combustible", "Motor/Combustible", "Engine_Raw", "Engine")
        city = clean_text(first(row, "City", "Ciudad", "city"))
        province = clean_text(first(row, "Province", "Provincia", "province")) or province_from_city(city)
        rrp = to_number(first(row, "RRP_EUR", "PVP (€)", "PVP (EUR)", "RRP (EUR)", "Base Price (EUR)", "Price (EUR)"))
        monthly = to_number(first(row, "Monthly_EUR", "Cuota/mes (€)", "Cuota/mes (EUR)", "Monthly Rate (EUR)", "Monthly (EUR)"))
        apr = to_number(first(row, "APR_pct", "TAE (%)", "APR (%)"))
        year = to_number(first(row, "Year", "Año", "Ano"))

        rows.append(
            {
                "Market": market,
                "Brand": brand,
                "Model": model,
                "Body_Type": body,
                "Fuel_Type": normalize_fuel(engine),
                "Year": int(year) if year else None,
                "Available_Date": clean_text(first(row, "Available_Date", "Fecha", "Fecha Disponible", "Date")),
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
                "URL": clean_text(first(row, "URL", "URL Coche", "Car URL")),
            }
        )
    print(f"{market} {brand}: {len(rows)} rows from {path.relative_to(BASE_DIR)}")
    return rows


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
