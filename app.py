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

# Fungsi untuk menyimpan data pasien ke JSON setelah input baru
def save_patient_data(data, file_path="sample_data.json"):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Pengaturan halaman aplikasi
st.set_page_config(page_title="3D Advanced Patient Monitoring", layout="wide")

# Judul aplikasi
st.title("🌌 Advanced 3D Anatomy Patient Monitoring System 🌌")

# Tampilkan waktu terakhir update
st.write(f"Data terakhir diperbarui pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Mengambil data pasien dari JSON
patient_data = load_patient_data()

# Jika data pasien tersedia
if patient_data:
    # Form input data baru untuk pasien
    st.subheader("📝 Input Data Baru Pasien")
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

    # Model Anatomi 3D dengan Plotly Mesh3D
    st.subheader("🔬 Model 3D Anatomi Manusia dengan Anotasi Penyakit")

    # Menggunakan Plotly untuk menampilkan model anatomi manusia dengan titik penyakit
    # Contoh sederhana untuk representasi dengan anotasi
    fig = go.Figure()

    # Model anatomi manusia (sederhana)
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-10, 10, 100)
    z = np.linspace(0, 20, 100)
    mesh3d = go.Mesh3d(x=x, y=y, z=z, opacity=0.2, color='lightblue')

    # Anotasi penyakit dari data JSON
    annotations = go.Scatter3d(
        x=[d['x'] for d in patient_data["disease_annotations"]],
        y=[d['y'] for d in patient_data["disease_annotations"]],
        z=[d['z'] for d in patient_data["disease_annotations"]],
        mode='markers+text',
        marker=dict(size=8, color='red'),
        text=[f"{d['part']}: {d['description']}" for d in patient_data["disease_annotations"]],
        textposition="top center"
    )

    fig.add_trace(mesh3d)
    fig.add_trace(annotations)

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X-Axis'),
            yaxis=dict(title='Y-Axis'),
            zaxis=dict(title='Z-Axis')
        ),
        title="Anatomi Manusia dengan Lokasi Penyakit"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Dashboard 3D Interaktif untuk Kesehatan Pasien
    st.subheader("📊 Dashboard 3D Kesehatan Pasien dengan Animasi")

    # Grafik interaktif untuk kesehatan pasien (detak jantung, tekanan darah, dan kadar oksigen)
    heart_rates = np.linspace(70, patient_data["current_conditions"]["heart_rate"], num=30)
    blood_pressures = np.linspace(120, patient_data["current_conditions"]["blood_pressure"], num=30)
    oxygen_levels = np.linspace(95, patient_data["current_conditions"]["oxygen_level"], num=30)

    health_graph = go.Scatter3d(
        x=heart_rates,
        y=blood_pressures,
        z=oxygen_levels,
        mode='lines+markers',
        marker=dict(size=6, color='cyan', opacity=0.8),
        line=dict(color='magenta', width=4)
    )

    # Pengaturan layout untuk tampilan interaktif tanpa animasi kompleks
    layout_health = go.Layout(
        scene=dict(
            xaxis=dict(title='Detak Jantung (BPM)', backgroundcolor="black", gridcolor="gray"),
            yaxis=dict(title='Tekanan Darah (mmHg)', backgroundcolor="black", gridcolor="gray"),
            zaxis=dict(title='Kadar Oksigen (%)', backgroundcolor="black", gridcolor="gray")
        ),
        title="Tren Kesehatan Pasien",
    )

    fig_health = go.Figure(data=[health_graph], layout=layout_health)
    st.plotly_chart(fig_health, use_container_width=True)

else:
    st.error("Data pasien tidak ditemukan.")
