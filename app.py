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
from datetime import datetime
import ast
import base64
import html
import json
import os
import re
import requests
import unicodedata

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Paleta corporativa premium ──────────────
   Azul oscuro principal : #071D3A
   Azul corporativo       : #0057B8
   Azul claro / acento    : #4A90E2
   Fondo general          : #F5F7FA
   Blanco tarjetas        : #FFFFFF
   Texto principal        : #111827
   Texto secundario       : #6B7280
   Bordes suaves          : #E5E7EB
   Verde positivo         : #008A3D
   Rojo negativo          : #D64545
   Gris neutro            : #9CA3AF
──────────────────────────────────────────── */

/* Fondo general de la app */
.stApp {
    background: #F5F7FA;
}

/* Ocultar header de streamlit */
header[data-testid="stHeader"] { background: transparent; }
div[data-testid="stToolbar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* ── Header corporativo (sustituye al header.png) ──
   Banda azul oscura degradada, ocupa todo el ancho */
.app-header-bar {
    display: flex !important;
    align-items: center;
    justify-content: space-between;
    width: calc(100% + 160px) !important;
    max-width: calc(100% + 160px) !important;
    margin-left: -80px !important;
    margin-right: -80px !important;
    margin-top: -96px !important;
    margin-bottom: 1.5rem !important;
    padding: 0 40px;
    height: 88px;
    background: linear-gradient(135deg, #071D3A 0%, #0A2A52 60%, #0057B8 100%);
    box-shadow: 0 2px 10px rgba(7,29,58,0.18);
}
.app-header-text { display: flex; flex-direction: column; gap: 4px; }
.app-header-title {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.01em;
    margin: 0;
}
.app-header-logo-mark {
    display: flex;
    align-items: center;
    margin-top: 2px;
}
.app-header-logo-mark svg { width: 48px; height: 20px; }
.app-header-right {
    display: flex;
    align-items: center;
    gap: 18px;
}
.app-header-update {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #C9D9F0;
    font-size: 11.5px;
    white-space: nowrap;
}
.app-header-update svg { width: 14px; height: 14px; stroke: #C9D9F0; }

/* ── Sidebar: fondo claro y bloques agrupados ─ */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCheckbox span {
    color: #6B7280 !important;
    font-size: 12px;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6 {
    color: #111827 !important;
}
[data-testid="stSidebar"] label p {
    color: #374151 !important;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: #0057B8;
}
[data-testid="stSidebar"] hr {
    border-color: #E5E7EB;
    margin: 18px 0;
}

/* Título del sidebar */
.sidebar-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 700;
    color: #071D3A;
    margin: 4px 0 18px;
}
.sidebar-title svg { width: 18px; height: 18px; stroke: #0057B8; }

/* Bloques de filtros agrupados: "Filtros principales", "Ubicación", etc. */
.sidebar-block-title {
    font-size: 12px;
    font-weight: 700;
    color: #071D3A;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 4px 0 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #E5E7EB;
}

/* -- Inputs del sidebar (selects, sliders, checkboxes) -- */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #F9FAFB;
    border-color: #E5E7EB !important;
    border-radius: 8px;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
    border-color: #4A90E2 !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] div,
[data-testid="stSidebar"] div[data-baseweb="select"] span,
[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color: #111827 !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #6B7280 !important;
}
div[data-baseweb="popover"] li {
    font-size: 12px;
}
div[data-baseweb="popover"] li:hover {
    background: #EAF2FB;
}

/* Botón "Limpiar filtros" */
[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF;
    border: 1px solid #0057B8;
    color: #0057B8;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    width: 100%;
    transition: border-color .15s ease, color .15s ease, background .15s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #0057B8;
    color: #FFFFFF;
    background: #0057B8;
}
[data-testid="stSidebar"] .stButton > button:focus:not(:active) {
    border-color: #0057B8;
    color: #0057B8;
}

/* Sliders */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [role="slider"] {
    background-color: #0057B8 !important;
    border-color: #0057B8 !important;
}
[data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] > div > div {
    background: #4A90E2 !important;
}
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMin"],
[data-testid="stSidebar"] .stSlider div[data-testid="stTickBarMax"] {
    color: #9CA3AF;
    font-size: 10px;
}

/* Checkboxes */
[data-testid="stSidebar"] input[type="checkbox"] {
    accent-color: #0057B8;
}

/* ── Títulos de sección (zona principal) ─────── */
.section-header {
    font-size: 13px;
    font-weight: 700;
    color: #071D3A;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 20px 0 12px;
    margin-bottom: 16px;
    position: relative;
}
.section-header::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 2px;
    background: #4A90E2;
    opacity: 0.35;
}

/* -- Status bar -- */
.status-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11px;
    color: #6B7280;
    letter-spacing: 0.04em;
    margin: -4px 0 18px;
}
.status-bar .sep { color: #E5E7EB; }
.status-bar .mono {
    font-family: 'JetBrains Mono', 'Roboto Mono', monospace;
    font-weight: 600;
    color: #111827;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #008A3D;
    flex-shrink: 0;
    box-shadow: 0 0 0 0 rgba(0,138,61,0.55);
    animation: status-pulse 2s infinite;
}
@keyframes status-pulse {
    0%   { box-shadow: 0 0 0 0 rgba(0,138,61,0.55); }
    70%  { box-shadow: 0 0 0 6px rgba(0,138,61,0); }
    100% { box-shadow: 0 0 0 0 rgba(0,138,61,0); }
}

/* ── Tarjetas KPI premium ─────────────────────
   Icono circular (SVG) + label + valor + delta  */
.kpi-wrap {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 18px 20px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    transition: transform .15s ease, box-shadow .15s ease;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 120px;
}
.kpi-wrap:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15,23,42,0.08);
}
.kpi-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #EAF2FB;
    display: flex;
    align-items: center;
    justify-content: center;
}
.kpi-icon svg { width: 17px; height: 17px; stroke: #0057B8; }
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    color: #6B7280;
    letter-spacing: 0.03em;
    margin-bottom: 2px;
    text-transform: none;
}
.kpi-value {
    font-family: 'Inter', sans-serif;
    font-variant-numeric: tabular-nums;
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    line-height: 1.2;
    letter-spacing: -0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-sub {
    font-size: 12px;
    color: #9CA3AF;
}
.kpi-sub.positive { color: #008A3D; font-weight: 600; }
.kpi-sub.negative { color: #D64545; font-weight: 600; }

/* ── Tarjeta gráfico / contenedor blanco ─────── */
.chart-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    margin-bottom: 18px;
    transition: box-shadow .15s ease;
}
.chart-card:hover {
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}

/* ── Indicador de carga (sustituye al spinner/icono por defecto) ── */
@keyframes sia-spin {
    to { transform: rotate(360deg); }
}
[data-testid="stStatusWidget"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(15,23,42,0.08);
    padding: 6px 14px 6px 36px !important;
    position: relative;
}
[data-testid="stStatusWidget"] svg {
    display: none !important;
}
[data-testid="stStatusWidget"]::before {
    content: "";
    position: absolute;
    left: 12px;
    top: 50%;
    width: 16px;
    height: 16px;
    margin-top: -8px;
    border-radius: 50%;
    border: 2px solid #EAF2FB;
    border-top-color: #0057B8;
    border-right-color: #4A90E2;
    animation: sia-spin 0.7s linear infinite;
}
[data-testid="stStatusWidget"] span {
    color: #071D3A !important;
    font-weight: 600;
    font-size: 12px;
}

div[data-testid="stSpinner"] {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #0057B8;
    font-weight: 600;
    font-size: 13px;
}
div[data-testid="stSpinner"] > div:first-child {
    position: relative;
    width: 20px;
    height: 20px;
    flex: 0 0 auto;
}
div[data-testid="stSpinner"] svg {
    display: none !important;
}
div[data-testid="stSpinner"] > div:first-child::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 3px solid #EAF2FB;
    border-top-color: #0057B8;
    border-right-color: #4A90E2;
    animation: sia-spin 0.7s linear infinite;
}

/* ── Tarjeta para gráficas Plotly (mismo estilo que ranking/donut) ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    margin-bottom: 18px;
    padding: 2px 6px;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}

/* ── Insight box ────────────────────────────── */
.insight-item {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-left: 4px solid #0057B8;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #111827;
    line-height: 1.6;
    box-shadow: 0 1px 4px rgba(15,23,42,0.03);
}
.insight-tag {
    display: inline-block;
    background: #0057B8;
    color: white;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 2px 8px;
    border-radius: 6px;
    margin-right: 8px;
    vertical-align: middle;
}

/* ── Ranking (sustituye a barras horizontales de Plotly) ─ */
.rank-card-title {
    font-size: 13px;
    font-weight: 700;
    color: #071D3A;
    margin: 0 0 16px;
    text-transform: none;
}
.rank-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 11px;
}
.rank-row:last-child { margin-bottom: 0; }
.rank-label {
    flex: 0 0 38%;
    font-size: 12px;
    color: #374151;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: flex;
    align-items: center;
    gap: 8px;
}
.rank-logo {
    width: 18px;
    height: 18px;
    object-fit: contain;
    flex: 0 0 auto;
}
/* ── Tabla comparador con logos en cabecera ──────────────── */
.comp-table-wrap { overflow-x: auto; }
.comp-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.comp-table th, .comp-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #EEF2F8;
    text-align: left;
    white-space: nowrap;
}
.comp-table thead th {
    color: #6B7280;
    font-weight: 600;
    font-size: 12px;
}
.comp-table thead th span {
    display: inline-block;
    vertical-align: middle;
    color: #111827;
    font-size: 13px;
    font-weight: 700;
}
.comp-table thead th .rank-logo {
    width: 20px;
    height: 20px;
    margin-right: 8px;
    vertical-align: middle;
}
.comp-row-label {
    color: #6B7280;
    font-weight: 500;
}
.comp-table tbody tr:last-child td { border-bottom: none; }
.rank-track {
    flex: 1;
    height: 7px;
    background: #EEF2F8;
    border-radius: 4px;
    overflow: hidden;
}
.rank-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #0057B8, #4A90E2);
}
.rank-value {
    flex: 0 0 auto;
    font-size: 12px;
    font-weight: 600;
    color: #111827;
    min-width: 64px;
    text-align: right;
}

/* ── Donut (sustituye a px.pie) ──────────────── */
.donut-wrap {
    display: flex;
    align-items: center;
    gap: 28px;
}
.donut-ring {
    position: relative;
    width: 132px;
    height: 132px;
    border-radius: 50%;
    flex: 0 0 auto;
}
.donut-hole {
    position: absolute;
    top: 22px;
    left: 22px;
    width: 88px;
    height: 88px;
    border-radius: 50%;
    background: #FFFFFF;
}
.donut-legend {
    flex: 1;
    min-width: 0;
}
.legend-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 12px;
    color: #374151;
}
.legend-row:last-child { margin-bottom: 0; }
.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 3px;
    flex: 0 0 auto;
}
.legend-label {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.legend-value {
    flex: 0 0 auto;
    font-weight: 600;
    color: #111827;
}

/* ── Tabla ──────────────────────────────────── */
.vehicle-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}
.vehicle-table th {
    background: #F5F7FA;
    color: #6B7280;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 10px 12px;
    text-align: left;
    position: sticky;
    top: 0;
    border-bottom: 1px solid #E5E7EB;
}
.vehicle-table td {
    padding: 9px 12px;
    border-bottom: 1px solid #F5F7FA;
    color: #111827;
    white-space: nowrap;
}
.vehicle-table tr:hover td { background: #F5F7FA; }
.table-scroll {
    overflow-x: auto;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    max-height: 520px;
    overflow-y: auto;
}
.brand-pill {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
}
.pill-bmw  { background: #EAF2FB; color: #0057B8; }
.pill-audi { background: #E6F4EA; color: #008A3D; }
.pill-mb   { background: #FBEAEA; color: #D64545; }

/* ── Chat ───────────────────────────────────── */
.chat-container {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    min-height: 320px;
    max-height: 420px;
    overflow-y: auto;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    margin-bottom: 12px;
}
.msg-user {
    text-align: right;
    margin: 8px 0;
}
.msg-user span {
    display: inline-block;
    background: #EAF2FB;
    color: #071D3A;
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
    background: #FFFFFF;
    color: #111827;
    padding: 9px 14px;
    border-radius: 12px 12px 12px 2px;
    font-size: 13px;
    max-width: 82%;
    border: 1px solid #E5E7EB;
    line-height: 1.6;
}

/* ── Tabs ─────────────────────────────────────
   Pestaña activa: texto azul + línea inferior azul */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-radius: 12px 12px 0 0;
    gap: 4px;
    border-bottom: 2px solid #E5E7EB;
    padding: 4px 8px 0;
}
.stTabs [data-baseweb="tab"] {
    font-size: 13px;
    font-weight: 600;
    padding: 12px 18px;
    color: #374151;
    border-radius: 8px 8px 0 0;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #0057B8 !important;
    border-bottom: 2px solid #0057B8 !important;
    background: #EAF2FB !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ICONOS (SVG inline estilo "outline", sin emojis)
# ─────────────────────────────────────────────────────────────
ICONS = {
    "car": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14M5 17a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm14 0a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM3 17V11l2-5h12l3 5v6"/><path d="M3 11h16"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.59 2.59 20 10v8a2 2 0 0 1-2 2h-8L2.59 11.59a2 2 0 0 1 0-2.83l7.17-7.17a2 2 0 0 1 2.83 0Z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
    "card": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
    "building": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
    "trophy": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4ZM7 6H4a2 2 0 0 0 0 4h3M17 6h3a2 2 0 0 1 0 4h-3"/></svg>',
    "database": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/><path d="M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-7.5 8-12.5A8 8 0 0 0 4 9.5C4 14.5 12 22 12 22Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "percent": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "filter": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3Z"/></svg>',
    "refresh": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.64-6.36L21 8"/><path d="M21 3v5h-5"/></svg>',
    "broom": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 5 9 15"/><path d="M10.5 19.5 4 13l3-3 6.5 6.5a3 3 0 0 1 0 4.24 3 3 0 0 1-4.24 0Z"/><path d="m17 3 4 4"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10Z"/></svg>',
    "logo": '<svg viewBox="0 0 48 20" fill="none"><path d="M2 14 8 6h4l3 8h2l3-8h4l6 8" stroke="#4A90E2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="8" cy="16" r="1.4" fill="#4A90E2"/><circle cx="40" cy="16" r="1.4" fill="#4A90E2"/><path d="M2 18h44" stroke="#0057B8" stroke-width="1" stroke-linecap="round" opacity="0.5"/></svg>',
}

def icon(name):
    return ICONS.get(name, "")

# ─────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────
BASE = Path(__file__).parent
DATA_SCHEMA_VERSION = "2026-06-10-master-segment-high-performance-published-date"

COLORS = {
    "BMW": "#0057B8",
    "Audi": "#008A3D",
    "Mercedes": "#D64545",
    "Mercedes-Benz": "#D64545",
}

def _logo_b64(name):
    p = BASE / "assets" / f"logo_{name}.png"
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode()

_BRAND_LOGOS = {
    "BMW": _logo_b64("bmw"),
    "Audi": _logo_b64("audi"),
    "Mercedes": _logo_b64("mercedes"),
    "Mercedes-Benz": _logo_b64("mercedes"),
}
FUEL_COLORS = {
    "ICE":  "#64748b",
    "HEV":  "#16a34a",
    "MHEV": "#0ea5e9",
    "BEV":  "#16a34a",
    "PHEV": "#d97706",
}
TPL = "plotly_white"

def fig_base(fig, h=310):
    fig.update_layout(
        template=TPL,
        height=h,
        margin=dict(l=8, r=8, t=32, b=8),
        font=dict(family="Inter", size=11, color="#6B7280"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        separators=",.",
        bargap=0.35,
        colorway=["#0057B8", "#4A90E2", "#9CB8E0", "#071D3A", "#7FB3F0", "#C9D9F0"],
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font_size=10,
        ),
    )
    fig.update_xaxes(
        showgrid=False, showline=False, zeroline=False,
        ticks="", tickfont_size=10, color="#9CA3AF",
    )
    fig.update_yaxes(
        showgrid=False, showline=False, zeroline=False,
        ticks="", tickfont_size=10, color="#9CA3AF",
    )
    return fig

def plotly_card(fig, title, h=300):
    """Envuelve una figura Plotly en una tarjeta blanca con título estilo
    'rank-card-title' (igual que render_ranking/render_donut), sin barra de
    herramientas ni título nativo de Plotly, para que todas las gráficas
    compartan el mismo aspecto."""
    fig.update_layout(title="", height=h)
    fig.update_layout(legend=dict(
        title="", orientation="h", yanchor="bottom", y=1.02,
        xanchor="left", x=0, font_size=10,
    ))
    fig.update_layout(margin=dict(t=36))
    with st.container(border=True):
        st.markdown(f'<p class="rank-card-title">{title}</p>', unsafe_allow_html=True)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

def model_brand_map(df):
    """Devuelve {Modelo_norm: Marca} usando la marca más frecuente de cada modelo."""
    if "Modelo_norm" not in df.columns or "Marca" not in df.columns:
        return {}
    gb = df.groupby(["Modelo_norm", "Marca"]).size().reset_index(name="N")
    gb = gb.sort_values("N", ascending=False).drop_duplicates("Modelo_norm")
    return dict(zip(gb["Modelo_norm"], gb["Marca"]))

def render_ranking(title, rows, fmt=None, max_val=None, empty_msg="Sin datos disponibles.", colors=None, row_brands=None, show_logos=False):
    """Lista tipo ranking con barras de progreso en HTML/CSS (sustituye a px.bar horizontal).

    `colors`: dict opcional {texto: color}. Si la etiqueta de una fila contiene
    (o coincide con) una de las claves, la barra de esa fila se pinta con ese
    color en lugar del degradado azul por defecto (p.ej. para distinguir
    marcas: BMW azul, Mercedes rojo, Audi verde).

    `row_brands`: lista opcional (mismo largo que `rows`) con la marca de cada
    fila ("BMW"/"Audi"/"Mercedes"...). Si se indica, la barra de esa fila se
    pinta con el color corporativo de esa marca.
    """
    fmt = fmt or (lambda v: str(v))
    rows = [(str(label), float(value)) for label, value in rows if value is not None]
    if not rows:
        st.markdown(
            f'<div class="chart-card"><p class="rank-card-title">{title}</p>'
            f'<p style="color:#9CA3AF;font-size:12px;margin:0;">{empty_msg}</p></div>',
            unsafe_allow_html=True,
        )
        return
    mx = max_val if max_val else max(v for _, v in rows)
    mx = mx or 1
    items_html = []
    for i, (label, value) in enumerate(rows):
        pct = max(2.0, min(100.0, (value / mx) * 100))
        fill_style = "background: linear-gradient(90deg, #0057B8, #4A90E2)"
        brand = row_brands[i] if row_brands and i < len(row_brands) else None
        if brand:
            c = COLORS.get(brand, "#9CA3AF")
            fill_style = f"background:{c}"
        elif colors:
            c = colors.get(label)
            if c is None:
                c = next((v for k, v in colors.items() if k in label), None)
            if c:
                fill_style = f"background:{c}"
        logo_html = ""
        if show_logos:
            b64 = _BRAND_LOGOS.get(brand or label)
            if b64:
                logo_html = f'<img class="rank-logo" src="data:image/png;base64,{b64}" />'
        items_html.append(
            f'<div class="rank-row">'
            f'<div class="rank-label">{logo_html}<span>{label}</span></div>'
            f'<div class="rank-track"><div class="rank-fill" style="width:{pct:.1f}%;{fill_style}"></div></div>'
            f'<div class="rank-value">{fmt(value)}</div>'
            f'</div>'
        )
    st.markdown(
        f'<div class="chart-card"><p class="rank-card-title">{title}</p>{"".join(items_html)}</div>',
        unsafe_allow_html=True,
    )

_DONUT_PALETTE = ["#0057B8", "#4A90E2", "#9CB8E0", "#071D3A", "#7FB3F0", "#C9D9F0", "#D64545", "#008A3D"]

def render_donut(title, rows, colors=None, empty_msg="Sin datos disponibles."):
    """Donut + leyenda en HTML/CSS (sustituye a px.pie)."""
    rows = [(str(label), float(value)) for label, value in rows if value is not None and float(value) > 0]
    if not rows:
        st.markdown(
            f'<div class="chart-card"><p class="rank-card-title">{title}</p>'
            f'<p style="color:#9CA3AF;font-size:12px;margin:0;">{empty_msg}</p></div>',
            unsafe_allow_html=True,
        )
        return
    total = sum(v for _, v in rows)
    colors = colors or {}
    stops, legend_items, acc = [], [], 0.0
    for i, (label, value) in enumerate(rows):
        pct = value / total * 100
        c = colors.get(label, _DONUT_PALETTE[i % len(_DONUT_PALETTE)])
        stops.append(f"{c} {acc:.3f}% {acc + pct:.3f}%")
        acc += pct
        legend_items.append(
            f'<div class="legend-row">'
            f'<span class="legend-dot" style="background:{c}"></span>'
            f'<span class="legend-label">{label}</span>'
            f'<span class="legend-value">{pct:.1f}%</span>'
            f'</div>'
        )
    gradient = ", ".join(stops)
    st.markdown(
        f'<div class="chart-card"><p class="rank-card-title">{title}</p>'
        f'<div class="donut-wrap">'
        f'<div class="donut-ring" style="background:conic-gradient({gradient})"><div class="donut-hole"></div></div>'
        f'<div class="donut-legend">{"".join(legend_items)}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# CARGA Y NORMALIZACIÓN DE DATOS
# ─────────────────────────────────────────────────────────────
def _safe_excel(path):
    try:
        return pd.read_excel(path, engine="openpyxl")
    except Exception:
        return None

_BRAND_PREFIX = re.compile(r"^(Mercedes(?:-Benz)?|BMW|Audi|MINI)\s+", re.IGNORECASE)
_BMW_SERIES_KEY_RE = re.compile(
    r"^(?:serie|series)\s+([1-8])\b|^([1-8])\s+(?:series?|active tourer|gran tourer|gran coupe|coup[eé]|cabrio|berlina|touring)\b",
    re.IGNORECASE,
)
_MERCEDES_CLASS_MAP = {
    "a": "Clase A", "b": "Clase B", "c": "Clase C", "e": "Clase E", "s": "Clase S",
    "g": "Clase G", "t": "Clase T", "v": "Clase V",
    "cla": "Clase CLA", "cle": "Clase CLE", "cls": "Clase CLS",
    "gla": "Clase GLA", "glb": "Clase GLB", "glc": "Clase GLC", "gle": "Clase GLE",
    "gls": "Clase GLS", "sl": "Clase SL",
}
_MERCEDES_CLASS_RE = re.compile(r"^(?:clase|class)\s+([a-z0-9]+)$|^([a-z0-9]+)\s*[- ]?\s*class$", re.IGNORECASE)
_AUDI_MODEL_PREFIXES = [
    "A1 Sportback", "A1 allstreet", "A3 Sportback", "A3 Limousine", "A3 allstreet",
    "A5 Avant", "A5 Limousine", "A5", "A6 Avant e-tron", "A6 Sportback e-tron",
    "A6 Avant", "A6 Limousine", "Q2", "Q3 Sportback e-hybrid", "Q3 SUV e-hybrid",
    "Q3 Sportback", "Q3 SUV", "Q3", "Q4 Sportback e-tron", "Q4 SUV e-tron",
    "Q5 Sportback", "Q5 SUV", "Q5", "Q6 Sportback e-tron", "Q6 SUV e-tron", "Q7", "Q8",
]

def _norm_key(value):
    s = unicodedata.normalize("NFD", str(value or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^0-9A-Za-z]+", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()

def normalize_brand_name(value):
    key = _norm_key(value)
    if key in {"mercedes", "mercedes benz", "mercedes-benz"}:
        return "Mercedes"
    if key == "bmw":
        return "BMW"
    if key == "audi":
        return "Audi"
    return re.sub(r"\s+", " ", str(value or "")).strip()

def clean_model_name(value, brand=""):
    model = re.sub(r"\s+", " ", str(value or "")).strip()
    if not model:
        return ""
    model = _BRAND_PREFIX.sub("", model).strip()
    key = _norm_key(model)
    version_key = key
    brand = normalize_brand_name(brand)

    bm = _BMW_SERIES_KEY_RE.match(key)
    if bm:
        return f"Serie {bm.group(1) or bm.group(2)}"
    if brand == "BMW":
        bmw = re.match(r"^(i?x[1-7]|m[1-8])\b", key, re.IGNORECASE)
        if bmw:
            code = bmw.group(1)
            if code.lower().startswith("m"):
                return f"Serie {code[-1]}"
            return "i" + code[1:].upper() if code.lower().startswith("ix") else code.upper()

    mc = _MERCEDES_CLASS_RE.match(key)
    if mc:
        code = (mc.group(1) or mc.group(2) or "").lower()
        return _MERCEDES_CLASS_MAP.get(code, f"Clase {code.upper()}")
    if key in _MERCEDES_CLASS_MAP:
        return _MERCEDES_CLASS_MAP[key]
    if brand == "Mercedes":
        if "amg gt" in key:
            return "AMG GT"
        if "mercedes amg a" in key:
            return "Clase A"
        if "mercedes amg c" in key:
            return "Clase C"
        if "mercedes amg e" in key or re.match(r"^e\d", key):
            return "Clase E"
        if "mercedes amg g " in f"{key} ":
            return "Clase G"
        if "glc" in key and ("coupe" in key or "coup" in key):
            return "Clase GLC Coupe"
        if "gle" in key and ("coupe" in key or "coup" in key):
            return "Clase GLE Coupe"
        for code in sorted(_MERCEDES_CLASS_MAP, key=len, reverse=True):
            if key == code or key.startswith(code + " ") or re.match(rf"^{code}\d", key):
                return _MERCEDES_CLASS_MAP[code]
        eq = re.match(r"^(eqa|eqb|eqc|eqe|eqs)\b", key, re.IGNORECASE)
        if eq:
            return eq.group(1).upper()

    if brand == "Audi":
        if "e tron gt" in key or "etron gt" in key:
            return "e-tron GT"
        if key.startswith(("rs 3", "rs3", "s3")):
            return "A3"
        if key.startswith(("s5", "rs5")):
            return "A5"
        if key.startswith("sq5"):
            return "Q5"
        for prefix in sorted(_AUDI_MODEL_PREFIXES, key=len, reverse=True):
            prefix_key = _norm_key(prefix)
            if key == prefix_key or key.startswith(prefix_key + " "):
                if prefix.startswith("A1"):
                    return "A1"
                if prefix.startswith("A3"):
                    return "A3"
                if prefix.startswith("A5"):
                    return "A5"
                if prefix.startswith("A6"):
                    return "A6"
                if prefix.startswith("Q3 Sportback"):
                    return "Q3 Sportback"
                if prefix.startswith("Q3"):
                    return "Q3"
                if prefix.startswith("Q4 Sportback"):
                    return "Q4 Sportback e-tron"
                if prefix.startswith("Q4"):
                    return "Q4 e-tron"
                if prefix.startswith("Q5 Sportback"):
                    return "Q5 Sportback"
                if prefix.startswith("Q5"):
                    return "Q5"
                if prefix.startswith("Q6 Sportback"):
                    return "Q6 e-tron Sportback"
                if prefix.startswith("Q6"):
                    return "Q6 e-tron"
                return prefix
        if "e tron gt" in key or "etron gt" in key:
            return "e-tron GT"

    return model.replace("Série", "Serie")

def clean_body_type(model="", body="", version=""):
    model_key = _norm_key(model)
    body_key = _norm_key(body)
    version_key = _norm_key(version)
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

def _post_normalize(df):
    df = df.copy()
    if "Marca" in df.columns:
        df["Marca"] = df["Marca"].map(normalize_brand_name)
    if "Modelo" in df.columns:
        if "Marca" in df.columns:
            df["Modelo"] = [clean_model_name(model, brand) for model, brand in zip(df["Modelo"], df["Marca"])]
        else:
            df["Modelo"] = df["Modelo"].map(clean_model_name)
        df["Modelo_norm"] = df["Modelo"]
    elif "Modelo_norm" in df.columns:
        if "Marca" in df.columns:
            df["Modelo_norm"] = [clean_model_name(model, brand) for model, brand in zip(df["Modelo_norm"], df["Marca"])]
        else:
            df["Modelo_norm"] = df["Modelo_norm"].map(clean_model_name)
        df["Modelo"] = df["Modelo_norm"]

    for c in ["PVP", "Cuota_mes", "TAE", "TIN", "Entrada", "Cuota_final", "Plazo", "Año"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["Marca", "Mercado", "Modelo_norm", "Modelo", "Versión", "Fecha", "Fecha Publicacion", "Fuel_type", "Carrocería", "Segment", "High_Performance", "Concesionario", "Ciudad", "Provincia"]:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str).str.strip()
    if "Fuel_type" in df.columns:
        df["Fuel_type"] = df["Fuel_type"].replace({"HEV": "ICE", "MHEV": "ICE"})
    body_col = next((c for c in df.columns if _norm_key(c) in {"carroceria", "body_type", "body"}), None)
    version_col = next((c for c in df.columns if _norm_key(c) in {"version", "versao"}), None)
    model_col = "Modelo_norm" if "Modelo_norm" in df.columns else ("Modelo" if "Modelo" in df.columns else None)
    if body_col and model_col:
        versions = df[version_col] if version_col else pd.Series([""] * len(df), index=df.index)
        df[body_col] = [
            clean_body_type(model, body, version)
            for model, body, version in zip(df[model_col], df[body_col], versions)
        ]
    return df

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
        "Published_Date":"Fecha Publicacion",
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
        "Deposit_EUR":   "Entrada",
        "Final_Installment_EUR": "Cuota_final",
        "Term_Months":   "Plazo",
        "Availability":  "Estado",
        "Engine_Raw":    "Motor",
    })
    df["Modelo_norm"] = df["Modelo"]
    for c in ["TIN","Entrada","Plazo","Cuota_final","Km_año"]:
        if c not in df.columns:
            df[c] = np.nan
    return _post_normalize(df)

def _norm_es(df, mercado="ES"):
    df = df.copy()
    df["Mercado"] = mercado
    df = df.rename(columns={
        "PVP (€)":          "PVP",
        "PVP (EUR)":        "PVP",
        "Cuota/mes (€)":    "Cuota_mes",
        "Cuota/mes (EUR)":  "Cuota_mes",
        "Cuota Final (€)":  "Cuota_final",
        "Cuota Final (EUR)":"Cuota_final",
        "TAE (%)":          "TAE",
        "TIN (%)":          "TIN",
        "Entrada (€)":      "Entrada",
        "Entrada (EUR)":    "Entrada",
        "Plazo (meses)":    "Plazo",
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
    return _post_normalize(df)

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
    return _post_normalize(df)

@st.cache_data(show_spinner="Cargando datos...")
def load_data():
    _ = DATA_SCHEMA_VERSION
    # 1. CSV recuperado del GLOBAL (fuente principal — siempre disponible)
    csv_f = BASE / "STOCK_UNIFICADO_GLOBAL.csv"
    if csv_f.exists():
        df = pd.read_csv(csv_f, low_memory=False)
        if len(df) > 100:
            return _norm_csv(df)

    # 2. XLSX global (si no está bloqueado por Excel)
    df_g = _safe_excel(BASE / "STOCK_UNIFICADO_GLOBAL.xlsx")
    if df_g is not None and len(df_g) > 100:
        if "Market" in df_g.columns or "Brand" in df_g.columns:
            return _norm_csv(df_g)
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
    return _post_normalize(df)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
def show_header(updated="—"):
    """Header corporativo: título y logo futurista a la izquierda,
    fecha de actualización a la derecha."""
    st.markdown(
        f'''
        <div class="app-header-bar">
            <div class="app-header-text">
                <p class="app-header-title">Stock Intelligence App</p>
                <div class="app-header-logo-mark">{icon("logo")}</div>
            </div>
            <div class="app-header-right">
                <div class="app-header-update">
                    {icon("refresh")}
                    <span>Última actualización: {updated}</span>
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# SIDEBAR — FILTROS
# ─────────────────────────────────────────────────────────────
def sidebar_filters(df):
    with st.sidebar:
        st.markdown(f'<div class="sidebar-title">{icon("filter")}Filtros</div>', unsafe_allow_html=True)

        filter_defs = [
            ("Marca", "Marca", "f_Marca"),
            ("Mercado", "Mercado", "f_Mercado"),
            ("Modelo", "Modelo_norm", "f_Modelo_norm"),
            ("Versión", "Versión", "f_Versión"),
            ("Combustible", "Fuel_type", "f_Fuel_type"),
            ("Carrocería", "Carrocería", "f_Carrocería"),
            ("Segmento", "Segment", "f_Segment"),
            ("High Performance", "High_Performance", "f_High_Performance"),
            ("Concesionario", "Concesionario", "f_Concesionario"),
            ("Ciudad", "Ciudad", "f_Ciudad"),
            ("Provincia", "Provincia", "f_Provincia"),
            ("Año", "Año", "f_año"),
        ]
        filter_keys = [key for _, _, key in filter_defs]
        range_keys = ["f_pvp_range", "f_cuota_range", "f_solo_pvp", "f_solo_cuota"]

        if st.button("Limpiar filtros", width="stretch"):
            for key in filter_keys + range_keys:
                st.session_state.pop(key, None)
            st.rerun()

        def selected_for(key):
            value = st.session_state.get(key, [])
            return value if isinstance(value, list) else []

        def mask_from_filters(exclude_col=None):
            mask = pd.Series(True, index=df.index)
            for _, col, key in filter_defs:
                if col == exclude_col or col not in df.columns:
                    continue
                sel = selected_for(key)
                if sel:
                    mask &= df[col].isin(sel)
            return mask

        def clean_options(col, opts):
            values = []
            for x in opts:
                if pd.isna(x):
                    continue
                if col == "Año":
                    values.append(int(x))
                    continue
                text = str(x).strip()
                if text and text.lower() not in {"nan", "none"}:
                    values.append(text)
            return sorted(set(values))

        def options_for(col):
            if col not in df.columns:
                return []
            base = df.loc[mask_from_filters(exclude_col=col), col].dropna()
            return clean_options(col, base.tolist())

        def msel(label, col, key):
            opts = options_for(col)
            current = [x for x in selected_for(key) if x in opts]
            if st.session_state.get(key, []) != current:
                st.session_state[key] = current
            return st.multiselect(label, opts, key=key)

        # ── Bloque: Filtros principales ──────────────────
        st.markdown('<div class="sidebar-block-title">Filtros principales</div>', unsafe_allow_html=True)
        marcas     = msel("Marca",          "Marca",          "f_Marca")
        modelos    = msel("Modelo",         "Modelo_norm",    "f_Modelo_norm")
        versiones  = msel("Versión",        "Versión",        "f_Versión")
        fuels      = msel("Combustible",    "Fuel_type",      "f_Fuel_type")
        carros     = msel("Carrocería",     "Carrocería",     "f_Carrocería")
        segmentos  = msel("Segmento",       "Segment",        "f_Segment")
        high_perf  = msel("High Performance", "High_Performance", "f_High_Performance")
        años = msel("Año", "Año", "f_año")

        st.markdown("---")

        # ── Bloque: Ubicación ─────────────────────────────
        st.markdown('<div class="sidebar-block-title">Ubicación</div>', unsafe_allow_html=True)
        mercados   = msel("Mercado",        "Mercado",        "f_Mercado")
        provincias = msel("Provincia",      "Provincia",      "f_Provincia")
        ciudades   = msel("Ciudad",         "Ciudad",         "f_Ciudad")
        dealers    = msel("Concesionario",  "Concesionario",  "f_Concesionario")

        st.markdown("---")

        # ── Bloque: Precio y financiación ─────────────────
        st.markdown('<div class="sidebar-block-title">Precio y financiación</div>', unsafe_allow_html=True)

        # Slider PVP
        pvp_s = df["PVP"].dropna() if "PVP" in df.columns else pd.Series(dtype=float)
        if len(pvp_s) > 0:
            pmin, pmax = float(pvp_s.min()), float(pvp_s.max())
            pmax = pmax if pmax > pmin else pmin + 1.0
            pvp_r = st.slider("Precio (€)", pmin, pmax, (pmin, pmax), step=500.0, format="%.0f€", key="f_pvp_range")
        else:
            pvp_r = (0, 999999)

        # Slider Cuota
        cuota_s = df["Cuota_mes"].dropna() if "Cuota_mes" in df.columns else pd.Series(dtype=float)
        if len(cuota_s) > 0:
            cmin, cmax = float(cuota_s.min()), float(cuota_s.max())
            cmax = cmax if cmax > cmin else cmin + 1.0
            cuota_r = st.slider("Cuota/mes (€)", cmin, cmax, (cmin, cmax), step=10.0, format="%.0f€", key="f_cuota_range")
        else:
            cuota_r = (0, 99999)

        solo_pvp   = st.checkbox("Solo con precio informado",       False, key="f_solo_pvp")
        solo_cuota = st.checkbox("Solo con cuota mensual informada", False, key="f_solo_cuota")

    # Aplicar
    mask = pd.Series(True, index=df.index)
    for col, sel in [
        ("Marca", marcas), ("Mercado", mercados), ("Modelo_norm", modelos), ("Versión", versiones),
        ("Fuel_type", fuels), ("Carrocería", carros), ("Segment", segmentos),
        ("High_Performance", high_perf), ("Concesionario", dealers),
        ("Ciudad", ciudades), ("Provincia", provincias),
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
def kpi(label, value, sub="", icon_name="chart", sub_class=""):
    cls = f"kpi-sub {sub_class}".strip()
    sub_html = f'<div class="{cls}">{sub}</div>' if sub else ""
    return (
        f'<div class="kpi-wrap">'
        f'<div class="kpi-icon">{icon(icon_name)}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{sub_html}</div>'
    )

def eu_num(x, dec=0):
    """Formato europeo: 1.234,56"""
    if not pd.notna(x) or x != x:
        return "—"
    s = f"{float(x):,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def eur(x, dec=0):
    return f"{eu_num(x, dec)} €" if pd.notna(x) and x == x else "—"

def eur2(x):
    return eur(x, 2)

def eu_mes(x):
    return f"{eur(x, 0)}/mes" if pd.notna(x) and x == x else "—"

def pct(n, d, dec=1):
    return f"{(n / d * 100):.{dec}f}%".replace(".", ",") if d > 0 else "—"

def pct_val(x, dec=1):
    return f"{x:.{dec}f}%".replace(".", ",") if pd.notna(x) and x == x else "—"

def fmt_date(value):
    if value is None or not pd.notna(value):
        return "—"
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "nat"}:
        return "—"
    dt = pd.to_datetime(text, errors="coerce")
    if pd.isna(dt):
        return text[:10]
    return dt.strftime("%d/%m/%Y")

def publication_dates(df):
    if "Fecha Publicacion" not in df.columns:
        return pd.Series(dtype="datetime64[ns]")
    return pd.to_datetime(df["Fecha Publicacion"], errors="coerce").dropna()

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

    tae_s = df["TAE"].dropna() if "TAE" in df.columns else pd.Series()

    row1 = st.columns(4)
    datos_r1 = [
        ("Total vehículos",   eu_num(total),              "en stock", "car"),
        ("Con precio",        eu_num(n_pvp),              pct(n_pvp, total), "tag"),
        ("Con cuota/mes",     eu_num(n_cuota),            pct(n_cuota, total), "card"),
        ("Precio medio",      eur(pvp_s.mean()),          f"Mín. {eur(pvp_s.min())} · Máx. {eur(pvp_s.max())}", "tag"),
    ]
    for col, (l, v, s, ic) in zip(row1, datos_r1):
        col.markdown(kpi(l, v, s, icon_name=ic), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    row2 = st.columns(4)
    datos_r2 = [
        ("Cuota media",       eu_mes(cuota_s.mean()) if len(cuota_s) else "—",
         f"Mín. {eur(cuota_s.min())} · Máx. {eur(cuota_s.max())}" if len(cuota_s) else "", "card"),
        ("Marcas",            str(df["Marca"].nunique()),  "analizadas", "car"),
        ("Modelos",           str(n_mods),                 "distintos", "car"),
        ("Concesionarios",    str(n_deal),                 "analizados", "building"),
    ]
    for col, (l, v, s, ic) in zip(row2, datos_r2):
        col.markdown(kpi(l, v, s, icon_name=ic), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    row3 = st.columns(4)
    datos_r3 = [
        ("Modelo top stock",  str(top_modelo)[:26],        "más unidades", "trophy"),
        ("Ciudad con más stock", str(top_ciudad),          "", "pin"),
        ("Dealer principal",  str(top_dealer)[:24],        "", "building"),
        ("TAE media",         pct_val(tae_s.mean(), 2) if len(tae_s) else "—", "sobre financiados", "percent"),
    ]
    for col, (l, v, s, ic) in zip(row3, datos_r3):
        col.markdown(kpi(l, v, s, icon_name=ic), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CHARTS — STOCK
# ─────────────────────────────────────────────────────────────
def charts_stock(df):
    c1, c2 = st.columns(2)

    with c1:
        gb = df.groupby("Marca").size().reset_index(name="N").sort_values("N", ascending=False)
        render_ranking(
            "Stock por marca",
            list(zip(gb["Marca"], gb["N"])),
            fmt=lambda v: eu_num(int(v)),
            colors=COLORS,
            show_logos=True,
        )

    with c2:
        gb2 = df.groupby("Fuel_type").size().reset_index(name="N").sort_values("N", ascending=False)
        render_donut(
            "Distribución por combustible",
            list(zip(gb2["Fuel_type"], gb2["N"])),
            colors=FUEL_COLORS,
        )

    c3, c4 = st.columns(2)

    with c3:
        all_m = df.groupby("Modelo_norm").size().reset_index(name="N").sort_values("N", ascending=False)
        model_brand = model_brand_map(df)
        top10 = all_m.head(10)
        render_ranking(
            "Top 10 modelos por unidades",
            list(zip(top10["Modelo_norm"], top10["N"])),
            fmt=lambda v: eu_num(int(v)),
            row_brands=[model_brand.get(m) for m in top10["Modelo_norm"]],
        )
        with st.expander("Ver todos los modelos"):
            st.dataframe(all_m.reset_index(drop=True), width="stretch", height=280, hide_index=True)

    with c4:
        all_d = df.groupby("Concesionario").size().reset_index(name="N").sort_values("N", ascending=False)
        render_ranking(
            "Top 10 concesionarios",
            list(zip(all_d.head(10)["Concesionario"], all_d.head(10)["N"])),
            fmt=lambda v: eu_num(int(v)),
        )
        with st.expander("Ver todos los concesionarios"):
            st.dataframe(all_d.reset_index(drop=True), width="stretch", height=280, hide_index=True)

    if "Ciudad" in df.columns and df["Ciudad"].notna().any():
        top_c = df.groupby("Ciudad").size().reset_index(name="N").sort_values("N", ascending=False).head(20)
        render_ranking(
            "Top 20 ciudades por stock",
            list(zip(top_c["Ciudad"], top_c["N"])),
            fmt=lambda v: eu_num(int(v)),
        )

    if "Carrocería" in df.columns and df["Carrocería"].notna().any():
        c5, c6 = st.columns(2)
        with c5:
            gb_c = df.groupby("Carrocería").size().reset_index(name="N").sort_values("N", ascending=False)
            render_ranking(
                "Stock por tipo de carrocería",
                list(zip(gb_c["Carrocería"], gb_c["N"])),
                fmt=lambda v: eu_num(int(v)),
            )

        with c6:
            gb_m = df.groupby("Mercado").size().reset_index(name="N")
            render_donut(
                "Stock por mercado",
                list(zip(gb_m["Mercado"], gb_m["N"])),
            )

    if "Fecha Publicacion" in df.columns:
        recent = df.copy()
        recent["_FechaPub_dt"] = pd.to_datetime(recent["Fecha Publicacion"], errors="coerce")
        recent = recent.dropna(subset=["_FechaPub_dt"]).sort_values("_FechaPub_dt", ascending=False)
        if not recent.empty:
            stock_cols = [c for c in [
                "Marca", "Modelo_norm", "Versión", "Fecha Publicacion",
                "PVP", "Cuota_mes", "Fuel_type", "Concesionario", "Ciudad", "URL",
            ] if c in recent.columns]
            recent = recent[stock_cols].copy()
            recent["Fecha Publicacion"] = recent["Fecha Publicacion"].map(fmt_date)
            if "PVP" in recent.columns:
                recent["PVP"] = recent["PVP"].map(eur)
            if "Cuota_mes" in recent.columns:
                recent["Cuota_mes"] = recent["Cuota_mes"].map(eu_mes)
            recent = recent.rename(columns={
                "Modelo_norm": "Modelo",
                "PVP": "Precio",
                "Cuota_mes": "Cuota/mes",
                "Fuel_type": "Combustible",
            })
            st.markdown('<div class="section-header">Ultimas publicaciones</div>', unsafe_allow_html=True)
            st.caption(f"{eu_num(len(recent))} vehiculos mas recientes con los filtros actuales")
            st.dataframe(recent, width="stretch", hide_index=True)

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
        gb = df_pvp.groupby("Marca")["PVP"].agg(["mean","min","max"]).reset_index().sort_values("mean", ascending=False)
        render_ranking(
            "Precio medio por marca",
            list(zip(gb["Marca"], gb["mean"])),
            fmt=lambda v: eur(v),
            colors=COLORS,
            show_logos=True,
        )

    with c2:
        fig2 = px.histogram(df_pvp, x="PVP", color="Marca",
                            color_discrete_map=COLORS, nbins=50,
                            labels={"PVP":"Precio (€)","count":"Vehículos"},
                            barmode="overlay", opacity=0.72)
        plotly_card(fig_base(fig2), "Distribución de precios")

    c3, c4 = st.columns(2)

    with c3:
        grp = (df_pvp.groupby("Modelo_norm")["PVP"]
               .agg(["mean","count"]).reset_index()
               .query("count >= 3")
               .sort_values("mean", ascending=False).head(15))
        model_brand = model_brand_map(df_pvp)
        render_ranking(
            "Precio medio — top 15 modelos (≥3 uds.)",
            list(zip(grp["Modelo_norm"], grp["mean"])),
            fmt=lambda v: eur(v),
            row_brands=[model_brand.get(m) for m in grp["Modelo_norm"]],
            empty_msg="No hay suficientes unidades por modelo con los filtros actuales.",
        )

    with c4:
        fig4 = px.box(df_pvp, x="Marca", y="PVP", color="Marca",
                      color_discrete_map=COLORS,
                      labels={"PVP":"Precio (€)"})
        fig4.update_layout(showlegend=False)
        plotly_card(fig_base(fig4), "Dispersión de precios por marca")

    if "Fuel_type" in df_pvp.columns:
        gb_f = df_pvp.groupby(["Fuel_type","Marca"])["PVP"].mean().reset_index().sort_values("PVP", ascending=False)
        render_ranking(
            "Precio medio por combustible y marca",
            list(zip(gb_f["Fuel_type"] + " — " + gb_f["Marca"], gb_f["PVP"])),
            fmt=lambda v: eur(v),
            colors=COLORS,
        )

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
        gb = df_c.groupby("Marca")["Cuota_mes"].mean().reset_index().sort_values("Cuota_mes", ascending=False)
        render_ranking(
            "Cuota mensual media por marca",
            list(zip(gb["Marca"], gb["Cuota_mes"])),
            fmt=lambda v: eu_mes(v),
            colors=COLORS,
            show_logos=True,
        )

    with c2:
        fig2 = px.histogram(df_c, x="Cuota_mes", color="Marca",
                            color_discrete_map=COLORS, nbins=40,
                            labels={"Cuota_mes":"Cuota (€/mes)"},
                            barmode="overlay", opacity=0.72)
        plotly_card(fig_base(fig2), "Distribución de cuotas mensuales")

    c3, c4 = st.columns(2)

    with c3:
        grp = (df_c.groupby("Modelo_norm")["Cuota_mes"]
               .agg(["mean","count"]).reset_index()
               .query("count >= 3").sort_values("mean").head(15))
        model_brand = model_brand_map(df_c)
        render_ranking(
            "Cuota media más baja — top 15 modelos",
            list(zip(grp["Modelo_norm"], grp["mean"])),
            fmt=lambda v: eu_mes(v),
            row_brands=[model_brand.get(m) for m in grp["Modelo_norm"]],
            empty_msg="No hay suficientes unidades por modelo con los filtros actuales.",
        )

    with c4:
        df_both = df[(df["PVP"].notna()) & (df["Cuota_mes"].notna())].copy() if "PVP" in df.columns else pd.DataFrame()
        if not df_both.empty:
            fig4 = px.scatter(df_both, x="PVP", y="Cuota_mes", color="Marca",
                              color_discrete_map=COLORS, opacity=0.55,
                              labels={"PVP":"Precio (€)","Cuota_mes":"Cuota (€/mes)"},
                              hover_data=["Modelo_norm"])
            plotly_card(fig_base(fig4), "Precio total vs cuota mensual")

    if "TAE" in df_c.columns and df_c["TAE"].notna().any():
        c5, _ = st.columns(2)
        with c5:
            gb_t = df_c.groupby("Marca")["TAE"].mean().reset_index().sort_values("TAE", ascending=False)
            render_ranking(
                "TAE media por marca",
                list(zip(gb_t["Marca"], gb_t["TAE"])),
                fmt=lambda v: pct_val(v, 2),
                colors=COLORS,
                show_logos=True,
            )

# ─────────────────────────────────────────────────────────────
# COMPARADOR DE MODELOS
# ─────────────────────────────────────────────────────────────
def comparador(df):
    modelos_disp = sorted(df["Modelo_norm"].dropna().unique().tolist())
    sel = st.multiselect(
        "Selecciona dos o más modelos:",
        modelos_disp,
        default=[],
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
        entrada = sub["Entrada"].dropna() if "Entrada" in sub.columns else pd.Series()
        tin   = sub["TIN"].dropna()   if "TIN"      in sub.columns else pd.Series()
        tae   = sub["TAE"].dropna()   if "TAE"      in sub.columns else pd.Series()
        plazo = sub["Plazo"].dropna() if "Plazo"    in sub.columns else pd.Series()
        pub   = publication_dates(sub)
        top_fuel  = sub["Fuel_type"].mode()[0]       if "Fuel_type" in sub.columns and not sub["Fuel_type"].isna().all() else "—"
        top_dealer= sub["Concesionario"].value_counts().idxmax() if "Concesionario" in sub.columns and not sub["Concesionario"].isna().all() else "—"
        rows.append({
            "Modelo":             m,
            "Stock total":        eu_num(len(sub)),
            "Fecha Publicacion":  fmt_date(pub.max()) if len(pub) else "—",
            "Con precio":         eu_num(len(pvp)),
            "Con cuota":          eu_num(len(cuota)),
            "Precio medio (€)":   eur(pvp.mean())   if len(pvp)   else "—",
            "Precio mín. (€)":    eur(pvp.min())    if len(pvp)   else "—",
            "Precio máx. (€)":    eur(pvp.max())    if len(pvp)   else "—",
            "Cuota media (€/mes)":eu_mes(cuota.mean()) if len(cuota) else "—",
            "Cuota mín. (€/mes)": eu_mes(cuota.min())  if len(cuota) else "—",
            "Cuota máx. (€/mes)": eu_mes(cuota.max())  if len(cuota) else "—",
            "Entrada media (€)":  eur(entrada.mean()) if len(entrada) else "—",
            "TIN medio (%)":      pct_val(tin.mean(), 2) if len(tin) else "—",
            "TAE media (%)":      f"{tae.mean():.2f}%".replace(".", ",") if len(tae) else "—",
            "Plazo medio (meses)":eu_num(plazo.mean()) if len(plazo) else "—",
            "Combustible frec.":  top_fuel,
            "Dealer principal":   top_dealer,
        })

    comp = pd.DataFrame(rows).set_index("Modelo")
    model_brand_h = model_brand_map(df)
    th_html = ['<th></th>']
    for m in comp.index:
        b64 = _BRAND_LOGOS.get(model_brand_h.get(m))
        logo_html = f'<img class="rank-logo" src="data:image/png;base64,{b64}" />' if b64 else ""
        th_html.append(f'<th>{logo_html}<span>{m}</span></th>')
    rows_html = []
    for idx_name, row_vals in comp.T.iterrows():
        tds = "".join(f"<td>{v}</td>" for v in row_vals.astype(str))
        rows_html.append(f"<tr><td class='comp-row-label'>{idx_name}</td>{tds}</tr>")
    st.markdown(
        '<div class="chart-card comp-table-wrap"><table class="comp-table">'
        f'<thead><tr>{"".join(th_html)}</tr></thead>'
        f'<tbody>{"".join(rows_html)}</tbody>'
        '</table></div>',
        unsafe_allow_html=True,
    )

    raw = []
    for m in sel:
        sub = df[df["Modelo_norm"] == m]
        raw.append({
            "Modelo": m,
            "Precio medio": sub["PVP"].mean()      if "PVP"      in sub.columns else np.nan,
            "Cuota media":  sub["Cuota_mes"].mean() if "Cuota_mes" in sub.columns else np.nan,
        })
    raw_df = pd.DataFrame(raw)

    model_brand = model_brand_map(df)
    c1, c2 = st.columns(2)
    with c1:
        d = raw_df.dropna(subset=["Precio medio"])
        render_ranking(
            "Precio medio por modelo",
            list(zip(d["Modelo"], d["Precio medio"])),
            fmt=lambda v: eur(v),
            row_brands=[model_brand.get(m) for m in d["Modelo"]],
            show_logos=True,
        )

    with c2:
        d2 = raw_df.dropna(subset=["Cuota media"])
        render_ranking(
            "Cuota mensual media por modelo",
            list(zip(d2["Modelo"], d2["Cuota media"])),
            fmt=lambda v: eu_mes(v),
            row_brands=[model_brand.get(m) for m in d2["Modelo"]],
            show_logos=True,
        )

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
            f'{m_min} tiene el precio medio más bajo ({eur(p_min)}). '
            f'{m_max} es el más caro ({eur(p_max)}). '
            f'Diferencia: <strong>{eur(diff)}</strong> ({pct_val(pct_v)}).'
            f'</div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────
# TABLA DE VEHÍCULOS
# ─────────────────────────────────────────────────────────────
def tabla_vehiculos(df):
    df = df.reset_index(drop=True)
    search = st.text_input("Buscar:", "", key="tabla_search",
                           placeholder="Modelo, concesionario, ciudad...")

    col_map = {
        "Marca": "Marca",
        "Modelo_norm": "Modelo",
        "Versión": "Versión",
        "Año": "Año",
        "Fecha Publicacion": "Fecha Publicacion",
        "Fuel_type": "Combustible",
        "Carrocería": "Carrocería",
        "Segment": "Segmento",
        "High_Performance": "High Performance",
        "PVP": "Precio (€)",
        "Cuota_mes": "Cuota/mes (€)",
        "Entrada": "Entrada (€)",
        "Cuota_final": "Cuota Final (€)",
        "TIN": "TIN (%)",
        "TAE": "TAE (%)",
        "Plazo": "Plazo (meses)",
        "Concesionario": "Concesionario",
        "Ciudad": "Ciudad",
        "Provincia": "Provincia",
        "Mercado": "Mercado",
        "Estado": "Estado",
        "URL": "URL",
    }
    display_cols = [c for c in col_map if c in df.columns]
    df_show = df[display_cols].rename(columns=col_map).reset_index(drop=True)

    if "Precio (€)" in df_show.columns:
        df_show["Precio (€)"] = df["PVP"].map(lambda x: eur(x) if pd.notna(x) else "")
    if "Cuota/mes (€)" in df_show.columns:
        df_show["Cuota/mes (€)"] = df["Cuota_mes"].map(lambda x: eu_mes(x) if pd.notna(x) else "")
    if "Entrada (€)" in df_show.columns:
        df_show["Entrada (€)"] = df["Entrada"].map(lambda x: eur(x) if pd.notna(x) else "")
    if "Cuota Final (€)" in df_show.columns:
        df_show["Cuota Final (€)"] = df["Cuota_final"].map(lambda x: eur(x) if pd.notna(x) else "")
    if "TIN (%)" in df_show.columns:
        df_show["TIN (%)"] = df["TIN"].map(lambda x: pct_val(x, 2) if pd.notna(x) else "")
    if "TAE (%)" in df_show.columns:
        df_show["TAE (%)"] = df["TAE"].map(lambda x: pct_val(x, 2) if pd.notna(x) else "")
    if "Plazo (meses)" in df_show.columns:
        df_show["Plazo (meses)"] = df["Plazo"].map(lambda x: str(int(x)) if pd.notna(x) else "")
    if "Año" in df_show.columns:
        df_show["Año"] = df["Año"].map(lambda x: str(int(x)) if pd.notna(x) else "")
    if "Fecha Publicacion" in df_show.columns:
        df_show["Fecha Publicacion"] = df["Fecha Publicacion"].map(fmt_date)

    if search:
        mask = df_show.apply(
            lambda col: col.astype(str).str.contains(search, case=False, na=False)
        ).any(axis=1)
        df_show = df_show[mask]

    st.caption(f"{eu_num(len(df_show))} vehículos")

    col_config = {}
    if "URL" in df_show.columns:
        col_config["URL"] = st.column_config.LinkColumn("URL", display_text="Ver anuncio")

    st.dataframe(
        df_show,
        width="stretch",
        height=520,
        hide_index=True,
        column_config=col_config,
    )

    # Exportar con formato europeo para lectura en Excel/Sheets.
    st.markdown("<br>", unsafe_allow_html=True)
    df_export = df[display_cols].copy()
    for c in ["PVP", "Entrada", "Cuota_final"]:
        if c in df_export.columns:
            df_export[c] = df_export[c].map(eur)
    if "Cuota_mes" in df_export.columns:
        df_export["Cuota_mes"] = df_export["Cuota_mes"].map(eu_mes)
    for c in ["TAE", "TIN"]:
        if c in df_export.columns:
            df_export[c] = df_export[c].map(lambda x: pct_val(x, 2))
    if "Año" in df_export.columns:
        df_export["Año"] = df_export["Año"].map(lambda x: eu_num(x, 0) if pd.notna(x) else "—")
    if "Fecha Publicacion" in df_export.columns:
        df_export["Fecha Publicacion"] = df_export["Fecha Publicacion"].map(fmt_date)
    csv = df_export.to_csv(index=False, sep=";").encode("utf-8-sig")
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
        f'con {eu_num(top_marca.max())} vehículos ({pct(top_marca.max(), total)} del total).'
    )

    top_mod = df["Modelo_norm"].value_counts()
    items.append(
        f'<span class="insight-tag">MODELO</span>'
        f'El modelo con mayor stock es <strong>{top_mod.idxmax()}</strong> '
        f'con {eu_num(top_mod.max())} unidades.'
    )

    if not pvp_s.empty:
        grp_pvp = df[df["PVP"].notna()].groupby("Modelo_norm")["PVP"].mean()
        items.append(
            f'<span class="insight-tag">PRECIO</span>'
            f'Precio medio general: <strong>{eur(pvp_s.mean())}</strong>. '
            f'Modelo más caro en media: <strong>{grp_pvp.idxmax()}</strong> ({eur(grp_pvp.max())}). '
            f'Modelo más económico: <strong>{grp_pvp.idxmin()}</strong> ({eur(grp_pvp.min())}).'
        )
        items.append(
            f'<span class="insight-tag">PRECIO</span>'
            f'El {pct(len(pvp_s), total)} del stock tiene precio informado '
            f'({eu_num(len(pvp_s))} de {eu_num(total)} vehículos).'
        )

    if not cuota_s.empty:
        grp_cuota = df[df["Cuota_mes"].notna()].groupby("Modelo_norm")["Cuota_mes"].mean()
        marca_cuota = df[df["Cuota_mes"].notna()].groupby("Marca")["Cuota_mes"].mean()
        items.append(
            f'<span class="insight-tag">CUOTA</span>'
            f'Cuota media: <strong>{eu_mes(cuota_s.mean())}</strong>. '
            f'La cuota media más baja por modelo corresponde a <strong>{grp_cuota.idxmin()}</strong> '
            f'({eu_mes(grp_cuota.min())}). '
            f'La marca con cuota media más baja es <strong>{marca_cuota.idxmin()}</strong> '
            f'({eu_mes(marca_cuota.min())}).'
        )
        items.append(
            f'<span class="insight-tag">CUOTA</span>'
            f'El {pct(len(cuota_s), total)} del stock tiene cuota mensual informada '
            f'({eu_num(len(cuota_s))} de {eu_num(total)} vehículos).'
        )

    if "Ciudad" in df.columns and df["Ciudad"].notna().any():
        top_c = df["Ciudad"].value_counts()
        items.append(
            f'<span class="insight-tag">GEOGRAFIA</span>'
            f'La ciudad con mayor concentración de stock es <strong>{top_c.idxmax()}</strong> '
            f'({eu_num(top_c.max())} vehículos).'
        )

    if "Provincia" in df.columns and df["Provincia"].notna().any():
        top_p = df["Provincia"].value_counts()
        items.append(
            f'<span class="insight-tag">GEOGRAFIA</span>'
            f'Provincia con más stock: <strong>{top_p.idxmax()}</strong> ({eu_num(top_p.max())} uds.).'
        )

    top_d = df["Concesionario"].value_counts()
    items.append(
        f'<span class="insight-tag">DEALER</span>'
        f'El concesionario con mayor volumen de vehículos anunciados es '
        f'<strong>{top_d.idxmax()}</strong> con {eu_num(top_d.max())} unidades.'
    )

    top_fuel = df["Fuel_type"].value_counts()
    items.append(
        f'<span class="insight-tag">COMBUSTIBLE</span>'
        f'El tipo de propulsión más frecuente en el stock es <strong>{top_fuel.idxmax()}</strong> '
        f'({eu_num(top_fuel.max())} uds., {pct(top_fuel.max(), total)}).'
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
        marcas_str = " | ".join([f"{m}: {eu_num(n)}" for m, n in df["Marca"].value_counts().items()])
        return (
            f"**Resumen del stock actual ({eu_num(total)} vehículos)**\n\n"
            f"- Por marca: {marcas_str}\n"
            f"- Con precio informado: {eu_num(len(pvp_s))} ({pct(len(pvp_s), total)})\n"
            f"- Con cuota mensual: {eu_num(len(cuota_s))} ({pct(len(cuota_s), total)})\n"
            f"- Precio medio: {eur(pvp_s.mean())}\n"
            f"- Cuota mensual media: {eu_mes(cuota_s.mean())}" if len(cuota_s) else ""
        )

    # Marca con más stock
    if re.search(r"marca.*más.*stock|mayor.*stock.*marca|qué.*marca.*más", q_l):
        top = df["Marca"].value_counts()
        lines = "\n".join([f"- {m}: {eu_num(n)}" for m, n in top.items()])
        return f"**Stock por marca:**\n\n{lines}\n\nLíder: **{top.idxmax()}** con {eu_num(top.max())} unidades."

    # Precio más bajo / económico
    if re.search(r"precio.*bajo|más.*económico|más barato|menor.*precio|precio.*mínimo", q_l):
        if pvp_s.empty:
            return "No hay datos de precio con los filtros actuales."
        grp = df[df["PVP"].notna()].groupby("Modelo_norm")["PVP"].mean().sort_values().head(5)
        lines = "\n".join([f"- **{m}:** {eur(v)}" for m, v in grp.items()])
        return f"**Modelos con precio medio más bajo:**\n\n{lines}"

    # Precio más alto / caro
    if re.search(r"precio.*alto|más.*caro|mayor.*precio|precio.*máximo", q_l):
        if pvp_s.empty:
            return "No hay datos de precio disponibles."
        grp = df[df["PVP"].notna()].groupby("Modelo_norm")["PVP"].mean().sort_values(ascending=False).head(5)
        lines = "\n".join([f"- **{m}:** {eur(v)}" for m, v in grp.items()])
        return f"**Modelos con precio medio más alto:**\n\n{lines}"

    # Cuota inferior a X
    if re.search(r"cuota.*inferior|cuota.*menos|cuota.*por debajo|menor.*cuota|cuota.*mínima|cuota.*baja", q_l):
        nums = re.findall(r'\d+', q_l)
        if nums and "inferior" in q_l or "menos" in q_l or "por debajo" in q_l:
            limit = int(nums[0])
            sub = df[df["Cuota_mes"].notna() & (df["Cuota_mes"] <= limit)]
            if sub.empty:
                return f"No hay vehículos con cuota ≤ {eu_mes(limit)} con los filtros actuales."
            grp = sub.groupby(["Marca","Modelo_norm"])["Cuota_mes"].agg(["count","mean"]).reset_index().sort_values("mean")
            lines = "\n".join([
                f"- **{r['Modelo_norm']}** ({r['Marca']}): {eu_mes(r['mean'])} — {eu_num(int(r['count']))} uds."
                for _, r in grp.head(10).iterrows()
            ])
            return f"**{eu_num(len(sub))} vehículos con cuota ≤ {eu_mes(limit)}:**\n\n{lines}"
        if cuota_s.empty:
            return "No hay datos de cuota mensual disponibles."
        grp = df[df["Cuota_mes"].notna()].groupby("Modelo_norm")["Cuota_mes"].mean().sort_values().head(5)
        lines = "\n".join([f"- **{m}:** {eu_mes(v)}" for m, v in grp.items()])
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
                pvp_str   = eur(p.mean())   if len(p) else "sin precio"
                cuota_str = eu_mes(c.mean()) if len(c) else "sin cuota"
                resp += f"- **{m}** — {eu_num(len(sub))} uds. | Precio: {pvp_str} | Cuota: {cuota_str}\n"
            if len(encontrados) == 2:
                p0 = df[df["Modelo_norm"]==encontrados[0]]["PVP"].dropna()
                p1 = df[df["Modelo_norm"]==encontrados[1]]["PVP"].dropna()
                if len(p0) and len(p1):
                    diff = abs(p0.mean()-p1.mean())
                    pct_v = diff/min(p0.mean(),p1.mean())*100
                    mas_caro = encontrados[0] if p0.mean() > p1.mean() else encontrados[1]
                    resp += f"\nDiferencia de precio: **{eur(diff)}** ({pct_val(pct_v)}). El más caro: **{mas_caro}**."
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
            lines = "\n".join([f"- **{m}:** {eu_num(n)} uds." for m, n in top_m.items()])
            return f"**{eu_num(len(sub2))} eléctricos con precio ≤ {eur(limit)}:**\n\n{lines}"
        top_m = sub["Modelo_norm"].value_counts().head(8)
        lines = "\n".join([f"- **{m}:** {eu_num(n)}" for m, n in top_m.items()])
        return f"**{eu_num(len(sub))} vehículos eléctricos (BEV) en el stock:**\n\n{lines}"

    # Dealers
    if re.search(r"dealer|concesionario|distribuid", q_l):
        top = df["Concesionario"].value_counts().head(8)
        lines = "\n".join([f"- **{d}:** {eu_num(n)} uds." for d, n in top.items()])
        return f"**Top 8 concesionarios por stock:**\n\n{lines}"

    # Provincia / ciudad
    if re.search(r"provincia|ciudad|ubicación|zona|región|donde|dónde", q_l):
        if "Provincia" in df.columns and df["Provincia"].notna().any():
            top = df["Provincia"].value_counts().head(8)
            lines = "\n".join([f"- **{p}:** {eu_num(n)}" for p, n in top.items()])
            return f"**Stock por provincia (top 8):**\n\n{lines}"
        if "Ciudad" in df.columns and df["Ciudad"].notna().any():
            top = df["Ciudad"].value_counts().head(8)
            lines = "\n".join([f"- **{c}:** {eu_num(n)}" for c, n in top.items()])
            return f"**Stock por ciudad (top 8):**\n\n{lines}"

    # Búsqueda de modelo específico
    for modelo in sorted(df["Modelo_norm"].dropna().unique(), key=len, reverse=True):
        if len(modelo) > 3 and modelo.lower() in q_l:
            sub = df[df["Modelo_norm"] == modelo]
            p = sub["PVP"].dropna()      if "PVP"      in sub.columns else pd.Series()
            c = sub["Cuota_mes"].dropna() if "Cuota_mes" in sub.columns else pd.Series()
            resp = f"**{modelo}** — {eu_num(len(sub))} vehículos\n\n"
            if len(p):
                resp += f"- Precio medio: **{eur(p.mean())}** (mín {eur(p.min())} · máx {eur(p.max())})\n"
                resp += f"- Con precio informado: {eu_num(len(p))} de {eu_num(len(sub))}\n"
            if len(c):
                resp += f"- Cuota media: **{eu_mes(c.mean())}** (mín {eu_mes(c.min())} · máx {eu_mes(c.max())})\n"
                resp += f"- Con cuota informada: {eu_num(len(c))} de {eu_num(len(sub))}\n"
            top_d = sub["Concesionario"].value_counts().head(3)
            resp += "\nPrincipales dealers: " + ", ".join([f"{d} ({eu_num(n)})" for d, n in top_d.items()])
            return resp

    # Precio y cuota a la vez
    if re.search(r"precio.*cuota|cuota.*precio|ambos|los dos datos", q_l):
        sub = df[df["PVP"].notna() & df["Cuota_mes"].notna()] if all(c in df.columns for c in ["PVP","Cuota_mes"]) else pd.DataFrame()
        if sub.empty:
            return "No hay vehículos con precio total y cuota mensual a la vez con los filtros actuales."
        top = sub.groupby("Modelo_norm").size().sort_values(ascending=False).head(8)
        lines = "\n".join([f"- **{m}:** {eu_num(n)}" for m, n in top.items()])
        return f"**{eu_num(len(sub))} vehículos con precio total Y cuota mensual disponibles:**\n\n{lines}"

    # Sin match
    return (
        "No he encontrado una respuesta directa. Ejemplos de preguntas:\n\n"
        "- *¿Cuál es el precio medio del BMW Serie 1?*\n"
        "- *Compara BMW Serie 3 con Audi A4*\n"
        "- *¿Qué concesionario tiene más coches?*\n"
        "- *Eléctricos con precio inferior a 50000 euros*\n"
        "- *Dame un resumen del stock actual*"
    )

def _secret(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""

def _llm_provider():
    providers = [
        ("groq", "GROQ_API_KEY", os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")),
        ("gemini", "GOOGLE_API_KEY", os.getenv("GEMINI_MODEL", "gemini-1.5-flash")),
        ("anthropic", "ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")),
        ("openai", "OPENAI_API_KEY", os.getenv("OPENAI_MODEL", "gpt-4o-mini")),
    ]
    for provider, key_name, model in providers:
        key = _secret(key_name)
        if key:
            return {"provider": provider, "key": key, "model": model}
    return None

def _chat_context(df: pd.DataFrame) -> str:
    context_cols = [c for c in [
        "Marca", "Mercado", "Modelo_norm", "Versión", "Año", "Fecha Publicacion",
        "Fuel_type", "Carrocería", "Segment", "High_Performance", "PVP", "Cuota_mes", "TAE",
        "Concesionario", "Ciudad", "Provincia", "URL",
    ] if c in df.columns]
    slim = df[context_cols].copy()
    numeric = {}
    for col in ["PVP", "Cuota_mes", "TAE", "Año"]:
        if col in slim.columns:
            s = pd.to_numeric(slim[col], errors="coerce").dropna()
            if not s.empty:
                numeric[col] = {
                    "count": int(s.count()),
                    "mean": round(float(s.mean()), 2),
                    "min": round(float(s.min()), 2),
                    "max": round(float(s.max()), 2),
                }
    top_values = {}
    for col in ["Marca", "Modelo_norm", "Versión", "Fuel_type", "Carrocería", "Segment", "High_Performance", "Concesionario", "Ciudad", "Provincia"]:
        if col in slim.columns and slim[col].notna().any():
            top_values[col] = slim[col].astype(str).value_counts().head(12).to_dict()
    sample = slim.head(10).fillna("").to_dict(orient="records")
    payload = {
        "filas_filtradas": int(len(df)),
        "columnas_disponibles": context_cols,
        "estadisticas_numericas": numeric,
        "top_valores": top_values,
        "muestra_10_filas": sample,
    }
    return json.dumps(payload, ensure_ascii=False, default=str)

_ALLOWED_PANDAS_ATTRS = {
    "agg", "all", "any", "astype", "between", "columns", "copy", "count", "describe",
    "drop_duplicates", "dropna", "dt", "fillna", "groupby", "head", "idxmax", "idxmin",
    "iloc", "index", "isin", "isna", "notna", "loc", "max", "mean", "median", "min",
    "mode", "nlargest", "nsmallest", "nunique", "reset_index", "round",
    "shape", "size", "sort_index", "sort_values", "str", "sum", "tail", "to_dict",
    "to_datetime", "to_frame", "to_list", "to_string", "unique", "value_counts", "values",
    "contains", "endswith", "lower", "replace", "startswith", "strip", "upper",
}
_ALLOWED_CALL_NAMES = {"len", "int", "float", "str", "round"}

def _validate_pandas_expr(expr: str):
    if len(expr) > 1200 or "\n" in expr or ";" in expr:
        raise ValueError("La expresión debe ser de una sola línea.")
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Expression, ast.Load, ast.Constant, ast.Name, ast.Attribute,
                             ast.Subscript, ast.Slice, ast.Tuple, ast.List, ast.Dict, ast.Set,
                             ast.Call, ast.keyword, ast.Compare, ast.BoolOp, ast.BinOp, ast.UnaryOp,
                             ast.And, ast.Or, ast.Not, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt,
                             ast.GtE, ast.In, ast.NotIn, ast.Is, ast.IsNot, ast.Add, ast.Sub,
                             ast.Mult, ast.Div, ast.Mod, ast.BitAnd, ast.BitOr, ast.Invert,
                             ast.USub, ast.UAdd)):
            continue
        raise ValueError(f"Operación no permitida: {type(node).__name__}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in {"df", "pd", "np", "True", "False", "None", *_ALLOWED_CALL_NAMES}:
            raise ValueError(f"Nombre no permitido: {node.id}")
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_") or node.attr not in _ALLOWED_PANDAS_ATTRS:
                raise ValueError(f"Atributo no permitido: {node.attr}")
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id not in _ALLOWED_CALL_NAMES:
                raise ValueError(f"Función no permitida: {func.id}")
            if isinstance(func, ast.Attribute) and func.attr not in _ALLOWED_PANDAS_ATTRS:
                raise ValueError(f"Método no permitido: {func.attr}")
    return tree

def _safe_pandas_eval(expr: str, df: pd.DataFrame):
    tree = _validate_pandas_expr(expr)
    safe_df = df.copy()
    return eval(compile(tree, "<llm-pandas>", "eval"), {"__builtins__": {}}, {
        "df": safe_df,
        "pd": pd,
        "np": np,
        "len": len,
        "int": int,
        "float": float,
        "str": str,
        "round": round,
    })

def _format_calc_result(result) -> str:
    if isinstance(result, pd.DataFrame):
        if result.empty:
            return "DataFrame vacío."
        return result.head(30).to_string(index=False)
    if isinstance(result, pd.Series):
        if result.empty:
            return "Serie vacía."
        return result.head(30).to_string()
    if isinstance(result, (dict, list, tuple, set)):
        return json.dumps(result, ensure_ascii=False, default=str, indent=2)
    return str(result)

def _llm_http_call(provider_cfg, messages, system_prompt=None, temperature=0.1, max_tokens=900):
    provider = provider_cfg["provider"]
    key = provider_cfg["key"]
    model = provider_cfg["model"]
    timeout = 35

    if provider in {"groq", "openai"}:
        base_url = "https://api.groq.com/openai/v1" if provider == "groq" else "https://api.openai.com/v1"
        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        payload_messages.extend(messages)
        r = requests.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": payload_messages, "temperature": temperature, "max_tokens": max_tokens},
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    if provider == "gemini":
        prompt = ""
        if system_prompt:
            prompt += system_prompt + "\n\n"
        prompt += "\n\n".join(m["content"] for m in messages)
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
            },
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

    if provider == "anthropic":
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
            json={"model": model, "system": system_prompt or "", "messages": messages, "temperature": temperature, "max_tokens": max_tokens},
            timeout=timeout,
        )
        r.raise_for_status()
        return "".join(block.get("text", "") for block in r.json().get("content", []))

    raise ValueError("Proveedor LLM no soportado.")

def _extract_llm_json(text: str) -> dict:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?|```$", "", cleaned, flags=re.I | re.M).strip()
    try:
        return json.loads(cleaned)
    except Exception:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start >= 0 and end > start:
            return json.loads(cleaned[start:end + 1])
    return {"answer": cleaned, "pandas": None}

def _llm_responder(q: str, df: pd.DataFrame) -> str:
    provider_cfg = _llm_provider()
    if not provider_cfg:
        return _responder(q, df)

    system_prompt = (
        "Eres un analista senior de stock de vehículos BMW, Audi y Mercedes. "
        "Responde siempre en español. Usa solo los datos proporcionados y no inventes cifras. "
        "Si necesitas un cálculo exacto, devuelve una expresión pandas de solo lectura sobre el DataFrame df. "
        "Devuelve siempre JSON válido con estas claves: answer y pandas. "
        "pandas debe ser null o una expresión de una sola línea, sin imports, sin asignaciones, sin escribir archivos. "
        "Usa nombres de columnas exactamente como aparecen."
    )
    user_prompt = (
        "Contexto del dataframe filtrado activo:\n"
        f"{_chat_context(df)}\n\n"
        "Pregunta del usuario:\n"
        f"{q}\n\n"
        "Formato obligatorio:\n"
        '{"answer":"respuesta breve o explicación de qué vas a calcular","pandas":null}'
    )

    try:
        raw = _llm_http_call(provider_cfg, [{"role": "user", "content": user_prompt}], system_prompt=system_prompt)
        plan = _extract_llm_json(raw)
        answer = str(plan.get("answer") or "").strip()
        expr = plan.get("pandas")
        if not expr:
            return answer or raw

        result = _safe_pandas_eval(str(expr), df)
        result_text = _format_calc_result(result)
        final_prompt = (
            "Pregunta original:\n"
            f"{q}\n\n"
            "Resultado calculado con pandas sobre el dataframe real filtrado:\n"
            f"{result_text}\n\n"
            "Redacta una respuesta final breve en español. No añadas datos que no estén en el resultado."
        )
        final_system = (
            "Eres un analista senior de stock de vehículos. "
            "Responde en español, de forma directa, usando solo el resultado calculado. "
            "No devuelvas JSON ni código."
        )
        try:
            return _llm_http_call(provider_cfg, [{"role": "user", "content": final_prompt}], system_prompt=final_system, max_tokens=700)
        except Exception:
            return f"{answer}\n\n**Resultado calculado:**\n\n{result_text}"
    except Exception as exc:
        fallback = _responder(q, df)
        return f"{fallback}\n\n_Nota: el LLM no ha respondido correctamente ({type(exc).__name__}). He usado el asistente local._"

def _chat_text_to_html(text: str) -> str:
    safe = html.escape(str(text))
    safe = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", safe)
    safe = safe.replace("\n", "<br>")
    return safe


def show_chatbot(df):
    if "chat_msgs" not in st.session_state:
        st.session_state.chat_msgs = [
            {"role": "bot", "text":
             f"Stock cargado: **{eu_num(len(df))} vehículos**. "
             "Puedes preguntarme sobre precios, cuotas, modelos, concesionarios o cualquier dato del dataset."}
        ]

    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_msgs:
        if msg["role"] == "user":
            chat_html += f'<div class="msg-user"><span>{_chat_text_to_html(msg["text"])}</span></div>'
        else:
            chat_html += f'<div class="msg-bot"><span>{_chat_text_to_html(msg["text"])}</span></div>'
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
        resp = _llm_responder(user_input, df)
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
        if col.button(sug,key=f"sug_{sug[:12]}", width="stretch"):
            st.session_state.chat_msgs.append({"role": "user", "text": sug})
            resp = _llm_responder(sug, df)
            st.session_state.chat_msgs.append({"role": "bot", "text": resp})
            st.rerun()

    if st.button("Limpiar conversacion"):
        st.session_state.chat_msgs = []
        st.rerun()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    csv_path = BASE / "STOCK_UNIFICADO_GLOBAL.csv"
    updated = (
        datetime.fromtimestamp(csv_path.stat().st_mtime).strftime("%d/%m/%Y %H:%M")
        if csv_path.exists() else "—"
    )
    show_header(updated)
    with st.spinner("Cargando datos del stock..."):
        df_raw = load_data()

    st.markdown(
        f'<div class="status-bar"><span class="status-dot"></span>'
        f'<span>SISTEMA EN VIVO</span><span class="sep">·</span>'
        f'<span>Datos actualizados: <span class="mono">{updated}</span></span>'
        f'<span class="sep">·</span>'
        f'<span><span class="mono">{eu_num(len(df_raw))}</span> vehículos en base</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

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


if __name__ == "__main__":
    main()
