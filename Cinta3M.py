# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO PROFESIONAL
# =================================================================
st.set_page_config(page_title="VHB Structural Lab | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .main > div { padding-left: 2.5rem; padding-right: 2.5rem; }
    .stMetric { background-color: #fcfcfc; padding: 20px; border-radius: 10px; border: 1px solid #eee; }
    .result-box { 
        background-color: #fffafa; 
        padding: 25px; 
        border: 1px solid #ffcccc;
        border-left: 10px solid #cc0000; 
        border-radius: 8px; 
    }
    .status-tag {
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 VHB™ Structural Design Lab")
st.markdown("#### **Verificación de Tracción y Cizalladura según Estándares 3M**")
st.divider()

# =================================================================
# 2. SIDEBAR: PARÁMETROS DE CARGA
# =================================================================
st.sidebar.header("📋 Especificaciones del Proyecto")

with st.sidebar.expander("📐 Geometría del Panel", expanded=True):
    ancho_p = st.number_input("Ancho del Panel (m)", value=1.20, step=0.05)
    alto_p = st.number_input("Alto del Panel (m)", value=2.40, step=0.05)
    t_vidrio = st.number_input("Espesor del Vidrio (mm)", value=6.0, step=1.0)
    lado_menor = min(ancho_p, alto_p)

with st.sidebar.expander("🌪️ Cargas Dinámicas (Viento)", expanded=True):
    p_viento = st.number_input("Presión de Viento (kgf/m²)", value=150.0)
    # Admisible dinámico 3M: 8,435 kgf/m2 (12 psi)
    adm_dinamico = 8435 

with st.sidebar.expander("⚖️ Cargas Estáticas (Peso)", expanded=True):
    # Admisible estático 3M: 173.5 kgf/m2 (0.25 psi)
    # Equivalencia: 60 cm2 por cada kg de peso
    adm_estatico = 173.5
    usa_calzos = st.checkbox("¿Usa calzos de apoyo?", value=True, help="Si usa calzos, la cinta no toma carga de cizalle permanente.")

# =================================================================
# 3. MOTOR DE CÁLCULO DUAL
# =================================================================

# A. Cálculo de Masa
peso_panel = (ancho_p * alto_p * (t_vidrio/1000)) * 2500

# B. Cálculo de Ancho por Viento (Dinámico)
ancho_viento_mm = (p_viento * lado_menor) / (2 * adm_dinamico) * 1000

# C. Cálculo de Ancho por Peso (Estático / Cizalle)
if not usa_calzos:
    perimetro_m = 2 * (ancho_p + alto_p)
    # Área requerida = Peso / Adm_estatico. Ancho = Área / Perímetro
    ancho_peso_mm = (peso_panel / (perimetro_m * adm_estatico)) * 1000
else:
    ancho_peso_mm = 0.0

# D. Selección del Crítico y Redondeo (3M sugiere múltiplo de 5 superior)
ancho_calculado = max(ancho_viento_mm, ancho_peso_mm, 15.0)
ancho_final = math.ceil(ancho_calculado / 5) * 5

# =================================================================
# 4. DASHBOARD DE RESULTADOS
# =================================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Peso del Panel", f"{peso_panel:.2f} kgf")
with c2:
    st.metric("Ancho Requerido (Viento)", f"{ancho_viento_mm:.2f} mm")
with c3:
    st.metric("Ancho Requerido (Peso)", f"{ancho_peso_mm:.2f} mm" if not usa_calzos else "0.00 mm (Calzos)")

st.markdown("### 🔍 Análisis de Capacidad de Cizalladura")

col_info, col_res = st.columns([1.2, 1])

with col_info:
    st.info(f"""
    **Criterios de Validación 3M:**
    * **Dinámico:** La cinta soporta cizalladura por viento con un límite de **{adm_dinamico} kgf/m²**.
    * **Estático:** Sin calzos, se requiere **60 cm² de cinta por cada 1 kg de carga muerta**.
    * **Geometría:** El diseño utiliza la teoría de áreas tributarias trapezoidales.
    """)
    if not usa_calzos:
        st.warning("⚠️ **ALERTA:** Al no usar calzos, la cinta asume carga de cizalle permanente. Verifique la preparación de superficie con 3M.")

with col_res:
    st.markdown(f"""
    <div class="result-box">
        <h2 style="margin-top:0; color:#cc0000;">Especificación Final</h2>
        <p style="font-size:1.1em;">Bite Mínimo Sugerido:</p>
        <p style="font-size:3em; font-weight:bold; margin:0;">{ancho_final} mm</p>
        <p style="margin-top:10px;">Gobernado por: <strong>{'Viento (Dinámico)' if ancho_viento_mm > ancho_peso_mm else 'Peso Propio (Estático)'}</strong></p>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 5. GRÁFICO DE ESFUERZOS COMBINADOS
# =================================================================


st.subheader("📈 Mapa de Sensibilidad Estructural")
p_viento_range = np.linspace(50, 450, 50)
w_viento = [(p * lado_menor) / (2 * adm_dinamico) * 1000 for p in p_viento_range]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(p_viento_range, w_viento, color='#cc0000', label='Ancho por Viento (Dinámico)', lw=2)
if not usa_calzos:
    ax.axhline(ancho_peso_mm, color='#333', ls='--', label='Límite Peso Propio (Estático)')

ax.fill_between(p_viento_range, [max(v, ancho_peso_mm, 15) for v in w_viento], color='#cc0000', alpha=0.05)
ax.set_xlabel("Presión de Viento (kgf/m²)")
ax.set_ylabel("Ancho de Cinta (mm)")
ax.legend()
st.pyplot(fig)

# =================================================================
# 6. CIERRE
# =================================================================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <strong>Ingeniero Responsable:</strong> Mauricio Riquelme | Proyectos Estructurales EIRL<br>
        <em>Basado en Boletines Técnicos 3M VHB™ (Marzo 2010 - Septiembre 2009)</em>
    </div>
""", unsafe_allow_html=True)