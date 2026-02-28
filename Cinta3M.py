# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO
# =================================================================
st.set_page_config(page_title="Cálculo VHB | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .main > div { padding-left: 2.5rem; padding-right: 2.5rem; max-width: 100%; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .result-box { background-color: #fff4f4; padding: 25px; border-left: 8px solid #cc0000; border-radius: 8px; margin: 20px 0; }
    .weight-box { background-color: #ffffff; padding: 15px; border: 1px dashed #cc0000; border-radius: 8px; margin-bottom: 20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 Diseño de Unión con Cinta 3M™ VHB™")
st.markdown("#### **Ancho de Cinta (Bondline) según Carga de Viento y Dilatación**")
st.divider()

# =================================================================
# 2. SIDEBAR: PARÁMETROS DE DISEÑO
# =================================================================
st.sidebar.header("⚙️ Parámetros de Diseño")

with st.sidebar.expander("📐 Geometría y Masa", expanded=True):
    ancho_p = st.number_input("Ancho del Panel (m)", value=1.20, step=0.05)
    alto_p = st.number_input("Alto del Panel (m)", value=2.40, step=0.05)
    t_vidrio = st.number_input("Espesor Vidrio (mm)", value=6.0, step=1.0)
    lado_menor = min(ancho_p, alto_p)
    lado_mayor = max(ancho_p, alto_p)

with st.sidebar.expander("🌪️ Viento y Térmico", expanded=True):
    p_viento = st.number_input("Presión de Diseño (kgf/m²)", value=150.0)
    delta_T = st.slider("Diferencial Térmico ΔT (°C)", 10, 80, 50)
    gt_cinta = st.selectbox("Espesor Cinta VHB (mm)", [1.1, 1.6, 2.3], index=1)
    
    # Parámetros fijos de seguridad 3M
    FS_FIJO = 5.0
    ancho_minimo_3m = 15.0

# =================================================================
# 3. MOTOR DE CÁLCULO
# =================================================================

# A. Peso del Vidrio
peso_vidrio = (ancho_p * alto_p * (t_vidrio/1000)) * 2500

# B. Ancho por Viento (Bondline Width)
# Capacidad dinámica 3M: 85,000 Pa. Esfuerzo admisible = 85,000 / 5 = 17,000 Pa ≈ 1734 kgf/m²
adm_dinamico = 1734 
ancho_viento_mm = (p_viento * lado_menor) / (2 * adm_dinamico) * 1000

# C. Ancho por Dilatación Térmica (Regla del 15% de 3M)
# Coeficientes de expansión (Aluminio vs Vidrio)
alfa_al, alfa_vi = 23.2e-6, 9.0e-6
delta_L = (lado_mayor * 1000) * abs(alfa_al - alfa_vi) * delta_T
# El ancho debe ser tal que el delta_L no supere el 15% del espesor, 
# pero 3M recomienda Bondline >= 6.7 * delta_L para seguridad técnica
ancho_termico_mm = delta_L / 0.15 

# Ancho Final (El mayor de todos, mínimo 15mm según 3M)
ancho_final = max(math.ceil(ancho_viento_mm), math.ceil(ancho_termico_mm), ancho_minimo_3m)

# =================================================================
# 4. DESPLIEGUE DE RESULTADOS
# =================================================================
st.subheader("📊 Resultados de Análisis Estructural")

st.markdown(f"""
<div class="weight-box">
    <p style="margin:5px 0; color:#555;">Peso Total del Panel: <strong>{peso_vidrio:.2f} kgf</strong></p>
    <p style="font-size: 1.1em; margin:0; color:#28a745; font-weight:bold;">✅ Peso soportado por CALZOS (Setting Blocks)</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Ancho (Viento)", f"{ancho_viento_mm:.2f} mm")
with c2:
    st.metric("Ancho (Térmico)", f"{ancho_termico_mm:.2f} mm")
with c3:
    st.metric("Espesor (gt)", f"{gt_cinta} mm")

st.markdown("### 🔍 Detalles de la Junta de Cinta")
col_fig, col_txt = st.columns([1, 1])

with col_fig:
    if os.path.exists("cinta.png"):
        st.image("cinta.png", caption="Nomenclatura Cinta VHB™", use_column_width=True)
    else:
        st.info("💡 Sube 'cinta.png' a la carpeta principal para ver el esquema técnico.")
        

with col_txt:
    st.markdown(f"""
    <div class="result-box" style="margin-top:0;">
        <h3 style="margin-top:0;">✅ Especificación Final:</h3>
        <p style="font-size: 1.4em;">
            <strong>Ancho de Cinta:</strong> <span style="color: #cc0000;">{ancho_final} mm</span><br>
            <strong>Espesor (gt):</strong> <span style="color: #003366;">{gt_cinta} mm</span>
        </p>
        <hr>
        <strong>Resumen Técnico:</strong>
        <ul>
            <li>Gobernado por: {'Viento' if ancho_viento_mm > ancho_termico_mm else 'Dilatación Térmica'}.</li>
            <li>Factor de Seguridad Dinámico: {FS_FIJO}</li>
            <li>Capacidad Adm. Dinámica: {adm_dinamico} kgf/m²</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 5. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad: Ancho de Cinta vs Presión de Viento")

p_rango = np.linspace(50, 450, 30)
w_rango = [(p * lado_menor) / (2 * adm_dinamico) * 1000 for p in p_rango]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(p_rango, w_rango, color='#cc0000', lw=2.5, label=f'Requerido por Viento (FS={FS_FIJO})')
ax.axhline(ancho_minimo_3m, color='black', ls='--', label=f'Mínimo 3M ({ancho_minimo_3m}mm)')
ax.axhline(ancho_termico_mm, color='blue', ls=':', label=f'Mínimo Térmico ({ancho_termico_mm:.1f}mm)')

ax.fill_between(p_rango, w_rango, ancho_minimo_3m, color='#cc0000', alpha=0.05)

ax.set_xlabel("Presión de Diseño p (kgf/m²)")
ax.set_ylabel("Ancho de Cinta (mm)")
ax.grid(True, alpha=0.3, ls='--')
ax.legend()
st.pyplot(fig)

# =================================================================
# 6. CIERRE
# =================================================================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; margin-top: 20px;">
        <p style="font-family: 'Georgia', serif; font-size: 1.4em; color: #003366; font-style: italic;">
            "Programming is understanding"
        </p>
        <p style="font-size: 0.9em; color: #666;">Mauricio Riquelme | Proyectos Estructurales EIRL</p>
    </div>
""", unsafe_allow_html=True)