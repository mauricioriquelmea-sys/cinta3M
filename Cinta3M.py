# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO
# =================================================================
st.set_page_config(page_title="Cálculo VHB FS=5 | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .result-box { background-color: #fff4f4; padding: 25px; border-left: 8px solid #cc0000; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. ENCABEZADO
# =================================================================
st.title("🔴 Diseño de Unión con Cinta 3M™ VHB™")
st.markdown(f"#### **Verificación Dinámica con Factor de Seguridad FS = 5**")
st.divider()

# =================================================================
# 3. SIDEBAR: PARÁMETROS DE DISEÑO
# =================================================================
st.sidebar.header("⚙️ Parámetros de Diseño")

with st.sidebar.expander("📐 Geometría del Panel", expanded=True):
    ancho = st.number_input("Ancho del Panel (m)", value=1.20, step=0.05)
    alto = st.number_input("Alto del Panel (m)", value=2.40, step=0.05)
    lado_menor = min(ancho, alto)

with st.sidebar.expander("🌪️ Carga de Viento y Seguridad", expanded=True):
    p_viento = st.number_input("Presión de Diseño (kgf/m²)", value=150.0)
    fs = st.number_input("Factor de Seguridad (FS)", value=5.0, help="Valor solicitado: 5")
    
    # Capacidad última típica de la cinta VHB (~50 psi)
    capacidad_ultima = 35150 # kgf/m²
    adm_dinamico = capacidad_ultima / fs

st.sidebar.info(f"**Esfuerzo Admisible:** {adm_dinamico:.2f} kgf/m²")

# =================================================================
# 4. MOTOR DE CÁLCULO
# =================================================================

# Cálculo del ancho de cinta necesario (mm)
# Formula: (Presion * Lado Menor) / (2 * Esfuerzo Admisible)
ancho_cinta_mm = (p_viento * lado_menor) / (2 * adm_dinamico / 10000) * 10 
ancho_final = max(math.ceil(ancho_cinta_mm), 15)

# =================================================================
# 5. RESULTADOS
# =================================================================
st.subheader("📊 Resultados de Análisis con FS = 5")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Esfuerzo Adm. (FS=5)", f"{adm_dinamico:.0f} kgf/m²")
with c2:
    st.metric("Ancho Calculado", f"{ancho_cinta_mm:.2f} mm")
with c3:
    st.metric("Especificación Mín.", f"{ancho_final} mm")

[Image of 3M VHB tape application stress distribution on glass panels]

st.markdown(f"""
<div class="result-box">
    <h3>✅ Especificación Técnica:</h3>
    <p style="font-size: 1.25em;">
        <strong>Ancho de Cinta Requerido:</strong> {ancho_final} mm
    </p>
    <hr>
    <strong>Resumen de Seguridad:</strong> 
    <ul>
        <li>Factor de Seguridad Aplicado: <strong>{fs}</strong></li>
        <li>Carga de Viento: {p_viento} kgf/m²</li>
        <li>Se asume transferencia de carga por el lado corto del panel (L={lado_menor}m).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Curva de Diseño: Ancho vs Presión (FS=5)")

p_rango = np.linspace(50, 450, 30)
b_rango = [(p * lado_menor) / (2 * adm_dinamico / 10000) * 10 for p in p_rango]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(p_rango, b_rango, color='#cc0000', lw=2.5, label=f'Bite Requerido (FS={fs})')
ax.axhline(15, color='black', ls='--', label='Mínimo Constructivo (15mm)')
ax.fill_between(p_rango, b_rango, 15