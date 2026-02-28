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
st.markdown("#### **Cálculo del Ancho de Cinta para Carga de Viento**")
st.divider()

# =================================================================
# 3. SIDEBAR: PARÁMETROS DE DISEÑO
# =================================================================
st.sidebar.header("⚙️ Parámetros de Diseño")

with st.sidebar.expander("📐 Geometría del Panel", expanded=True):
    ancho_p = st.number_input("Ancho del Panel (m)", value=1.20, step=0.05)
    alto_p = st.number_input("Alto del Panel (m)", value=2.40, step=0.05)
    # El lado menor gobierna la transferencia de carga tributaria
    lado_menor = min(ancho_p, alto_p)

with st.sidebar.expander("🌪️ Carga de Viento y Seguridad", expanded=True):
    p_viento = st.number_input("Presión de Diseño (kgf/m²)", value=150.0)
    
    # Factor de Seguridad (FS) constante = 5
    FS_FIJO = 5.0
    st.markdown(f"**Factor de Seguridad (FS):** `{FS_FIJO}`")
    
    # Capacidad última nominal de tracción dinámica VHB (aprox. 50 psi)
    capacidad_ultima_kgm2 = 35150  
    
    # Esfuerzo admisible dinámico
    adm_dinamico = capacidad_ultima_kgm2 / FS_FIJO
    st.info(f"Esfuerzo Adm. Dinámico: {adm_dinamico:.0f} kgf/m²")

# =================================================================
# 4. MOTOR DE CÁLCULO RIGUROSO
# =================================================================

# Cálculo del ancho de cinta (Bondline Width) en mm
# Fórmula: (Presion [kgf/m2] * Lado_Menor [m]) / (2 * Adm_Dinamico [kgf/m2]) * 1000 [mm/m]
ancho_cinta_calculado_mm = (p_viento * lado_menor) / (2 * adm_dinamico) * 1000

# Mínimo recomendado por 3M para aplicaciones de fachada estructural
ancho_minimo_3m = 15.0
ancho_final = max(math.ceil(ancho_cinta_calculado_mm), ancho_minimo_3m)

# =================================================================
# 5. RESULTADOS
# =================================================================
st.subheader("📊 Análisis de Ancho de Cinta")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Presión (q)", f"{p_viento} kgf/m²")
with c2:
    st.metric("Ancho Calculado", f"{ancho_cinta_calculado_mm:.2f} mm")
with c3:
    st.metric("Ancho Mínimo de Cinta Sugerido", f"{ancho_final} mm")



st.markdown(f"""
<div class="result-box">
    <h3>✅ Especificación de la Unión:</h3>
    <p style="font-size: 1.3em; margin-bottom: 0;">
        <strong>Ancho de Cinta VHB Mínimo:</strong> <span style="color: #cc0000;">{ancho_final} mm</span>
    </p>
    <hr>
    <strong>Notas Técnicas:</strong> 
    <ul>
        <li><strong>Bondline Width:</strong> El ancho calculado asegura que la cinta trabaje dentro de su rango elástico bajo ráfagas críticas.</li>
        <li><strong>Factor de Seguridad:</strong> Se aplica un FS=5 sobre la capacidad de ruptura última.</li>
        <li><strong>Carga Muerta:</strong> Esta cinta debe trabajar en conjunto con apoyos mecánicos (setting blocks) para el peso propio del panel.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. GRÁFICO DE SENSIBILIDAD
# =================================================================
st.subheader("📈 Sensibilidad: Ancho de Cinta vs Presión de Viento")

p_rango = np.linspace(50, 450, 30)
# Re-calculamos el ancho para el rango del gráfico
w_rango = [(p * lado_menor) / (2 * adm_dinamico) * 1000 for p in p_rango]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(p_rango, w_rango, color='#cc0000', lw=2.5, label=f'Ancho Requerido (FS={FS_FIJO})')
ax.axhline(ancho_minimo_3m, color='black', ls='--', label='Mínimo constructivo (15mm)')
ax.fill_between(p_rango, w_rango, ancho_minimo_3m, where=(np.array(w_rango) > ancho_minimo_3m), color='#cc0000', alpha=0.1)

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