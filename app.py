import streamlit as st
import plotly.graph_objs as go
import numpy as np
import json
from datetime import datetime
from streamlit.components.v1 import html

# Fungsi untuk memuat data pasien dari JSON
def load_patient_data(file_path="sample_data.json"):
    with open(file_path) as f:
        data = json.load(f)
    return data

# Pengaturan halaman aplikasi
st.set_page_config(page_title="Advanced 3D Patient Monitoring", layout="wide")
st.markdown(
    """
    <style>
        .reportview-container {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #cfcfcf;
        }
        h1, h2, h3 {
            color: #39FF14;
            text-shadow: 0px 0px 10px rgba(57, 255, 20, 0.7);
        }
        .stText, .stMarkdown {
            color: #A9F1FF;
        }
        .data-input-container {
            background-color: #111;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(57, 255, 20, 0.5);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul aplikasi
st.title("🌌 Advanced 3D Holographic Patient Monitoring System 🌌")

# Tampilkan waktu terakhir update
st.write(f"Data terakhir diperbarui pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Mengambil data pasien dari JSON
patient_data = load_patient_data()

# Jika data pasien tersedia
if patient_data:
    # Tampilan Dasbor dengan Model 3D Pasien
    st.subheader(f"🧑‍⚕️ Informasi Pasien: {patient_data['name']}")
    st.write(f"**ID Pasien**: {patient_data['patient_id']}")
    st.write(f"**Usia**: {patient_data['age']} tahun")
    st.write(f"**Jenis Kelamin**: {patient_data['gender']}")
    
    # Model 3D Pasien
    st.subheader("🔬 Model 3D Pasien")
    html("""
    <script type="module">
      import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.126.1/build/three.module.js';
      import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.126.1/examples/jsm/loaders/GLTFLoader.js';

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);

      const loader = new GLTFLoader();
      loader.load(
        'https://your_bucket_url/patient_model.glb',
        function (gltf) {
          scene.add(gltf.scene);
          gltf.scene.rotation.y += 0.01;  // Rotate the model for animation
          animate();
        },
        undefined,
        function (error) {
          console.error(error);
        }
      );

      camera.position.z = 5;
      function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      }
    </script>
    """, height=400)

    # Kondisi Saat Ini dalam Grafik 3D
    st.subheader("💎 Kondisi Pasien dalam Grafik 3D 💎")
    heart_rates = np.linspace(patient_data['current_conditions']['heart_rate'] - 5, 
                              patient_data['current_conditions']['heart_rate'], num=30)
    blood_pressures = np.linspace(patient_data['current_conditions']['blood_pressure'] - 5, 
                                  patient_data['current_conditions']['blood_pressure'], num=30)
    oxygen_levels = np.linspace(patient_data['current_conditions']['oxygen_level'] - 2, 
                                patient_data['current_conditions']['oxygen_level'], num=30)

    trace = go.Scatter3d(
        x=heart_rates,
        y=blood_pressures,
        z=oxygen_levels,
        mode='lines+markers',
        marker=dict(size=6, color='rgb(0, 255, 255)', opacity=0.8, line=dict(width=2, color='rgb(255, 255, 255)')),
        line=dict(color='rgb(255, 20, 147)', width=4)
    )

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='💙 Heart Rate (BPM)', gridcolor="#d1d1d1", showbackground=True, backgroundcolor="#0e0b16"),
            yaxis=dict(title='💜 Blood Pressure (mmHg)', gridcolor="#d1d1d1", showbackground=True, backgroundcolor="#1b1a1f"),
            zaxis=dict(title='💚 Oxygen Level (%)', gridcolor="#d1d1d1", showbackground=True, backgroundcolor="#13131e")
        ),
        paper_bgcolor="#0e0b16",
        font=dict(color="#A9F1FF", family="Courier New"),
        margin=dict(l=0, r=0, b=0, t=50),
        title=f"<b>Patient ID:</b> {patient_data['patient_id']} | <b>Risk Score:</b> {patient_data['current_conditions']['risk_score']}",
    )

    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

    # Panel Informasi Lainnya
    st.subheader("📊 Statistik Harian dan Kesehatan Pasien")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Detak Jantung Rata-rata", f"{patient_data['daily_stats']['avg_heart_rate']} BPM")
        st.metric("Langkah Harian", f"{patient_data['daily_stats']['steps_count']}")
    with col2:
        st.metric("Tekanan Darah Rata-rata", patient_data['daily_stats']['avg_blood_pressure'])
        st.metric("Kalori Terbakar", f"{patient_data['daily_stats']['calories_burned']} kcal")
    with col3:
        st.metric("Jam Tidur", f"{patient_data['daily_stats']['sleep_hours']} jam")
        st.metric("Durasi Olahraga", f"{patient_data['daily_stats']['exercise_duration']} menit")

else:
    st.error("Data pasien tidak ditemukan.")
