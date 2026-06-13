"""
Pipeline global — combina ES + PT y genera STOCK_UNIFICADO_GLOBAL.csv
Llamado por GitHub Actions tras ejecutar los scrapers.
"""
import pandas as pd
import numpy as np
import html
import re
import struct
import zlib
from pathlib import Path

BASE = Path(__file__).parent

FUEL_MAP = {"MHEV": "ICE", "HEV": "ICE"}   # Alineado con catálogo maestro

def _safe_excel(path):
    try:
        return pd.read_excel(path, engine="openpyxl")
    except Exception:
        return None

def _clean(v):
    if isinstance(v, str):
        return html.unescape(v).strip()
    return v

def _norm_es(df):
    df = df.rename(columns={
        "PVP (€)": "RRP_EUR", "Cuota/mes (€)": "Monthly_EUR",
        "TAE (%)": "APR_pct", "Motor/Combustible": "Engine_Raw",
        "URL Coche": "URL", "Carrocería": "Body_Type",
        "Concesionario": "Dealer", "Ciudad": "City",
        "Provincia": "Province", "Versión": "Version",
        "Color": "Ext_Color", "Estado": "Availability",
        "Año": "Year", "Fecha": "Available_Date",
        "Tipo": "Type", "Fuel_type": "Fuel_Type",
    })
    df["Brand"] = df.get("Marca", "")
    df["Model"] = df.get("Modelo_norm", df.get("Modelo", ""))
    df["Market"] = "ES"
    return df

def _norm_pt(df):
    df["Market"] = "PT"
    df["Province"] = df.get("City", "")
    return df

COLS = ["Market","Brand","Model","Body_Type","Fuel_Type","Year","Available_Date",
        "Dealer","City","Province","Type","Version","Ext_Color","Int_Color",
        "RRP_EUR","Monthly_EUR","APR_pct","Availability","Engine_Raw","URL"]

frames = []

# ── ES ────────────────────────────────────────────────────────
es_unified = BASE / "ES_MARKET" / "STOCK_UNIFICADO.xlsx"
df_es = _safe_excel(es_unified)
if df_es is not None:
    df_es = _norm_es(df_es)
    frames.append(df_es)
    print(f"ES cargado: {len(df_es):,} filas")
else:
    print("AVISO: STOCK_UNIFICADO.xlsx no encontrado")

# ── PT ────────────────────────────────────────────────────────
pt_unified = BASE / "PT_MARKET" / "STOCK_PT.xlsx"
df_pt = _safe_excel(pt_unified)
if df_pt is not None:
    df_pt = _norm_pt(df_pt)
    frames.append(df_pt)
    print(f"PT cargado: {len(df_pt):,} filas")
else:
    print("AVISO: STOCK_PT.xlsx no encontrado")

if not frames:
    print("ERROR: sin datos. Saliendo.")
    raise SystemExit(1)

# ── Combinar ──────────────────────────────────────────────────
df = pd.concat(frames, ignore_index=True)

# Limpiar HTML entities
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].apply(_clean)

# Normalizar Fuel_Type (MHEV/HEV → ICE)
if "Fuel_Type" in df.columns:
    df["Fuel_Type"] = df["Fuel_Type"].replace(FUEL_MAP)

# Garantizar columnas del CSV final
for col in COLS:
    if col not in df.columns:
        df[col] = np.nan

df = df[COLS]

# Numéricos
for col in ["RRP_EUR", "Monthly_EUR", "APR_pct"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Guardar
out = BASE / "STOCK_UNIFICADO_GLOBAL.csv"
df.to_csv(out, index=False)

print(f"\nCSV generado: {out}")
print(f"Total filas:  {len(df):,}")
print(f"Marcas:       {df['Brand'].value_counts().to_dict()}")
print(f"Fuel_Type:    {df['Fuel_Type'].value_counts().to_dict()}")
print(f"Con precio:   {df['RRP_EUR'].notna().sum():,}")
