"""Paso 1: prueba de conexión. Muestra las 4 hojas leídas desde Google Sheets."""
import streamlit as st

from core.config import HOJAS
from core.sheets import leer_todo, limpiar_cache

st.set_page_config(page_title="Flota Chaglla", page_icon="🚙", layout="wide")
st.title("Flota Chaglla · prueba de conexión")

usuario = getattr(st.user, "email", None) or "anónimo"
st.caption(f"Usuario: {usuario}")

if st.button("Recargar datos"):
    limpiar_cache()

datos = leer_todo()
for clave, df in datos.items():
    with st.expander(f"{HOJAS[clave]} · {len(df)} filas", expanded=clave == "inspecciones"):
        if df.empty:
            st.warning("Hoja vacía o no existe todavía.")
        else:
            st.dataframe(df.tail(20), use_container_width=True)
