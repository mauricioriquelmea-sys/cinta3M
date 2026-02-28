# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# =================================================================
# 1. CONFIGURACIÓN Y ESTILO (WIDE)
# =================================================================
st.set_page_config(page_title="Cálculo VHB Viento | Mauricio Riquelme", layout="wide")

st.markdown("""
    <style>
    .main > div { padding-left: 2.5rem; padding-right: 2.5rem; max-width: 100%; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .result-box { background-color: #fff4f4; padding: 25px; border-left: 8px solid #cc0000; border-radius: 8px; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. ENCABEZADO
# =================================================================
st.title("🔴 Diseño de Unión con Cinta 3M™ VHB™")
st.markdown("#### **Verificación por Carga Dinámica (Viento) - FS = 5**")
st.divider()

# =================================================================
# 3. SIDEBAR: PARÁMETROS DE DISEÑO (SIN DUPLICADOS)
# =================================================================
st.sidebar.header("⚙️ Parámetros de Diseño")

with st.sidebar.expander("📐 Geometría del Panel", expanded=True):
    ancho = st.number_input("Ancho del Panel (m)", value=1.20, step=0.05)
    alto = st.number_input("Alto del Panel (m)", value=2.40, step=0.05)
    lado_menor = min(ancho, alto)

with st.sidebar.expander("🌪️ Carga de Viento y Seguridad", expanded=True):
    p_viento = st.number_input("Presión de Diseño (kgf/m²)", value=150.0)
    
    # Factor de Seguridad constante y no editable
    FS_FIJO = 5.0
    st.markdown(f"**Factor de Seguridad (FS):** `{FS_FIJO}`")
    
    # Capacidad última nominal VHB (aprox. 50 psi)
    capacidad_ultima = 35150  # kgf/m²
    
    # Esfuerzo admisible derivado
    adm_dinamico = capacidad_ultima / FS_FIJO
    
    st.info(f"Esfuerzo Adm. Dinámico: {adm_dinamico:.0f} kgf/m²")

# =================================================================
# 4. MOTOR DE CÁLCULO
# =================================================================

# Cálculo del ancho de cinta necesario (mm)
# (Presion * Lado_Menor) / (2 * Esfuerzo_Adm_en_cm2) * 10
ancho_cinta_mm = (p_viento * lado_menor) / (2 * (adm_dinamico / 10000)) * 10 

# Aplicación del mínimo constructivo de 15 mm
ancho_final = max(math.ceil(ancho_cinta_mm), 15)

# =================================================================
# 5. RESULTADOS
# =================================================================
st.subheader("📊 Resultados de Análisis Dinámico")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Presión (Carga)", f"{p_viento} kgf/m²")
with c2:
    st.metric("Ancho Calculado", f"{ancho_cinta_mm:.2f} mm")
with c3:
    st.metric("Bite Sugerido", f"{ancho_final} mm")



st.markdown(f"""
<div class="result-box">
    <h3>✅ Especificación Técnica (FS=5):</h3>
    <p style="font-size: 1.3em; margin-bottom: 0;">
        <strong>Ancho de Cinta VHB Requerido:</strong> <span style="color: #cc0000;">{ancho_final} mm</span>
    </p>
    <hr>
    <strong>Notas de Seguridad:</strong> 
    <ul>
        <li>Factor de Seguridad Aplicado: <strong>{FS_FIJO}</strong> (Estándar de alta exigencia).</li>
        <li>Este diseño solo verifica la carga de viento; requiere apoyos para carga muerta.</li>
        <li>Capacidad última considerada: {capacidad_ultima} kgf/m².</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad: Ancho de Cinta vs Presión de Viento")

p_rango = np.linspace(50, 450, 30)
b_rango = [(p * lado_menor) / (2 * (adm_dinamico / 10000)) * 10 for p in p_rango]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(p_rango, b_rango, color='#cc0000', lw=2.5, label=f'Curva de Diseño (FS={FS_FIJO})')
ax.axhline(15, color='black', ls='--', label='Mínimo Constructivo (15mm)')
ax.fill_between(p_rango, b_rango, 15, where=(np.array(b_rango) > 15), color='#cc0000', alpha=0.1)

ax.set_xlabel("Presión de Diseño p (kgf/m²)")
ax.set_ylabel("Ancho de Cinta (mm)")
ax.grid(True, alpha=0.3, ls='--')
ax.legend()
st.pyplot(fig)

# =================================================================
# 7. CIERRE
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