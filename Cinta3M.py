# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import base64
import os

st.set_page_config(page_title="Diseño Cinta 3M VHB | Mauricio Riquelme", layout="wide")

# Estilo Estructural
st.markdown("""
    <style>
    .main > div { padding-left: 2.5rem; padding-right: 2.5rem; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .result-box { background-color: #fff4f4; padding: 25px; border-left: 8px solid #cc0000; border-radius: 8px; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.title("🔴 Diseño de Unión con Cinta 3M™ VHB™")
st.markdown("#### **Metodología de Cálculo según Guía Técnica de 3M para Fachadas**")
st.divider()

# --- SIDEBAR ---
st.sidebar.header("⚙️ Parámetros de Diseño")
with st.sidebar.expander("📐 Geometría del Panel", expanded=True):
    ancho = st.number_input("Ancho del Vidrio/Panel (m)", value=1.20, step=0.05)
    alto = st.number_input("Alto del Vidrio/Panel (m)", value=2.40, step=0.05)
    t_panel = st.number_input("Espesor del Panel (mm)", value=6.0, step=1.0)
    densidad = st.number_input("Densidad Material (kg/m³)", value=2500, help="Vidrio: 2500, Aluminio: 2700")

with st.sidebar.expander("🌪️ Cargas y Propiedades VHB", expanded=True):
    p_viento = st.number_input("Presión de Diseño (kgf/m²)", value=150.0)
    # Valores típicos de diseño 3M (con factor de seguridad incluido)
    adm_dinamico = 8500  # kgf/m² (aprox 12 psi para ráfagas)
    adm_estatico = 175   # kgf/m² (aprox 0.25 psi para peso muerto)
    delta_T = st.slider("Diferencial Térmico ΔT (°C)", 10, 80, 50)

# --- CÁLCULOS ---
# 1. Peso Propio
peso_kg = ancho * alto * (t_panel/1000) * densidad

# 2. Área Requerida por Viento (Dinámico)
# Ancho de cinta = (Presión * Lado Menor) / (2 * Esfuerzo Admisible)
area_viento_mm = (p_viento * min(ancho, alto)) / (2 * adm_dinamico / 10000) * 10 

# 3. Área Requerida por Peso (Estatico) - Basado en 3M (0.25 psi / 175 kg/m2)
# Se requiere 55 cm2 de cinta por cada kg de peso para carga permanente
area_peso_total_cm2 = peso_kg / (adm_estatico / 10000)
perimetro_m = 2 * (ancho + alto)
ancho_cinta_peso_mm = (area_peso_total_cm2 / (perimetro_m * 100)) * 10

# 4. Expansión Térmica (Límite de espesor de cinta)
# La cinta debe ser al menos 2 veces el movimiento diferencial
mov_termico = max(ancho, alto) * 1000 * abs(23.2e-6 - 9.0e-6) * delta_T
espesor_min_cinta = mov_termico * 2

# --- RESULTADOS ---
st.subheader("📊 Resultados de Análisis")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Peso del Panel", f"{peso_kg:.2f} kgf")
with c2:
    st.metric("Ancho por Viento", f"{area_viento_mm:.2f} mm")
with c3:
    st.metric("Espesor Mín. Cinta", f"{espesor_min_cinta:.2f} mm")

ancho_final = max(math.ceil(area_viento_mm), math.ceil(ancho_cinta_peso_mm), 15) # Mínimo 15mm por aplicación



st.markdown(f"""
<div class="result-box">
    <h3>✅ Especificación de Cinta VHB:</h3>
    <p style="font-size: 1.2em;">
        <strong>Ancho de Cinta Requerido:</strong> {ancho_final} mm<br>
        <strong>Espesor Recomendado:</strong> > {espesor_min_cinta:.2f} mm (Usar 2.3mm o superior)
    </p>
    <hr>
    <strong>Nota Técnica 3M:</strong> El ancho de cinta por peso propio es crítico en paneles sin apoyo mecánico inferior. 
    Se recomienda siempre el uso de soportes de carga (setting blocks).
</div>
""", unsafe_allow_html=True)

# --- GRÁFICO ---
st.subheader("📈 Sensibilidad: Ancho de Cinta vs Viento")
p_rango = np.linspace(50, 400, 20)
b_rango = [(p * min(ancho, alto)) / (2 * adm_dinamico / 10000) * 10 for p in p_rango]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(p_rango, b_rango, color='#cc0000', label='Ancho requerido (Viento)')
ax.axhline(15, color='black', ls='--', label='Mínimo constructivo (15mm)')
ax.set_xlabel("Presión (kgf/m²)")
ax.set_ylabel("Ancho Cinta (mm)")
ax.legend()
st.pyplot(fig)

st.markdown("---")
st.markdown('<p style="text-align: center; font-style: italic;">"Programming is understanding"</p>', unsafe_allow_html=True)