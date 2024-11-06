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
st.set_page_config(page_title="3D Holographic Patient Monitoring", layout="wide")
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
    # Informasi Dasar Pasien
    st.subheader(f"🧑‍⚕️ Informasi Pasien: {patient_data['name']}")
    st.write(f"**ID Pasien**: {patient_data['patient_id']}")
    st.write(f"**Usia**: {patient_data['age']} tahun")
    st.write(f"**Jenis Kelamin**: {patient_data['gender']}")
    
    # Riwayat Kesehatan Pasien
    st.subheader("📋 Riwayat Kesehatan Pasien")
    st.write("**Diabetes**: ", "Ya" if patient_data["medical_history"]["diabetes"] else "Tidak")
    st.write("**Hipertensi**: ", "Ya" if patient_data["medical_history"]["hypertension"] else "Tidak")
    st.write("**Riwayat Merokok**: ", patient_data["medical_history"]["smoking_history"])
    st.write("**Riwayat Keluarga**: ", patient_data["medical_history"]["family_history"])

    # Kondisi Saat Ini dalam Grafik 3D dengan Efek Neon dan Trail
    st.subheader("🔮 Kondisi Pasien dalam Grafik 3D Holografis 🔮")
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

    # Render grafik 3D
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, use_container_width=True)

    # Statistik Harian Pasien
    st.subheader("📊 Statistik Harian Pasien")
    st.write(f"- **Detak Jantung Rata-rata**: {patient_data['daily_stats']['avg_heart_rate']} BPM")
    st.write(f"- **Tekanan Darah Rata-rata**: {patient_data['daily_stats']['avg_blood_pressure']}")
    st.write(f"- **Jumlah Langkah**: {patient_data['daily_stats']['steps_count']}")
    st.write(f"- **Kalori Terbakar**: {patient_data['daily_stats']['calories_burned']} kcal")
    st.write(f"- **Jam Tidur**: {patient_data['daily_stats']['sleep_hours']} jam")
    st.write(f"- **Durasi Olahraga**: {patient_data['daily_stats']['exercise_duration']} menit")

    # Rekomendasi Nutrisi dan Rencana Rehabilitasi
    st.subheader("🍎 Rekomendasi Nutrisi")
    st.markdown(f"<div style='color:#00FFD1;font-size:20px;font-weight:bold;'>{patient_data['recommendations']['nutritional_advice']}</div>", unsafe_allow_html=True)

    st.subheader("🏃‍♂️ Rencana Rehabilitasi Medik")
    st.markdown(f"<div style='color:#FF00FF;font-size:20px;font-weight:bold;'>{patient_data['recommendations']['rehabilitation_plan']}</div>", unsafe_allow_html=True)

    # Peringatan Kesehatan Terbaru
    st.subheader("🚨 Peringatan Kesehatan Terbaru 🚨")
    for alert in patient_data["alerts"]["recent_alerts"]:
        st.write(f"- **Tanggal**: {alert['date']} | **Peringatan**: {alert['alert']}")
    st.write(f"**Pemeriksaan Terakhir**: {patient_data['alerts']['last_checkup']}")

    # Faktor Risiko Pasien
    st.subheader("⚠️ Faktor Risiko Pasien")
    st.write(f"- **Risiko Merokok**: {patient_data['risk_factors']['smoking_risk']}")
    st.write(f"- **Risiko Diabetes**: {patient_data['risk_factors']['diabetes_risk']}")
    st.write(f"- **Risiko Penyakit Jantung**: {patient_data['risk_factors']['heart_disease_risk']}")
    st.write(f"- **Risiko Aktivitas Fisik**: {patient_data['risk_factors']['activity_risk']}")

else:
    st.error("Data pasien tidak ditemukan.")
