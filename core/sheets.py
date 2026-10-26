"""Acceso a Google Sheets: lectura cacheada y escrituras acotadas."""
from datetime import date, datetime

import gspread
import pandas as pd
import streamlit as st

from core.config import CACHE_TTL, HISTORIAL_HEADERS, HOJAS, INS_COL, SHEET_ID


@st.cache_resource
def _libro() -> gspread.Spreadsheet:
    gc = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
    return gc.open_by_key(SHEET_ID)


def _ws(clave: str) -> gspread.Worksheet:
    return _libro().worksheet(HOJAS[clave])


@st.cache_data(ttl=CACHE_TTL, show_spinner="Leyendo Google Sheets…")
def leer(clave: str) -> pd.DataFrame:
    """Hoja → DataFrame. Números sin formato, fechas como texto.
    Descarta columnas sin encabezado (p. ej. G:I de Inspecciones).
    Agrega `_fila` = número de fila en la hoja (para escribir después)."""
    try:
        valores = _ws(clave).get_all_values(
            value_render_option="UNFORMATTED_VALUE",
            date_time_render_option="FORMATTED_STRING",
        )
    except gspread.WorksheetNotFound:
        return pd.DataFrame()
    if not valores:
        return pd.DataFrame()

    headers = [str(h).strip() for h in valores[0]]
    keep = [i for i, h in enumerate(headers) if h]
    filas = [[r[i] if i < len(r) else "" for i in keep] for r in valores[1:]]
    df = pd.DataFrame(filas, columns=[headers[i] for i in keep])
    df["_fila"] = range(2, len(df) + 2)
    # quitar filas totalmente vacías
    datos = df.drop(columns="_fila").astype(str).apply(lambda s: s.str.strip())
    return df[(datos != "").any(axis=1)].reset_index(drop=True)


def leer_todo() -> dict[str, pd.DataFrame]:
    return {k: leer(k) for k in HOJAS}


def limpiar_cache() -> None:
    leer.clear()


# ── Escrituras ──────────────────────────────────────────────

def actualizar_inspeccion(fila: int, fecha: date, km: int) -> None:
    """Escribe solo B:D de una fila: fecha, km y Notificado vacío."""
    c0, c1 = INS_COL["fecha"], INS_COL["notificado"]
    rango = f"{gspread.utils.rowcol_to_a1(fila, c0)}:{gspread.utils.rowcol_to_a1(fila, c1)}"
    _ws("inspecciones").update(
        [[fecha.strftime("%d/%m/%Y"), int(km), ""]],
        rango,
        value_input_option="USER_ENTERED",
    )


def agregar_historial(placa: str, fecha: date, km: int, km_prev: int,
                      obs: str, usuario: str) -> None:
    libro = _libro()
    try:
        ws = libro.worksheet(HOJAS["historial"])
    except gspread.WorksheetNotFound:
        ws = libro.add_worksheet(HOJAS["historial"], rows=1000, cols=len(HISTORIAL_HEADERS))
        ws.append_row(HISTORIAL_HEADERS)
        ws.freeze(rows=1)
    ws.append_row(
        [datetime.now().strftime("%d/%m/%Y %H:%M:%S"), placa, fecha.strftime("%d/%m/%Y"),
         int(km), int(km_prev), int(km) - int(km_prev), obs, usuario],
        value_input_option="USER_ENTERED",
    )
