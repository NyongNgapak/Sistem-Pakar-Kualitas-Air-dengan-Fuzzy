import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

st.set_page_config(page_title="Sistem Pakar Kualitas Air", layout="centered")

st.title("💧 Sistem Pakar Penentuan Kualitas Air Minum (Fuzzy)")
st.write("Menentukan kualitas air berdasarkan pH, kekeruhan, dan TDS")

# ==========================
# FUZZY VARIABLE
# ==========================

ph = ctrl.Antecedent(np.arange(0, 15, 0.1), 'pH')
kekeruhan = ctrl.Antecedent(np.arange(0, 20, 0.1), 'Kekeruhan')
tds = ctrl.Antecedent(np.arange(0, 2000, 1), 'TDS')

kualitas = ctrl.Consequent(np.arange(0, 101, 1), 'Kualitas')

# ==========================
# MEMBERSHIP FUNCTION
# ==========================

# pH
ph['Asam'] = fuzz.trapmf(ph.universe, [0, 0, 5.5, 6.5])
ph['Netral'] = fuzz.trimf(ph.universe, [6.5, 7, 7.5])
ph['Basa'] = fuzz.trapmf(ph.universe, [7.5, 8.5, 14, 14])

# Kekeruhan (NTU)
kekeruhan['Jernih'] = fuzz.trapmf(kekeruhan.universe, [0, 0, 2, 5])
kekeruhan['Sedang'] = fuzz.trimf(kekeruhan.universe, [3, 7, 11])
kekeruhan['Keruh'] = fuzz.trapmf(kekeruhan.universe, [9, 12, 20, 20])

# TDS (ppm)
tds['Rendah'] = fuzz.trapmf(tds.universe, [0, 0, 200, 500])
tds['Sedang'] = fuzz.trimf(tds.universe, [300, 600, 900])
tds['Tinggi'] = fuzz.trapmf(tds.universe, [700, 1000, 2000, 2000])

# Output Kualitas
kualitas['Buruk'] = fuzz.trapmf(kualitas.universe, [0, 0, 30, 45])
kualitas['Cukup'] = fuzz.trimf(kualitas.universe, [40, 55, 70])
kualitas['Baik'] = fuzz.trapmf(kualitas.universe, [65, 80, 100, 100])

# ==========================
# RULE BASE
# ==========================

rule1 = ctrl.Rule(ph['Netral'] & kekeruhan['Jernih'] & tds['Rendah'], kualitas['Baik'])
rule2 = ctrl.Rule(ph['Asam'] & kekeruhan['Keruh'], kualitas['Buruk'])
rule3 = ctrl.Rule(ph['Netral'] & tds['Sedang'], kualitas['Cukup'])
rule4 = ctrl.Rule(kekeruhan['Sedang'] & tds['Sedang'], kualitas['Cukup'])
rule5 = ctrl.Rule(ph['Basa'] & kekeruhan['Keruh'], kualitas['Buruk'])
rule6 = ctrl.Rule(ph['Netral'] & kekeruhan['Jernih'] & tds['Sedang'], kualitas['Cukup'])

# ==========================
# CONTROL SYSTEM
# ==========================

kualitas_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6
])

kualitas_simulasi = ctrl.ControlSystemSimulation(kualitas_ctrl)

# ==========================
# INPUT UI
# ==========================

st.subheader("🔹 Masukkan Parameter Air")

ph_input = st.number_input("pH Air", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
kekeruhan_input = st.number_input("Kekeruhan (NTU)", min_value=0.0, max_value=20.0, value=3.0)
tds_input = st.number_input("TDS (ppm)", min_value=0, max_value=2000, value=400)

# ==========================
# PROCESS BUTTON
# ==========================

if st.button("🔍 Tentukan Kualitas Air"):
    kualitas_simulasi.input['pH'] = ph_input
    kualitas_simulasi.input['Kekeruhan'] = kekeruhan_input
    kualitas_simulasi.input['TDS'] = tds_input

    kualitas_simulasi.compute()
    hasil = kualitas_simulasi.output['Kualitas']

    if hasil <= 45:
        kategori = "🚫 Buruk"
    elif hasil <= 70:
        kategori = "⚠️ Cukup"
    else:
        kategori = "✅ Baik"

    st.success(f"Nilai Kualitas Air: **{hasil:.2f}**")
    st.subheader(f"Hasil Akhir: **{kategori}**")

# ==========================
# FOOTER
# ==========================

st.markdown("---")
st.caption("Sistem Pakar Fuzzy Logic | Python + Streamlit")
