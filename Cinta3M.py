# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import os

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO
# =================================================================
st.set_page_config(page_title="VHB Structural Lab | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .main > div { padding-left: 2.5rem; padding-right: 2.5rem; }
    .stMetric { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; }
    .result-box { 
        background-color: #fff4f4; 
        padding: 25px; 
        border: 1px solid #ffcccc;
        border-left: 10px solid #cc0000; 
        border-radius: 8px; 
    }
    .weight-box { 
        background-color: #ffffff; 
        padding: 15px; 
        border: 1px dashed #cc0000; 
        border-radius: 8px; 
        margin-bottom: 20px; 
        text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔴 VHB™ Structural Design Lab")
st.markdown("#### **Verificación de Bite: Tracción Dinámica y Cizalladura Estática**")
st.divider()

# =================================================================
# 2. SIDEBAR: PARÁMETROS TÉCNICOS RIGUROSOS
# =================================================================
st.sidebar.header("⚙️ Parámetros de Diseño")

with st.sidebar.expander("📐 Geometría del Panel", expanded=True):
    ancho_p = st.number_input("Ancho del Panel (m)", value=1.20, step=0.05)
    alto_p = st.number_input("Alto del Panel (m)", value=2.40, step=0.05)
    t_vidrio = st.number_input("Espesor Vidrio (mm)", value=6.0, step=1.0)
    lado_menor = min(ancho_p, alto_p)

with st.sidebar.expander("🌪️ Cargas y Seguridad", expanded=True):
    p_viento = st.number_input("Presión de Diseño (kgf/m²)", value=150.0, step=5.0)
    usa_calzos = st.checkbox("¿Usa calzos de apoyo?", value=True)
    
    # Valores de diseño según Boletín Técnico 3M
    # Dinámico: 12 psi ≈ 82.7 kPa ≈ 8435 kgf/m2
    adm_viento_psi = 12.0
    adm_viento_kpa = 82.7
    adm_viento_kgm2 = 8435  

    # Estático: 0.25 psi ≈ 1.72 kPa ≈ 173.5 kgf/m2
    adm_peso_psi = 0.25
    adm_peso_kpa = 1.72
    adm_peso_kgm2 = 173.5   
    
    ancho_minimo_3m = 15.0

# =================================================================
# 3. MOTOR DE CÁLCULO
# =================================================================

# A. Peso del Vidrio
peso_vidrio = (ancho_p * alto_p * (t_vidrio/1000)) * 2500

# B. Ancho por Viento (Tracción Dinámica)
ancho_viento_mm = (p_viento * lado_menor) / (2 * adm_viento_kgm2) * 1000

# C. Ancho por Peso (Cizalladura Estática)
if not usa_calzos:
    perimetro_m = 2 * (ancho_p + alto_p)
    ancho_peso_mm = (peso_vidrio / (perimetro_m * adm_peso_kgm2)) * 1000
else:
    ancho_peso_mm = 0.0

# Ancho Final
ancho_calculado = max(ancho_viento_mm, ancho_peso_mm, ancho_minimo_3m)
ancho_final = math.ceil(ancho_calculado)

# =================================================================
# 4. DESPLIEGUE DE RESULTADOS
# =================================================================
st.subheader("📊 Análisis de Desempeño Estructural")

st.markdown(f"""
<div class="weight-box">
    <p style="margin:5px 0; color:#555;">Masa del Panel: <strong>{peso_vidrio:.2f} kgf</strong></p>
    <p style="font-size: 1.1em; margin:0; color:{'#28a745' if usa_calzos else '#cc0000'}; font-weight:bold;">
        {'✅ Carga muerta soportada por CALZOS' if usa_calzos else '⚠️ CIZALLADURA PERMANENTE SOBRE CINTA'}
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Bite Requerido", f"{ancho_final} mm")
with c2:
    st.metric("Esfuerzo Adm. Viento", f"{adm_viento_psi} psi", f"{adm_viento_kpa} kPa")
with c3:
    st.metric("Esfuerzo Adm. Peso", f"{adm_peso_psi} psi", f"{adm_peso_kpa} kPa")

st.divider()

# --- SECCIÓN DE ESQUEMA Y ESPECIFICACIÓN ---
col_fig, col_txt = st.columns([1, 1.2])

with col_fig:
    st.markdown("### 🔍 Detalle del Bite")
    if os.path.exists("cinta.png"):
        st.image("cinta.png", caption="Bondline Width (Bite) - Detalle Típico", use_column_width=True)
    else:
        st.info("💡 Sube 'cinta.png' para ver el esquema técnico.")

with col_txt:
    st.markdown(f"""
    <div class="result-box">
        <h3 style="margin-top:0; color:#cc0000;">✅ Especificación Final:</h3>
        <p style="font-size: 2em; margin-bottom:10px; font-weight:bold;">
            Ancho Sugerido: {ancho_final} mm
        </p>
        <hr>
        <strong>Resumen de Verificación Técnica:</strong>
        <ul>
            <li>Criterio Dominante: <strong>{'Viento (Dinámico)' if ancho_viento_mm > ancho_peso_mm else 'Peso (Estático)'}</strong>.</li>
            <li>Tensión Adm. Dinámica: {adm_viento_psi} psi ({adm_viento_kpa} kPa).</li>
            <li>Tensión Adm. Estática: {adm_peso_psi} psi ({adm_peso_kpa} kPa).</li>
            <li>{"Uso de calzos obligatorio." if usa_calzos else "Diseño apto para cizalladura permanente."}</li>
            <li>Se recomienda limpieza con Isopropanol/Agua (50:50).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if not usa_calzos:
    st.error("❗ **Nota sobre Cizalle:** El diseño sin calzos requiere validación de 3M para garantizar la adhesión a largo plazo.")

# =================================================================
# 5. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad del Diseño")
p_range = np.linspace(50, 500, 50)
w_v_range = [(p * lado_menor) / (2 * adm_viento_kgm2) * 1000 for p in p_range]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(p_range, w_v_range, color='#cc0000', lw=2, label='Requerido por Viento')
if not usa_calzos:
    ax.axhline(ancho_peso_mm, color='#333', ls='--', label='Requerido por Peso')
ax.axhline(ancho_minimo_3m, color='gray', ls=':', label='Mínimo 3M (15mm)')

ax.set_xlabel("Presión de Diseño (kgf/m²)")
ax.set_ylabel("Ancho de Cinta (mm)")
ax.legend()
st.pyplot(fig)

# =================================================================
# 6. CIERRE
# =================================================================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <strong>Mauricio Riquelme | Proyectos Estructurales EIRL</strong><br>
        <em>"Programming is understanding"</em>
    </div>
""", unsafe_allow_html=True)