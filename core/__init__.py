"""Configuración central: nombres de hojas, columnas y umbrales."""
import streamlit as st

# ID del Google Sheet (se puede sobreescribir en secrets: [app] sheet_id)
try:
    SHEET_ID = st.secrets["app"]["sheet_id"]
except Exception:
    SHEET_ID = "15Dbg1OVj9GxRtZtt92B342w6MweXLElfcq65zbbf6sY"

HOJAS = {
    "checklist": "Checklist Vehicular",
    "control": "Control",
    "inspecciones": "Inspecciones",
    "historial": "Historial_Mantto",
}

# Columnas de Inspecciones (base 1) que la app escribe: B:D
INS_COL = {"placa": 1, "fecha": 2, "km": 3, "notificado": 4, "email": 5, "km_actual": 6}

HISTORIAL_HEADERS = [
    "Registro", "Placa", "Fecha mantto", "Km mantto",
    "Km mantto anterior", "Km recorridos", "Observaciones", "Registrado por",
]

PLACAS = ["BUQ-889", "BUQ-809", "BUZ-884", "BVA-729", "BYF-947", "BYF-870", "BYF-723", "BYG-757"]

# Umbrales
INTERVALO_KM = 5000       # mantenimiento cada 5000 km
AVISO_KM = 4500           # semáforo ámbar desde aquí
MARGEN_KM_ACTUAL = 1000   # km mantto ≤ km actual + margen

CACHE_TTL = 900           # s (15 min) para lecturas
ZONA = "America/Lima"
