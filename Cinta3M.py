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
st.markdown("#### **Determinación de Ancho de Cinta (Bite) por Carga de Viento**")
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

with st.sidebar.expander("🌪️ Parámetros de Viento", expanded=True):
    p_viento = st.number_input("Presión de Diseño (kgf/m²)", value=150.0, step=5.0)
    
    # Constantes Técnicas 3M (Dinámico)
    # Esfuerzo admisible para viento = 12 psi (8,437 kgf/m2)
    adm_viento_kgm2 = 8437 
    ancho_minimo_3m = 15.0 # Mínimo constructivo recomendado

# =================================================================
# 3. MOTOR DE CÁLCULO
# =================================================================

# A. Peso del Vidrio (Solo informativo para calzos)
peso_vidrio = (ancho_p * alto_p * (t_vidrio/1000)) * 2500

# B. Ancho de Cinta Requerido por Viento (Bondline Width)
# Fórmula: (Presión * Lado Menor) / (2 * Esfuerzo Admisible)
ancho_viento_mm = (p_viento * lado_menor) / (2 * adm_viento_kgm2) * 1000

# Ancho Final (Máximo entre cálculo y mínimo constructivo)
ancho_final = max(math.ceil(ancho_viento_mm), ancho_minimo_3m)

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

c1, c2 = st.columns(2)
with c1:
    st.metric("Ancho Minimo Sugerido (Tracción/Succión Viento)", f"{ancho_viento_mm:.2f} mm")
with c2:
    st.metric("Esfuerzo Adm. (Dinámico)", "12 psi", delta="8,437 kgf/m²")

st.markdown("### 🔍 Detalle de Aplicación")
col_fig, col_txt = st.columns([1, 1])

with col_fig:
    if os.path.exists("cinta.png"):
        st.image("cinta.png", caption="Esquema Bondline VHB", use_column_width=True)
    else:
        st.info("💡 Sube 'cinta.png' para visualizar el detalle del Bite.")
        

with col_txt:
    st.markdown(f"""
    <div class="result-box" style="margin-top:0;">
        <h3 style="margin-top:0;">✅ Especificación Final:</h3>
        <p style="font-size: 1.6em; margin-bottom:10px;">
            <strong>Ancho de Cinta:</strong> <span style="color: #cc0000;">{ancho_final} mm</span>
        </p>
        <hr>
        <strong>Resumen de Diseño:</strong>
        <ul>
            <li>Carga de Viento: {p_viento} kgf/m²</li>
            <li>Factor de Seguridad incorporado en admisible (12 psi).</li>
            <li><strong>Importante:</strong> Uso de calzos obligatorio para carga muerta.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 5. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad: Ancho de Cinta vs Presión de Viento")

p_rango = np.linspace(50, 450, 40)
w_rango = [(p * lado_menor) / (2 * adm_viento_kgm2) * 1000 for p in p_rango]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(p_rango, w_rango, color='#cc0000', lw=2.5, label='Ancho Teórico Requerido')
ax.axhline(ancho_minimo_3m, color='black', ls='--', label=f'Mínimo Constructivo ({ancho_minimo_3m}mm)')
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