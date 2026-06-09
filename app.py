"""
Stock Intelligence Hub
Dashboard de análisis de stock de vehículos premium — BMW · Audi · Mercedes-Benz
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
import re

# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Intelligence Hub",
    page_icon="assets/favicon.png" if Path("assets/favicon.png").exists() else "🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fondo general */
.stApp {
    background: #f1f4f9;
}

/* Ocultar header de streamlit */
header[data-testid="stHeader"] { background: transparent; }
div[data-testid="stToolbar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Header imagen */
.app-header {
    width: 100%;
    display: block;
    margin-bottom: 0;
}

/* ── Sidebar ────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0d1b2a;
    border-right: 1px solid #1e3050;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCheckbox span {
    color: #94a3b8 !important;
    font-size: 12px;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: #1c69d4;
}
[data-testid="stSidebar"] hr {
    border-color: #1e3050;
}

/* ── Títulos de sección ─────────────────────── */
.section-header {
    font-size: 13px;
    font-weight: 600;
    color: #0f172a;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 20px 0 10px;
    border-bottom: 2px solid #1c69d4;
    margin-bottom: 16px;
}

/* ── Tarjetas KPI ───────────────────────────── */
.kpi-wrap {
    background: #ffffff;
    border-radius: 6px;
    padding: 16px 18px;
    border-top: 3px solid #1c69d4;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.kpi-label {
    font-size: 10px;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 20px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub {
    font-size: 11px;
    color: #94a3b8;
}

/* ── Tarjeta gráfico ────────────────────────── */
.chart-card {
    background: #ffffff;
    border-radius: 6px;
    padding: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

/* ── Insight box ────────────────────────────── */
.insight-item {
    background: #ffffff;
    border-left: 3px solid #1c69d4;
    border-radius: 0 6px 6px 0;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #1e293b;
    line-height: 1.6;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.insight-tag {
    display: inline-block;
    background: #1c69d4;
    color: white;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 2px 8px;
    border-radius: 3px;
    margin-right: 8px;
    vertical-align: middle;
}

/* ── Tabla ──────────────────────────────────── */
.vehicle-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}
.vehicle-table th {
    background: #0d1b2a;
    color: #94a3b8;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 10px 12px;
    text-align: left;
    position: sticky;
    top: 0;
}
.vehicle-table td {
    padding: 9px 12px;
    border-bottom: 1px solid #f1f4f9;
    color: #334155;
    white-space: nowrap;
}
.vehicle-table tr:hover td { background: #f8fafc; }
.table-scroll {
    overflow-x: auto;
    border-radius: 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    max-height: 520px;
    overflow-y: auto;
}
.brand-pill {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 3px;
}
.pill-bmw  { background: #dbeafe; color: #1d4ed8; }
.pill-audi { background: #fee2e2; color: #991b1b; }
.pill-mb   { background: #f1f5f9; color: #475569; }

/* ── Chat ───────────────────────────────────── */
.chat-container {
    background: #ffffff;
    border-radius: 6px;
    padding: 16px;
    min-height: 320px;
    max-height: 420px;
    overflow-y: auto;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-bottom: 12px;
}
.msg-user {
    text-align: right;
    margin: 8px 0;
}
.msg-user span {
    display: inline-block;
    background: #1c69d4;
    color: white;
    padding: 9px 14px;
    border-radius: 12px 12px 2px 12px;
    font-size: 13px;
    max-width: 75%;
    text-align: left;
}
.msg-bot {
    text-align: left;
    margin: 8px 0;
}
.msg-bot span {
    display: inline-block;
    background: #f8fafc;
    color: #1e293b;
    padding: 9px 14px;
    border-radius: 12px 12px 12px 2px;
    font-size: 13px;
    max-width: 82%;
    border: 1px solid #e2e8f0;
    line-height: 1.6;
}

/* ── Tabs ───────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 6px 6px 0 0;
    gap: 0;
    border-bottom: 2px solid #e2e8f0;
    padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
    font-size: 12px;
    font-weight: 500;
    padding: 10px 18px;
    color: #64748b;
    border-radius: 0;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #1c69d4 !important;
    border-bottom: 2px solid #1c69d4 !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────
BASE = Path(__file__).parent

COLORS = {
    "BMW": "#1c69d4",
    "Audi": "#bb0a14",
    "Mercedes-Benz": "#6b7271",
}
FUEL_COLORS = {
    "ICE":  "#64748b",
    "HEV":  "#16a34a",
    "MHEV": "#0ea5e9",
    "BEV":  "#7c3aed",
    "PHEV": "#d97706",
}
TPL = "plotly_white"

def fig_base(fig, h=310):
    fig.update_layout(
        template=TPL,
        height=h,
        margin=dict(l=8, r=8, t=32, b=8),
        font=dict(family="Inter", size=11, color="#334155"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font_size=10,
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#e2e8f0", tickfont_size=10)
    fig.update_yaxes(gridcolor="#f1f4f9", linecolor="#e2e8f0", tickfont_size=10)
    return fig

# ─────────────────────────────────────────────────────────────
# CARGA Y NORMALIZACIÓN DE DATOS
# ─────────────────────────────────────────────────────────────
def _safe_excel(path):
    try:
        return pd.read_excel(path, engine="openpyxl")
    except Exception:
        return None

def _norm_csv(df):
    """Normaliza el CSV recuperado del GLOBAL (columnas en inglés)."""
    df = df.copy()
    df = df.rename(columns={
        "Market":        "Mercado",
        "Brand":         "Marca",
        "Model":         "Modelo",
        "Body_Type":     "Carrocería",
        "Fuel_Type":     "Fuel_type",
        "Year":          "Año",
        "Available_Date":"Fecha",
        "Dealer":        "Concesionario",
        "City":          "Ciudad",
        "Province":      "Provincia",
        "Type":          "Tipo",
        "Version":       "Versión",
        "Ext_Color":     "Color",
        "Int_Color":     "Color_int",
        "RRP_EUR":       "PVP",
        "Monthly_EUR":   "Cuota_mes",
        "APR_pct":       "TAE",
        "Availability":  "Estado",
        "Engine_Raw":    "Motor",
    })
    df["Modelo_norm"] = df["Modelo"]
    for c in ["TIN","Entrada","Plazo","Cuota_final","Km_año"]:
        if c not in df.columns:
            df[c] = np.nan
    for c in ["PVP","Cuota_mes","TAE","Año"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def _norm_es(df, mercado="ES"):
    df = df.copy()
    df["Mercado"] = mercado
    df = df.rename(columns={
        "PVP (€)":          "PVP",
        "Cuota/mes (€)":    "Cuota_mes",
        "TAE (%)":          "TAE",
        "TIN (%)":          "TIN",
        "Motor/Combustible":"Motor",
        "URL Coche":        "URL",
    })
    if "Modelo_norm" not in df.columns:
        df["Modelo_norm"] = df.get("Modelo", "")
    if "Modelo" not in df.columns:
        df["Modelo"] = df["Modelo_norm"]
    for c in ["TIN","Entrada","Plazo","Cuota_final","Km_año","Provincia","Color","Estado"]:
        if c not in df.columns:
            df[c] = np.nan
    return df

def _norm_pt(df, mercado="PT"):
    df = df.copy()
    df["Mercado"] = mercado
    df = df.rename(columns={
        "Brand":        "Marca",
        "Model":        "Modelo",
        "Body_Type":    "Carrocería",
        "Fuel_Type":    "Fuel_type",
        "Year":         "Año",
        "Available_Date":"Fecha",
        "Dealer":       "Concesionario",
        "City":         "Ciudad",
        "Type":         "Tipo",
        "Version":      "Versión",
        "Ext_Color":    "Color",
        "RRP_EUR":      "PVP",
        "Monthly_EUR":  "Cuota_mes",
        "APR_pct":      "TAE",
        "Availability": "Estado",
        "Engine_Raw":   "Motor",
    })
    df["Modelo_norm"] = df.get("Modelo", "")
    df["Provincia"] = df.get("Ciudad", "")
    for c in ["TIN","Entrada","Plazo","Cuota_final","Km_año","Int_Color"]:
        if c not in df.columns:
            df[c] = np.nan
    return df

@st.cache_data(show_spinner="Cargando datos...")
def load_data():
    # 1. CSV recuperado del GLOBAL (fuente principal — siempre disponible)
    csv_f = BASE / "STOCK_UNIFICADO_GLOBAL.csv"
    if csv_f.exists():
        df = pd.read_csv(csv_f, low_memory=False)
        if len(df) > 100:
            return _norm_csv(df)

    # 2. XLSX global (si no está bloqueado por Excel)
    df_g = _safe_excel(BASE / "STOCK_UNIFICADO_GLOBAL.xlsx")
    if df_g is not None and len(df_g) > 100:
        if "Mercado" not in df_g.columns:
            df_g["Mercado"] = "ES"
        return _norm_es(df_g)

    # 3. Fallback: combinar ES + PT
    frames = []
    df_es = _safe_excel(BASE / "ES_MARKET" / "STOCK_UNIFICADO.xlsx")
    if df_es is not None:
        frames.append(_norm_es(df_es, "ES"))
    df_pt = _safe_excel(BASE / "PT_MARKET" / "STOCK_PT.xlsx")
    if df_pt is not None:
        frames.append(_norm_pt(df_pt, "PT"))

    if not frames:
        st.error("No se encontraron archivos de datos.")
        st.stop()

    df = pd.concat(frames, ignore_index=True)
    for c in ["PVP","Cuota_mes","TAE","TIN"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
def show_header():
    img = BASE / "header.png"
    if img.exists():
        b64 = base64.b64encode(img.read_bytes()).decode()
        st.markdown(
            f'<img src="data:image/png;base64,{b64}" class="app-header">',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="background:#07111C;padding:28px 40px;">'
            '<span style="color:white;font-size:28px;font-weight:700;letter-spacing:3px;">STOCK</span>'
            '<span style="color:#1c69d4;font-size:14px;letter-spacing:5px;margin-left:16px;">INTELLIGENCE HUB</span>'
            '</div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────
# SIDEBAR — FILTROS
# ─────────────────────────────────────────────────────────────
def sidebar_filters(df):
    with st.sidebar:
        st.markdown("### Filtros")

        def msel(label, col):
            opts = sorted(df[col].dropna().unique().tolist()) if col in df.columns else []
            return st.multiselect(label, opts, default=[], key=f"f_{col}")

        marcas     = msel("Marca",          "Marca")
        mercados   = msel("Mercado",        "Mercado")
        modelos    = msel("Modelo",         "Modelo_norm")
        fuels      = msel("Combustible",    "Fuel_type")
        carros     = msel("Carrocería",     "Carrocería")
        dealers    = msel("Concesionario",  "Concesionario")
        ciudades   = msel("Ciudad",         "Ciudad")
        provincias = msel("Provincia",      "Provincia")
        estados    = msel("Estado",         "Estado")

        st.markdown("---")

        # Slider PVP
        pvp_s = df["PVP"].dropna() if "PVP" in df.columns else pd.Series(dtype=float)
        if len(pvp_s) > 0:
            pmin, pmax = float(pvp_s.min()), float(pvp_s.max())
            pmax = pmax if pmax > pmin else pmin + 1.0
            pvp_r = st.slider("Precio (€)", pmin, pmax, (pmin, pmax), step=500.0, format="%.0f€")
        else:
            pvp_r = (0, 999999)

        # Slider Cuota
        cuota_s = df["Cuota_mes"].dropna() if "Cuota_mes" in df.columns else pd.Series(dtype=float)
        if len(cuota_s) > 0:
            cmin, cmax = float(cuota_s.min()), float(cuota_s.max())
            cmax = cmax if cmax > cmin else cmin + 1.0
            cuota_r = st.slider("Cuota/mes (€)", cmin, cmax, (cmin, cmax), step=10.0, format="%.0f€")
        else:
            cuota_r = (0, 99999)

        st.markdown("---")
        solo_pvp   = st.checkbox("Solo con precio informado",       False)
        solo_cuota = st.checkbox("Solo con cuota mensual informada", False)

        años_opts = sorted(df["Año"].dropna().unique().astype(int).tolist()) if "Año" in df.columns else []
        años = st.multiselect("Año", años_opts, default=[], key="f_año")

    # Aplicar
    mask = pd.Series(True, index=df.index)
    for col, sel in [
        ("Marca", marcas), ("Mercado", mercados), ("Modelo_norm", modelos),
        ("Fuel_type", fuels), ("Carrocería", carros), ("Concesionario", dealers),
        ("Ciudad", ciudades), ("Provincia", provincias), ("Estado", estados),
    ]:
        if sel and col in df.columns:
            mask &= df[col].isin(sel)

    if años and "Año" in df.columns:
        mask &= df["Año"].isin(años)

    if "PVP" in df.columns:
        pvp_m = df["PVP"].notna()
        mask &= (~pvp_m) | df["PVP"].between(*pvp_r)

    if "Cuota_mes" in df.columns:
        cuota_m = df["Cuota_mes"].notna()
        mask &= (~cuota_m) | df["Cuota_mes"].between(*cuota_r)

    if solo_pvp   and "PVP"      in df.columns: mask &= df["PVP"].notna()
    if solo_cuota and "Cuota_mes" in df.columns: mask &= df["Cuota_mes"].notna()

    return df[mask].copy()

# ─────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────
def kpi(label, value, sub=""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="kpi-wrap">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{sub_html}</div>'
    )

def _eu(x, dec=0):
    """Formato europeo: 1.234,56 €"""
    if not pd.notna(x) or x != x:
        return "—"
    s = f"{x:,.{dec}f}"                     # "1,234.56"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")  # "1.234,56"
    return f"{s} €"

def eur(x):       return _eu(x, 0)
def eur2(x):      return _eu(x, 2)
def eu_mes(x):    return f"{_eu(x, 0)}/mes" if pd.notna(x) and x == x else "—"
def eu_num(x):    # número sin símbolo
    if not pd.notna(x) or x != x: return "—"
    s = f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def pct(n, d):
    return f"{n/d*100:.0f}%" if d > 0 else "—"

def show_kpis(df):
    total   = len(df)
    pvp_s   = df["PVP"].dropna()     if "PVP"      in df.columns else pd.Series()
    cuota_s = df["Cuota_mes"].dropna() if "Cuota_mes" in df.columns else pd.Series()

    n_pvp   = len(pvp_s)
    n_cuota = len(cuota_s)
    n_mods  = df["Modelo_norm"].nunique() if "Modelo_norm" in df.columns else 0
    n_deal  = df["Concesionario"].nunique() if "Concesionario" in df.columns else 0

    top_modelo = df["Modelo_norm"].value_counts().idxmax() if "Modelo_norm" in df.columns and n_pvp else "—"
    top_ciudad = df["Ciudad"].value_counts().idxmax() if "Ciudad" in df.columns and not df["Ciudad"].isna().all() else "—"
    top_dealer = df["Concesionario"].value_counts().idxmax() if "Concesionario" in df.columns and not df["Concesionario"].isna().all() else "—"

    row1 = st.columns(7)
    datos_r1 = [
        ("Total vehículos",   eu_num(total),              "en stock"),
        ("Con precio",        eu_num(n_pvp),              pct(n_pvp, total)),
        ("Con cuota/mes",     eu_num(n_cuota),            pct(n_cuota, total)),
        ("Precio medio",      eur(pvp_s.mean()),          f"Mín. {eur(pvp_s.min())}"),
        ("Precio máximo",     eur(pvp_s.max()),           ""),
        ("Cuota media",       eu_mes(cuota_s.mean()) if len(cuota_s) else "—", f"Mín. {_eu(cuota_s.min(), 0)}" if len(cuota_s) else ""),
        ("Cuota máxima",      eu_mes(cuota_s.max())  if len(cuota_s) else "—", ""),
    ]
    for col, (l, v, s) in zip(row1, datos_r1):
        col.markdown(kpi(l, v, s), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    row2 = st.columns(7)
    tae_s = df["TAE"].dropna() if "TAE" in df.columns else pd.Series()
    datos_r2 = [
        ("Marcas",            str(df["Marca"].nunique()),  "analizadas"),
        ("Modelos",           str(n_mods),                 "distintos"),
        ("Concesionarios",    str(n_deal),                 "analizados"),
        ("Modelo top stock",  str(top_modelo)[:26],        "más unidades"),
        ("Ciudad con más stock", str(top_ciudad),          ""),
        ("Dealer principal",  str(top_dealer)[:24],        ""),
        ("TAE media",         f"{tae_s.mean():.2f}%" if len(tae_s) else "—", "sobre financiados"),
    ]
    for col, (l, v, s) in zip(row2, datos_r2):
        col.markdown(kpi(l, v, s), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CHARTS — STOCK
# ─────────────────────────────────────────────────────────────
def charts_stock(df):
    c1, c2 = st.columns(2)

    with c1:
        gb = df.groupby("Marca").size().reset_index(name="N").sort_values("N", ascending=False)
        fig = px.bar(gb, x="Marca", y="N", color="Marca",
                     color_discrete_map=COLORS, text="N",
                     title="Stock por marca",
                     labels={"N": "Vehículos", "Marca": ""})
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig_base(fig), width="stretch")

    with c2:
        gb2 = df.groupby("Fuel_type").size().reset_index(name="N").sort_values("N", ascending=False)
        fig2 = px.pie(gb2, names="Fuel_type", values="N",
                      color="Fuel_type", color_discrete_map=FUEL_COLORS,
                      title="Distribución por combustible", hole=0.5)
        fig2.update_traces(textinfo="percent+label", textfont_size=11)
        st.plotly_chart(fig_base(fig2), width="stretch")

    c3, c4 = st.columns(2)

    with c3:
        top_m = df.groupby("Modelo_norm").size().reset_index(name="N").sort_values("N", ascending=False).head(15)
        fig3 = px.bar(top_m, y="Modelo_norm", x="N", orientation="h",
                      title="Top 15 modelos por unidades",
                      labels={"N": "Unidades", "Modelo_norm": ""},
                      color="N", color_continuous_scale=["#bfdbfe", "#1c69d4"])
        fig3.update_layout(coloraxis_showscale=False,
                           yaxis=dict(autorange="reversed", tickfont_size=10))
        st.plotly_chart(fig_base(fig3, 380), width="stretch")

    with c4:
        top_d = df.groupby("Concesionario").size().reset_index(name="N").sort_values("N", ascending=False).head(12)
        fig4 = px.bar(top_d, y="Concesionario", x="N", orientation="h",
                      title="Top 12 concesionarios",
                      labels={"N": "Unidades", "Concesionario": ""},
                      color="N", color_continuous_scale=["#bfdbfe", "#1c69d4"])
        fig4.update_layout(coloraxis_showscale=False,
                           yaxis=dict(autorange="reversed", tickfont_size=10))
        st.plotly_chart(fig_base(fig4, 380), width="stretch")

    if "Ciudad" in df.columns and df["Ciudad"].notna().any():
        top_c = df.groupby("Ciudad").size().reset_index(name="N").sort_values("N", ascending=False).head(20)
        fig5 = px.bar(top_c, x="Ciudad", y="N",
                      title="Top 20 ciudades por stock",
                      color="N", color_continuous_scale=["#bfdbfe", "#1c69d4"],
                      labels={"N": "Unidades", "Ciudad": ""})
        fig5.update_layout(coloraxis_showscale=False, xaxis_tickangle=-35)
        st.plotly_chart(fig_base(fig5, 300), width="stretch")

    if "Carrocería" in df.columns and df["Carrocería"].notna().any():
        c5, c6 = st.columns(2)
        with c5:
            gb_c = df.groupby("Carrocería").size().reset_index(name="N").sort_values("N", ascending=False)
            fig6 = px.bar(gb_c, x="Carrocería", y="N",
                          title="Stock por tipo de carrocería",
                          labels={"N": "Unidades", "Carrocería": ""},
                          color="Carrocería")
            fig6.update_layout(showlegend=False)
            st.plotly_chart(fig_base(fig6, 280), width="stretch")

        with c6:
            gb_m = df.groupby("Mercado").size().reset_index(name="N")
            fig7 = px.pie(gb_m, names="Mercado", values="N",
                          title="Stock por mercado", hole=0.5,
                          color_discrete_sequence=["#1c69d4","#0f172a"])
            fig7.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_base(fig7, 280), width="stretch")

# ─────────────────────────────────────────────────────────────
# CHARTS — PRECIOS
# ─────────────────────────────────────────────────────────────
def charts_precios(df):
    df_pvp = df[df["PVP"].notna()].copy() if "PVP" in df.columns else pd.DataFrame()
    if df_pvp.empty:
        st.info("No hay datos de precio disponibles con los filtros actuales.")
        return

    c1, c2 = st.columns(2)

    with c1:
        gb = df_pvp.groupby("Marca")["PVP"].agg(["mean","min","max"]).reset_index()
        fig = go.Figure()
        for _, r in gb.iterrows():
            c = COLORS.get(r["Marca"], "#1c69d4")
            fig.add_trace(go.Bar(
                name=r["Marca"], x=[r["Marca"]],
                y=[r["mean"]], marker_color=c,
                error_y=dict(type="data", symmetric=False,
                             array=[r["max"] - r["mean"]],
                             arrayminus=[r["mean"] - r["min"]]),
                text=[f"{r['mean']:,.0f}€"], textposition="outside",
            ))
        fig.update_layout(
            title="Precio medio por marca (con rango)",
            showlegend=False, yaxis_title="€",
            template=TPL, height=310,
            margin=dict(l=8,r=8,t=36,b=8),
            font=dict(family="Inter", size=11),
            paper_bgcolor="white", plot_bgcolor="white",
        )
        st.plotly_chart(fig, width="stretch")

    with c2:
        fig2 = px.histogram(df_pvp, x="PVP", color="Marca",
                            color_discrete_map=COLORS, nbins=50,
                            title="Distribución de precios",
                            labels={"PVP":"Precio (€)","count":"Vehículos"},
                            barmode="overlay", opacity=0.72)
        st.plotly_chart(fig_base(fig2), width="stretch")

    c3, c4 = st.columns(2)

    with c3:
        grp = (df_pvp.groupby("Modelo_norm")["PVP"]
               .agg(["mean","count"]).reset_index()
               .query("count >= 3")
               .sort_values("mean", ascending=False).head(15))
        fig3 = px.bar(grp, y="Modelo_norm", x="mean", orientation="h",
                      title="Precio medio — top 15 modelos (≥3 uds.)",
                      labels={"mean":"Precio medio (€)","Modelo_norm":""},
                      color="mean", color_continuous_scale=["#bfdbfe","#1c69d4"],
                      text=grp["mean"].map(lambda x: f"{x:,.0f}€"))
        fig3.update_traces(textposition="outside", textfont_size=10)
        fig3.update_layout(coloraxis_showscale=False, yaxis=dict(autorange="reversed", tickfont_size=10))
        st.plotly_chart(fig_base(fig3, 400), width="stretch")

    with c4:
        fig4 = px.box(df_pvp, x="Marca", y="PVP", color="Marca",
                      color_discrete_map=COLORS,
                      title="Dispersión de precios por marca",
                      labels={"PVP":"Precio (€)"})
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig_base(fig4), width="stretch")

    if "Fuel_type" in df_pvp.columns:
        gb_f = df_pvp.groupby(["Fuel_type","Marca"])["PVP"].mean().reset_index()
        fig5 = px.bar(gb_f, x="Fuel_type", y="PVP", color="Marca",
                      barmode="group", color_discrete_map=COLORS,
                      title="Precio medio por combustible y marca",
                      labels={"PVP":"Precio medio (€)","Fuel_type":"Combustible"})
        st.plotly_chart(fig_base(fig5, 300), width="stretch")

# ─────────────────────────────────────────────────────────────
# CHARTS — CUOTAS
# ─────────────────────────────────────────────────────────────
def charts_cuotas(df):
    df_c = df[df["Cuota_mes"].notna()].copy() if "Cuota_mes" in df.columns else pd.DataFrame()
    if df_c.empty:
        st.info("No hay datos de cuota mensual disponibles con los filtros actuales.")
        return

    c1, c2 = st.columns(2)

    with c1:
        gb = df_c.groupby("Marca")["Cuota_mes"].mean().reset_index().sort_values("Cuota_mes")
        fig = px.bar(gb, x="Marca", y="Cuota_mes", color="Marca",
                     color_discrete_map=COLORS,
                     title="Cuota mensual media por marca",
                     text=gb["Cuota_mes"].map(lambda x: f"{x:.0f}€/mes"),
                     labels={"Cuota_mes":"€/mes"})
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig_base(fig), width="stretch")

    with c2:
        fig2 = px.histogram(df_c, x="Cuota_mes", color="Marca",
                            color_discrete_map=COLORS, nbins=40,
                            title="Distribución de cuotas mensuales",
                            labels={"Cuota_mes":"Cuota (€/mes)"},
                            barmode="overlay", opacity=0.72)
        st.plotly_chart(fig_base(fig2), width="stretch")

    c3, c4 = st.columns(2)

    with c3:
        grp = (df_c.groupby("Modelo_norm")["Cuota_mes"]
               .agg(["mean","count"]).reset_index()
               .query("count >= 3").sort_values("mean").head(15))
        fig3 = px.bar(grp, y="Modelo_norm", x="mean", orientation="h",
                      title="Cuota media más baja — top 15 modelos",
                      labels={"mean":"€/mes","Modelo_norm":""},
                      color="mean", color_continuous_scale=["#1c69d4","#bfdbfe"],
                      text=grp["mean"].map(lambda x: f"{x:.0f}€"))
        fig3.update_traces(textposition="outside", textfont_size=10)
        fig3.update_layout(coloraxis_showscale=False, yaxis=dict(tickfont_size=10))
        st.plotly_chart(fig_base(fig3, 380), width="stretch")

    with c4:
        df_both = df[(df["PVP"].notna()) & (df["Cuota_mes"].notna())].copy() if "PVP" in df.columns else pd.DataFrame()
        if not df_both.empty:
            fig4 = px.scatter(df_both, x="PVP", y="Cuota_mes", color="Marca",
                              color_discrete_map=COLORS, opacity=0.55,
                              title="Precio total vs cuota mensual",
                              labels={"PVP":"Precio (€)","Cuota_mes":"Cuota (€/mes)"},
                              hover_data=["Modelo_norm"])
            st.plotly_chart(fig_base(fig4), width="stretch")

    if "TAE" in df_c.columns and df_c["TAE"].notna().any():
        c5, _ = st.columns(2)
        with c5:
            gb_t = df_c.groupby("Marca")["TAE"].mean().reset_index()
            fig5 = px.bar(gb_t, x="Marca", y="TAE", color="Marca",
                          color_discrete_map=COLORS,
                          title="TAE media por marca (%)",
                          text=gb_t["TAE"].map(lambda x: f"{x:.2f}%"),
                          labels={"TAE":"TAE (%)"})
            fig5.update_traces(textposition="outside")
            fig5.update_layout(showlegend=False)
            st.plotly_chart(fig_base(fig5, 280), width="stretch")

# ─────────────────────────────────────────────────────────────
# COMPARADOR DE MODELOS
# ─────────────────────────────────────────────────────────────
def comparador(df):
    modelos_disp = sorted(df["Modelo_norm"].dropna().unique().tolist())
    sel = st.multiselect(
        "Selecciona dos o más modelos:",
        modelos_disp,
        default=modelos_disp[:3] if len(modelos_disp) >= 3 else modelos_disp,
        key="comp_sel",
    )
    if len(sel) < 2:
        st.info("Selecciona al menos 2 modelos para comparar.")
        return

    rows = []
    for m in sel:
        sub = df[df["Modelo_norm"] == m]
        pvp   = sub["PVP"].dropna()   if "PVP"      in sub.columns else pd.Series()
        cuota = sub["Cuota_mes"].dropna() if "Cuota_mes" in sub.columns else pd.Series()
        tae   = sub["TAE"].dropna()   if "TAE"      in sub.columns else pd.Series()
        top_fuel  = sub["Fuel_type"].mode()[0]       if "Fuel_type" in sub.columns and not sub["Fuel_type"].isna().all() else "—"
        top_dealer= sub["Concesionario"].value_counts().idxmax() if "Concesionario" in sub.columns and not sub["Concesionario"].isna().all() else "—"
        rows.append({
            "Modelo":             m,
            "Stock total":        len(sub),
            "Con precio":         len(pvp),
            "Con cuota":          len(cuota),
            "Precio medio (€)":   f"{pvp.mean():,.0f}"  if len(pvp)   else "—",
            "Precio mín. (€)":    f"{pvp.min():,.0f}"   if len(pvp)   else "—",
            "Precio máx. (€)":    f"{pvp.max():,.0f}"   if len(pvp)   else "—",
            "Cuota media (€/mes)":f"{cuota.mean():,.0f}" if len(cuota) else "—",
            "Cuota mín. (€/mes)": f"{cuota.min():,.0f}"  if len(cuota) else "—",
            "Cuota máx. (€/mes)": f"{cuota.max():,.0f}"  if len(cuota) else "—",
            "TAE media (%)":      f"{tae.mean():.2f}"   if len(tae)   else "—",
            "Combustible frec.":  top_fuel,
            "Dealer principal":   top_dealer,
        })

    comp = pd.DataFrame(rows).set_index("Modelo")
    st.dataframe(comp.T.astype(str), width="stretch")

    raw = []
    for m in sel:
        sub = df[df["Modelo_norm"] == m]
        raw.append({
            "Modelo": m,
            "Precio medio": sub["PVP"].mean()      if "PVP"      in sub.columns else np.nan,
            "Cuota media":  sub["Cuota_mes"].mean() if "Cuota_mes" in sub.columns else np.nan,
        })
    raw_df = pd.DataFrame(raw)

    c1, c2 = st.columns(2)
    with c1:
        d = raw_df.dropna(subset=["Precio medio"])
        if not d.empty:
            fig = px.bar(d, x="Modelo", y="Precio medio", color="Modelo",
                         title="Precio medio por modelo",
                         text=d["Precio medio"].map(lambda x: f"{x:,.0f}€"),
                         labels={"Precio medio":"€"})
            fig.update_traces(textposition="outside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig_base(fig), width="stretch")

    with c2:
        d2 = raw_df.dropna(subset=["Cuota media"])
        if not d2.empty:
            fig2 = px.bar(d2, x="Modelo", y="Cuota media", color="Modelo",
                          title="Cuota mensual media por modelo",
                          text=d2["Cuota media"].map(lambda x: f"{x:.0f}€/mes"),
                          labels={"Cuota media":"€/mes"})
            fig2.update_traces(textposition="outside")
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig_base(fig2), width="stretch")

    # Insight comparativo
    d_pvp = raw_df.dropna(subset=["Precio medio"])
    if len(d_pvp) >= 2:
        idx_min = d_pvp["Precio medio"].idxmin()
        idx_max = d_pvp["Precio medio"].idxmax()
        m_min = d_pvp.loc[idx_min, "Modelo"]
        m_max = d_pvp.loc[idx_max, "Modelo"]
        p_min = d_pvp.loc[idx_min, "Precio medio"]
        p_max = d_pvp.loc[idx_max, "Precio medio"]
        diff  = p_max - p_min
        pct_v = diff / p_min * 100
        st.markdown(
            f'<div class="insight-item">'
            f'<span class="insight-tag">COMPARATIVA</span>'
            f'{m_min} tiene el precio medio más bajo ({p_min:,.0f} €). '
            f'{m_max} es el más caro ({p_max:,.0f} €). '
            f'Diferencia: <strong>{diff:,.0f} €</strong> ({pct_v:.1f}%).'
            f'</div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────
# TABLA DE VEHÍCULOS
# ─────────────────────────────────────────────────────────────
def tabla_vehiculos(df):
    # Búsqueda
    search = st.text_input("Buscar:", "", key="tabla_search",
                           placeholder="Modelo, concesionario, ciudad...")

    display_cols = [c for c in [
        "Marca","Modelo_norm","Versión","Año","Fuel_type","Carrocería",
        "PVP","Cuota_mes","TAE","Concesionario","Ciudad","Provincia",
        "Mercado","Estado","URL",
    ] if c in df.columns]

    df_show = df[display_cols].copy().reset_index(drop=True)

    if search:
        mask = df_show.apply(
            lambda col: col.astype(str).str.contains(search, case=False, na=False)
        ).any(axis=1)
        df_show = df_show[mask]

    st.caption(f"{len(df_show):,} vehículos")

    # Construir HTML de tabla
    col_labels = {
        "Modelo_norm":"Modelo","PVP":"Precio (€)","Cuota_mes":"Cuota/mes (€)",
        "TAE":"TAE (%)","Fuel_type":"Combustible",
    }

    def brand_pill(marca):
        if marca == "BMW":           return f'<span class="brand-pill pill-bmw">BMW</span>'
        elif marca == "Audi":        return f'<span class="brand-pill pill-audi">Audi</span>'
        elif marca == "Mercedes-Benz": return f'<span class="brand-pill pill-mb">MB</span>'
        return marca

    headers = "".join(f"<th>{col_labels.get(c, c)}</th>" for c in display_cols)
    rows_html = ""
    for _, row in df_show.iterrows():
        cells = ""
        for c in display_cols:
            v = row[c]
            if c == "Marca":
                cells += f"<td>{brand_pill(str(v) if pd.notna(v) else '')}</td>"
            elif c == "URL":
                if pd.notna(v) and str(v).startswith("http"):
                    cells += f'<td><a href="{v}" target="_blank" style="color:#1c69d4;text-decoration:none;">Ver anuncio</a></td>'
                else:
                    cells += "<td>—</td>"
            elif c in ("PVP","Cuota_mes","Entrada","Cuota_final"):
                cells += f"<td>{f'{v:,.0f}' if pd.notna(v) else '—'}</td>"
            elif c in ("TAE","TIN"):
                cells += f"<td>{f'{v:.2f}%' if pd.notna(v) else '—'}</td>"
            elif c == "Año":
                cells += f"<td>{int(v) if pd.notna(v) else '—'}</td>"
            else:
                cells += f"<td>{v if pd.notna(v) else '—'}</td>"
        rows_html += f"<tr>{cells}</tr>"

    html = (
        f'<div class="table-scroll">'
        f'<table class="vehicle-table">'
        f'<thead><tr>{headers}</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table></div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    # Exportar
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", csv, "stock_filtrado.csv", "text/csv")

# ─────────────────────────────────────────────────────────────
# INSIGHTS AUTOMÁTICOS
# ─────────────────────────────────────────────────────────────
def show_insights(df):
    total   = len(df)
    pvp_s   = df["PVP"].dropna()      if "PVP"      in df.columns else pd.Series()
    cuota_s = df["Cuota_mes"].dropna() if "Cuota_mes" in df.columns else pd.Series()

    items = []

    top_marca   = df["Marca"].value_counts()
    items.append(
        f'<span class="insight-tag">STOCK</span>'
        f'La marca con más unidades anunciadas es <strong>{top_marca.idxmax()}</strong> '
        f'con {top_marca.max():,} vehículos ({top_marca.max()/total*100:.1f}% del total).'
    )

    top_mod = df["Modelo_norm"].value_counts()
    items.append(
        f'<span class="insight-tag">MODELO</span>'
        f'El modelo con mayor stock es <strong>{top_mod.idxmax()}</strong> '
        f'con {top_mod.max():,} unidades.'
    )

    if not pvp_s.empty:
        grp_pvp = df[df["PVP"].notna()].groupby("Modelo_norm")["PVP"].mean()
        items.append(
            f'<span class="insight-tag">PRECIO</span>'
            f'Precio medio general: <strong>{pvp_s.mean():,.0f} €</strong>. '
            f'Modelo más caro en media: <strong>{grp_pvp.idxmax()}</strong> ({grp_pvp.max():,.0f} €). '
            f'Modelo más económico: <strong>{grp_pvp.idxmin()}</strong> ({grp_pvp.min():,.0f} €).'
        )
        items.append(
            f'<span class="insight-tag">PRECIO</span>'
            f'El {len(pvp_s)/total*100:.1f}% del stock tiene precio informado '
            f'({len(pvp_s):,} de {total:,} vehículos).'
        )

    if not cuota_s.empty:
        grp_cuota = df[df["Cuota_mes"].notna()].groupby("Modelo_norm")["Cuota_mes"].mean()
        marca_cuota = df[df["Cuota_mes"].notna()].groupby("Marca")["Cuota_mes"].mean()
        items.append(
            f'<span class="insight-tag">CUOTA</span>'
            f'Cuota media: <strong>{cuota_s.mean():,.0f} €/mes</strong>. '
            f'La cuota media más baja por modelo corresponde a <strong>{grp_cuota.idxmin()}</strong> '
            f'({grp_cuota.min():,.0f} €/mes). '
            f'La marca con cuota media más baja es <strong>{marca_cuota.idxmin()}</strong> '
            f'({marca_cuota.min():,.0f} €/mes).'
        )
        items.append(
            f'<span class="insight-tag">CUOTA</span>'
            f'El {len(cuota_s)/total*100:.1f}% del stock tiene cuota mensual informada '
            f'({len(cuota_s):,} de {total:,} vehículos).'
        )

    if "Ciudad" in df.columns and df["Ciudad"].notna().any():
        top_c = df["Ciudad"].value_counts()
        items.append(
            f'<span class="insight-tag">GEOGRAFIA</span>'
            f'La ciudad con mayor concentración de stock es <strong>{top_c.idxmax()}</strong> '
            f'({top_c.max():,} vehículos).'
        )

    if "Provincia" in df.columns and df["Provincia"].notna().any():
        top_p = df["Provincia"].value_counts()
        items.append(
            f'<span class="insight-tag">GEOGRAFIA</span>'
            f'Provincia con más stock: <strong>{top_p.idxmax()}</strong> ({top_p.max():,} uds.).'
        )

    top_d = df["Concesionario"].value_counts()
    items.append(
        f'<span class="insight-tag">DEALER</span>'
        f'El concesionario con mayor volumen de vehículos anunciados es '
        f'<strong>{top_d.idxmax()}</strong> con {top_d.max():,} unidades.'
    )

    top_fuel = df["Fuel_type"].value_counts()
    items.append(
        f'<span class="insight-tag">COMBUSTIBLE</span>'
        f'El tipo de propulsión más frecuente en el stock es <strong>{top_fuel.idxmax()}</strong> '
        f'({top_fuel.max():,} uds., {top_fuel.max()/total*100:.1f}%).'
    )

    for item in items:
        st.markdown(f'<div class="insight-item">{item}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CHATBOT
# ─────────────────────────────────────────────────────────────
def _responder(q: str, df: pd.DataFrame) -> str:
    q_l = q.lower().strip()
    total = len(df)
    pvp_s   = df["PVP"].dropna()      if "PVP"      in df.columns else pd.Series()
    cuota_s = df["Cuota_mes"].dropna() if "Cuota_mes" in df.columns else pd.Series()

    # Resumen general
    if re.search(r"resumen|total.*stock|cuántos.*coches|cuántos.*vehíc|stock.*total|stock.*actual", q_l):
        marcas_str = " | ".join([f"{m}: {n:,}" for m, n in df["Marca"].value_counts().items()])
        return (
            f"**Resumen del stock actual ({total:,} vehículos)**\n\n"
            f"- Por marca: {marcas_str}\n"
            f"- Con precio informado: {len(pvp_s):,} ({len(pvp_s)/total*100:.1f}%)\n"
            f"- Con cuota mensual: {len(cuota_s):,} ({len(cuota_s)/total*100:.1f}%)\n"
            f"- Precio medio: {pvp_s.mean():,.0f} €\n"
            f"- Cuota mensual media: {cuota_s.mean():,.0f} €/mes" if len(cuota_s) else ""
        )

    # Marca con más stock
    if re.search(r"marca.*más.*stock|mayor.*stock.*marca|qué.*marca.*más", q_l):
        top = df["Marca"].value_counts()
        lines = "\n".join([f"- {m}: {n:,}" for m, n in top.items()])
        return f"**Stock por marca:**\n\n{lines}\n\nLíder: **{top.idxmax()}** con {top.max():,} unidades."

    # Precio más bajo / económico
    if re.search(r"precio.*bajo|más.*económico|más barato|menor.*precio|precio.*mínimo", q_l):
        if pvp_s.empty:
            return "No hay datos de precio con los filtros actuales."
        grp = df[df["PVP"].notna()].groupby("Modelo_norm")["PVP"].mean().sort_values().head(5)
        lines = "\n".join([f"- **{m}:** {v:,.0f} €" for m, v in grp.items()])
        return f"**Modelos con precio medio más bajo:**\n\n{lines}"

    # Precio más alto / caro
    if re.search(r"precio.*alto|más.*caro|mayor.*precio|precio.*máximo", q_l):
        if pvp_s.empty:
            return "No hay datos de precio disponibles."
        grp = df[df["PVP"].notna()].groupby("Modelo_norm")["PVP"].mean().sort_values(ascending=False).head(5)
        lines = "\n".join([f"- **{m}:** {v:,.0f} €" for m, v in grp.items()])
        return f"**Modelos con precio medio más alto:**\n\n{lines}"

    # Cuota inferior a X
    if re.search(r"cuota.*inferior|cuota.*menos|cuota.*por debajo|menor.*cuota|cuota.*mínima|cuota.*baja", q_l):
        nums = re.findall(r'\d+', q_l)
        if nums and "inferior" in q_l or "menos" in q_l or "por debajo" in q_l:
            limit = int(nums[0])
            sub = df[df["Cuota_mes"].notna() & (df["Cuota_mes"] <= limit)]
            if sub.empty:
                return f"No hay vehículos con cuota ≤ {limit} €/mes con los filtros actuales."
            grp = sub.groupby(["Marca","Modelo_norm"])["Cuota_mes"].agg(["count","mean"]).reset_index().sort_values("mean")
            lines = "\n".join([
                f"- **{r['Modelo_norm']}** ({r['Marca']}): {r['mean']:.0f} €/mes — {int(r['count'])} uds."
                for _, r in grp.head(10).iterrows()
            ])
            return f"**{len(sub):,} vehículos con cuota ≤ {limit} €/mes:**\n\n{lines}"
        if cuota_s.empty:
            return "No hay datos de cuota mensual disponibles."
        grp = df[df["Cuota_mes"].notna()].groupby("Modelo_norm")["Cuota_mes"].mean().sort_values().head(5)
        lines = "\n".join([f"- **{m}:** {v:.0f} €/mes" for m, v in grp.items()])
        return f"**Modelos con cuota mensual media más baja:**\n\n{lines}"

    # Comparativa entre modelos
    if re.search(r"compara|vs\.?|versus|diferencia.*entre", q_l):
        encontrados = [
            m for m in sorted(df["Modelo_norm"].dropna().unique(), key=len, reverse=True)
            if m.lower() in q_l and len(m) > 3
        ]
        if len(encontrados) >= 2:
            resp = "**Comparativa de modelos:**\n\n"
            for m in encontrados:
                sub = df[df["Modelo_norm"] == m]
                p = sub["PVP"].dropna()      if "PVP"      in sub.columns else pd.Series()
                c = sub["Cuota_mes"].dropna() if "Cuota_mes" in sub.columns else pd.Series()
                pvp_str   = f"{p.mean():,.0f} €"   if len(p) else "sin precio"
                cuota_str = f"{c.mean():.0f} €/mes" if len(c) else "sin cuota"
                resp += f"- **{m}** — {len(sub):,} uds. | Precio: {pvp_str} | Cuota: {cuota_str}\n"
            if len(encontrados) == 2:
                p0 = df[df["Modelo_norm"]==encontrados[0]]["PVP"].dropna()
                p1 = df[df["Modelo_norm"]==encontrados[1]]["PVP"].dropna()
                if len(p0) and len(p1):
                    diff = abs(p0.mean()-p1.mean())
                    pct_v = diff/min(p0.mean(),p1.mean())*100
                    mas_caro = encontrados[0] if p0.mean() > p1.mean() else encontrados[1]
                    resp += f"\nDiferencia de precio: **{diff:,.0f} €** ({pct_v:.1f}%). El más caro: **{mas_caro}**."
            return resp
        return "Indica los modelos a comparar. Ejemplo: 'Compara BMW Serie 1 con Audi A3'."

    # Eléctricos
    if re.search(r"eléctric|bev|electr", q_l):
        sub = df[df["Fuel_type"] == "BEV"] if "Fuel_type" in df.columns else pd.DataFrame()
        if sub.empty:
            return "No hay vehículos eléctricos (BEV) con los filtros actuales."
        nums = re.findall(r'\d+', q_l)
        if nums:
            limit = float(nums[0]) * 1000 if float(nums[0]) < 1000 else float(nums[0])
            sub2 = sub[sub["PVP"].notna() & (sub["PVP"] <= limit)] if "PVP" in sub.columns else sub
            top_m = sub2["Modelo_norm"].value_counts().head(8)
            lines = "\n".join([f"- **{m}:** {n} uds." for m, n in top_m.items()])
            return f"**{len(sub2):,} eléctricos con precio ≤ {limit:,.0f} €:**\n\n{lines}"
        top_m = sub["Modelo_norm"].value_counts().head(8)
        lines = "\n".join([f"- **{m}:** {n}" for m, n in top_m.items()])
        return f"**{len(sub):,} vehículos eléctricos (BEV) en el stock:**\n\n{lines}"

    # Dealers
    if re.search(r"dealer|concesionario|distribuid", q_l):
        top = df["Concesionario"].value_counts().head(8)
        lines = "\n".join([f"- **{d}:** {n:,} uds." for d, n in top.items()])
        return f"**Top 8 concesionarios por stock:**\n\n{lines}"

    # Provincia / ciudad
    if re.search(r"provincia|ciudad|ubicación|zona|región|donde|dónde", q_l):
        if "Provincia" in df.columns and df["Provincia"].notna().any():
            top = df["Provincia"].value_counts().head(8)
            lines = "\n".join([f"- **{p}:** {n:,}" for p, n in top.items()])
            return f"**Stock por provincia (top 8):**\n\n{lines}"
        if "Ciudad" in df.columns and df["Ciudad"].notna().any():
            top = df["Ciudad"].value_counts().head(8)
            lines = "\n".join([f"- **{c}:** {n:,}" for c, n in top.items()])
            return f"**Stock por ciudad (top 8):**\n\n{lines}"

    # Búsqueda de modelo específico
    for modelo in sorted(df["Modelo_norm"].dropna().unique(), key=len, reverse=True):
        if len(modelo) > 3 and modelo.lower() in q_l:
            sub = df[df["Modelo_norm"] == modelo]
            p = sub["PVP"].dropna()      if "PVP"      in sub.columns else pd.Series()
            c = sub["Cuota_mes"].dropna() if "Cuota_mes" in sub.columns else pd.Series()
            resp = f"**{modelo}** — {len(sub):,} vehículos\n\n"
            if len(p):
                resp += f"- Precio medio: **{p.mean():,.0f} €** (mín {p.min():,.0f} € · máx {p.max():,.0f} €)\n"
                resp += f"- Con precio informado: {len(p)} de {len(sub)}\n"
            if len(c):
                resp += f"- Cuota media: **{c.mean():.0f} €/mes** (mín {c.min():.0f} € · máx {c.max():.0f} €)\n"
                resp += f"- Con cuota informada: {len(c)} de {len(sub)}\n"
            top_d = sub["Concesionario"].value_counts().head(3)
            resp += "\nPrincipales dealers: " + ", ".join([f"{d} ({n})" for d, n in top_d.items()])
            return resp

    # Precio y cuota a la vez
    if re.search(r"precio.*cuota|cuota.*precio|ambos|los dos datos", q_l):
        sub = df[df["PVP"].notna() & df["Cuota_mes"].notna()] if all(c in df.columns for c in ["PVP","Cuota_mes"]) else pd.DataFrame()
        if sub.empty:
            return "No hay vehículos con precio total y cuota mensual a la vez con los filtros actuales."
        top = sub.groupby("Modelo_norm").size().sort_values(ascending=False).head(8)
        lines = "\n".join([f"- **{m}:** {n}" for m, n in top.items()])
        return f"**{len(sub):,} vehículos con precio total Y cuota mensual disponibles:**\n\n{lines}"

    # Sin match
    return (
        "No he encontrado una respuesta directa. Ejemplos de preguntas:\n\n"
        "- *¿Cuál es el precio medio del BMW Serie 1?*\n"
        "- *Compara BMW Serie 3 con Audi A4*\n"
        "- *¿Qué concesionario tiene más coches?*\n"
        "- *Eléctricos con precio inferior a 50000 euros*\n"
        "- *Dame un resumen del stock actual*"
    )


def show_chatbot(df):
    import re as _re
    if "chat_msgs" not in st.session_state:
        st.session_state.chat_msgs = [
            {"role": "bot", "text":
             f"Stock cargado: **{len(df):,} vehículos**. "
             "Puedes preguntarme sobre precios, cuotas, modelos, concesionarios o cualquier dato del dataset."}
        ]

    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_msgs:
        if msg["role"] == "user":
            chat_html += f'<div class="msg-user"><span>{msg["text"]}</span></div>'
        else:
            text = _re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', msg["text"])
            text = text.replace("\n", "<br>")
            chat_html += f'<div class="msg-bot"><span>{text}</span></div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        user_input = c1.text_input(
            "Pregunta:", label_visibility="collapsed",
            placeholder="Ej: ¿Cuál es la cuota media del BMW X1?"
        )
        send = c2.form_submit_button("Enviar")

    if send and user_input.strip():
        st.session_state.chat_msgs.append({"role": "user", "text": user_input})
        resp = _responder(user_input, df)
        st.session_state.chat_msgs.append({"role": "bot", "text": resp})
        st.rerun()

    st.markdown("**Sugerencias:**")
    sugs = [
        "Resumen del stock actual",
        "Modelos con cuota inferior a 400 euros",
        "Concesionario con mas coches",
        "Electricos con precio inferior a 50000",
        "Precio medio del BMW Serie 1",
    ]
    cols = st.columns(len(sugs))
    for col, sug in zip(cols, sugs):
        if col.button(sug, key=f"sug_{sug[:12]}", width="stretch"):
            st.session_state.chat_msgs.append({"role": "user", "text": sug})
            resp = _responder(sug, df)
            st.session_state.chat_msgs.append({"role": "bot", "text": resp})
            st.rerun()

    if st.button("Limpiar conversacion"):
        st.session_state.chat_msgs = []
        st.rerun()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    show_header()
    df_raw = load_data()
    df = sidebar_filters(df_raw)

    if df.empty:
        st.warning("No hay vehículos con los filtros seleccionados.")
        return

    tabs = st.tabs(["Resumen", "Stock", "Precios", "Cuotas", "Comparador", "Tabla", "Asistente"])

    with tabs[0]:
        st.markdown('<div class="section-header">Resumen ejecutivo</div>', unsafe_allow_html=True)
        show_kpis(df)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Insights automaticos</div>', unsafe_allow_html=True)
        show_insights(df)

    with tabs[1]:
        st.markdown('<div class="section-header">Analisis de stock</div>', unsafe_allow_html=True)
        charts_stock(df)

    with tabs[2]:
        st.markdown('<div class="section-header">Analisis de precios</div>', unsafe_allow_html=True)
        charts_precios(df)

    with tabs[3]:
        st.markdown('<div class="section-header">Analisis de cuotas mensuales</div>', unsafe_allow_html=True)
        charts_cuotas(df)

    with tabs[4]:
        st.markdown('<div class="section-header">Comparador de modelos</div>', unsafe_allow_html=True)
        comparador(df)

    with tabs[5]:
        st.markdown('<div class="section-header">Tabla de vehiculos</div>', unsafe_allow_html=True)
        tabla_vehiculos(df)

    with tabs[6]:
        st.markdown('<div class="section-header">Asistente analitico</div>', unsafe_allow_html=True)
        st.caption("El asistente responde calculando directamente sobre los datos filtrados.")
        show_chatbot(df)

    st.markdown(
        '<div style="text-align:center;padding:24px 0 8px;color:#94a3b8;font-size:11px;">' +
        'Stock Intelligence Hub · BMW Group · Datos: STOCK_UNIFICADO_GLOBAL.csv' +
        '</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
