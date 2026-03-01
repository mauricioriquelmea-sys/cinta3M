# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import base64
from fpdf import FPDF

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
        margin: 20px 0;
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
st.markdown("#### **Verificación de Bite según Estándares Técnicos 3M (kPa)**")
st.divider()

# =================================================================
# 2. SIDEBAR: PARÁMETROS TÉCNICOS
# =================================================================
st.sidebar.header("⚙️ Parámetros de Diseño")

with st.sidebar.expander("📐 Geometría del Panel", expanded=True):
    ancho_p = st.sidebar.number_input("Ancho del Panel (m)", value=1.20, step=0.05)
    alto_p = st.sidebar.number_input("Alto del Panel (m)", value=2.40, step=0.05)
    t_vidrio = st.sidebar.number_input("Espesor Vidrio (mm)", value=6.0, step=1.0)
    lado_menor = min(ancho_p, alto_p)

with st.sidebar.expander("🌪️ Cargas y Seguridad", expanded=True):
    p_viento = st.sidebar.number_input("Presión de Diseño (kgf/m²)", value=150.0, step=5.0)
    usa_calzos = st.sidebar.checkbox("¿Usa calzos de apoyo?", value=True)
    
    # VALORES ESTRICTOS 3M
    adm_viento_kpa = 85.0
    adm_viento_kgm2 = 85.0 * 101.97
    adm_peso_kpa = 1.7
    adm_peso_kgm2 = 1.7 * 101.97
    ancho_minimo_3m = 15.0

# =================================================================
# 3. MOTOR DE CÁLCULO
# =================================================================
peso_vidrio = (ancho_p * alto_p * (t_vidrio/1000)) * 2500
ancho_viento_mm = (p_viento * lado_menor) / (2 * adm_viento_kgm2) * 1000

if not usa_calzos:
    perimetro_m = 2 * (ancho_p + alto_p)
    ancho_peso_mm = (peso_vidrio / (perimetro_m * adm_peso_kgm2)) * 1000
else:
    ancho_peso_mm = 0.0

ancho_final = math.ceil(max(ancho_viento_mm, ancho_peso_mm, ancho_minimo_3m))

# =================================================================
# 4. GENERADOR DE PDF PROFESIONAL (ESTÁTICO)
# =================================================================
def generar_pdf_vhb():
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists("Logo.png"):
        pdf.image("Logo.png", x=10, y=8, w=33)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Memoria de Calculo: Cinta VHB(TM)", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 7, "Proyectos Estructurales | Mauricio Riquelme", ln=True, align='C')
    pdf.ln(15)

    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 1. DATOS DEL PANEL", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f" Dimensiones: {ancho_p}m x {alto_p}m | Peso: {peso_vidrio:.2f} kgf", ln=True)
    pdf.cell(0, 8, f" Presion Viento: {p_viento} kgf/m2 | Calzos de Apoyo: {'SI' if usa_calzos else 'NO'}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 2. CRITERIOS TECNICOS 3M", ln=True, fill=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f" Esfuerzo Adm. Dinamico (Viento): {adm_viento_kpa} kPa (FS=5)", ln=True)
    pdf.cell(0, 8, f" Esfuerzo Adm. Estatico (Peso): {adm_peso_kpa} kPa (FS=10)", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, " 3. RESULTADO DE BITE (BONDLINE WIDTH)", ln=True, fill=True)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 12, f" ANCHO MINIMO REQUERIDO: {ancho_final} mm", ln=True, align='C')
    
    pdf.set_y(-25)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Calculo basado en estandares de Servicio Tecnico 3M Chile", align='C')
    return pdf.output()

# Botón persistente en sidebar
pdf_bytes = generar_pdf_vhb()
b64 = base64.b64encode(pdf_bytes).decode()
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <a href="data:application/pdf;base64,{b64}" download="Memoria_VHB_{ancho_final}mm.pdf" 
           style="background-color: #cc0000; color: white; padding: 12px 20px; text-decoration: none; 
           border-radius: 5px; font-weight: bold; display: block;">
           📥 DESCARGAR REPORTE VHB
        </a>
    </div>
""", unsafe_allow_html=True)

# =================================================================
# 5. RESULTADOS EN PANTALLA
# =================================================================
st.subheader("📊 Análisis Estructural (Métrica 3M)")

st.markdown(f"""
<div class="weight-box">
    <p style="margin:5px 0; color:#555;">Masa del Panel: <strong>{peso_vidrio:.2f} kgf</strong></p>
    <p style="font-size: 1.1em; margin:0; color:{'#28a745' if usa_calzos else '#cc0000'}; font-weight:bold;">
        {'✅ Carga muerta soportada por CALZOS' if usa_calzos else '⚠️ CIZALLADURA PERMANENTE SOBRE CINTA'}
    </p>
</div>
""", unsafe_allow_html=True)

if not usa_calzos:
    st.error("🚨 **ALERTA:** Configuraciones sin calzos requieren aprobación expresa de 3M.")

c1, c2, c3 = st.columns(3)
with c1: st.metric("Bite Requerido", f"{ancho_final} mm")
with c2: st.metric("Adm. Viento", f"{adm_viento_kpa} kPa")
with c3: st.metric("Adm. Peso", f"{adm_peso_kpa} kPa")

st.divider()

col_fig, col_txt = st.columns([1, 1.2])
with col_fig:
    if os.path.exists("cinta.png"):
        st.image("cinta.png", caption="Detalle de Unión VHB", use_column_width=True)

with col_txt:
    st.markdown(f"""
    <div class="result-box">
        <h3 style="margin-top:0; color:#cc0000;">✅ Especificación Final:</h3>
        <p style="font-size: 2.2em; margin-bottom:10px; font-weight:bold;">{ancho_final} mm</p>
        <hr>
        <li>Criterio: <strong>{'Viento' if ancho_viento_mm > ancho_peso_mm else 'Peso'}</strong></li>
        <li>Ancho Mínimo Constructivo: 15 mm</li>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de Sensibilidad
p_range = np.linspace(50, 500, 50)
w_v_range = [(p * lado_menor) / (2 * adm_viento_kgm2) * 1000 for p in p_range]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(p_range, w_v_range, color='#cc0000', label='Bite Dinámico'); ax.grid(True, alpha=0.3)
st.pyplot(fig)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Mauricio Riquelme | Proyectos Estructurales Lab</div>", unsafe_allow_html=True)