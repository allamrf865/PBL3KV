import streamlit as st
import plotly.graph_objs as go
import numpy as np
import json
from datetime import datetime

# Fungsi untuk memuat data pasien dari JSON
def load_patient_data(file_path="sample_data.json"):
    with open(file_path) as f:
        data = json.load(f)
    return data

# Pengaturan halaman aplikasi
st.set_page_config(page_title="3D Medical Dashboard", layout="wide")

# Judul aplikasi
st.title("🌌 Advanced 3D Medical Dashboard for Acute Coronary Syndrome 🌌")

# Mengambil data pasien dari JSON
patient_data = load_patient_data()

if patient_data:
    # Panel data pasien dengan informasi dasar dan riwayat
    st.sidebar.header("🧑‍⚕️ Informasi Pasien")
    st.sidebar.write(f"**Nama**: {patient_data['name']}")
    st.sidebar.write(f"**Usia**: {patient_data['age']} tahun")
    st.sidebar.write(f"**Jenis Kelamin**: {patient_data['gender']}")
    st.sidebar.write(f"**Diabetes**: {'Ya' if patient_data['medical_history']['diabetes'] else 'Tidak'}")
    st.sidebar.write(f"**Hipertensi**: {'Ya' if patient_data['medical_history']['hypertension'] else 'Tidak'}")

    # Form untuk input data vital
    st.subheader("📝 Input Data Vital Baru")
    with st.form("update_data_form"):
        heart_rate = st.number_input("Detak Jantung (BPM)", min_value=50, max_value=200, value=int(patient_data["current_conditions"]["heart_rate"]))
        blood_pressure = st.number_input("Tekanan Darah (mmHg)", min_value=80, max_value=200, value=int(patient_data["current_conditions"]["blood_pressure"]))
        oxygen_level = st.slider("Kadar Oksigen (%)", 80, 100, int(patient_data["current_conditions"]["oxygen_level"]))
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Update JSON dengan data baru
            patient_data["current_conditions"]["heart_rate"] = heart_rate
            patient_data["current_conditions"]["blood_pressure"] = blood_pressure
            patient_data["current_conditions"]["oxygen_level"] = oxygen_level
            save_patient_data(patient_data)
            st.success("Data berhasil diperbarui!")

    # Grafik 3D untuk visualisasi vital signs
    st.subheader("📊 Grafik 3D Vital Signs Pasien")
    heart_rate_values = np.random.normal(patient_data['current_conditions']['heart_rate'], 5, 30)
    blood_pressure_values = np.random.normal(patient_data['current_conditions']['blood_pressure'], 10, 30)
    oxygen_level_values = np.random.normal(patient_data['current_conditions']['oxygen_level'], 2, 30)
    vital_signs_graph = go.Scatter3d(
        x=heart_rate_values,
        y=blood_pressure_values,
        z=oxygen_level_values,
        mode='lines+markers',
        marker=dict(size=5, color='lime', opacity=0.7),
        line=dict(color='blue', width=2)
    )
    layout_vital_signs = go.Layout(
        scene=dict(
            xaxis=dict(title='Heart Rate (BPM)'),
            yaxis=dict(title='Blood Pressure (mmHg)'),
            zaxis=dict(title='Oxygen Level (%)')
        )
    )
    fig_vital_signs = go.Figure(data=[vital_signs_graph], layout=layout_vital_signs)
    st.plotly_chart(fig_vital_signs, use_container_width=True)

    # Model 3D anatomi manusia
    st.subheader("🔬 Model 3D Anatomi dengan Anotasi Penyakit")
    anatomy_mesh = go.Mesh3d(x=np.linspace(-5, 5, 100), y=np.linspace(-10, 10, 100), z=np.linspace(0, 20, 100), opacity=0.2, color='lightblue')
    disease_annotations = go.Scatter3d(
        x=[d['x'] for d in patient_data["disease_annotations"]],
        y=[d['y'] for d in patient_data["disease_annotations"]],
        z=[d['z'] for d in patient_data["disease_annotations"]],
        mode='markers+text',
        marker=dict(size=10, color='red'),
        text=[f"{d['part']}: {d['description']}" for d in patient_data["disease_annotations"]],
    )
    fig_anatomy = go.Figure(data=[anatomy_mesh, disease_annotations])
    fig_anatomy.update_layout(scene=dict(xaxis=dict(title='X'), yaxis=dict(title='Y'), zaxis=dict(title='Z')))
    st.plotly_chart(fig_anatomy, use_container_width=True)
    
    # Rekomendasi gizi dan rehabilitasi
    st.subheader("🍲 Rekomendasi Nutrisi & Rehabilitasi")
    st.write(patient_data["recommendations"]["nutritional_advice"])
    st.write(patient_data["recommendations"]["rehabilitation_plan"])

else:
    st.error("Data pasien tidak ditemukan.")
