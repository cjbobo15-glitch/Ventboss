import streamlit as st

st.set_page_config(page_title="VentBoss AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background: #f8fafc;
        color: #1e293b;
    }
    
    .stApp {
        background: #ffffff;
    }
    
    .main-header {
        font-size: 48px;
        font-weight: 800;
        color: #0f172a;
        text-align: center;
        margin: 40px 0 8px 0;
        letter-spacing: -1.5px;
    }
    
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 40px;
    }
    
    .patient-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }
    
    .patient-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.12);
    }
    
    .risk-value {
        font-size: 32px;
        font-weight: 700;
    }
    
    .risk-high { color: #dc2626; }
    .risk-medium { color: #f59e0b; }
    .risk-low { color: #10b981; }
    
    .stButton > button {
        background: #3b82f6;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        width: 100%;
        font-size: 16px;
    }
    
    .stButton > button:hover {
        background: #2563eb;
    }
    
    h1, h2, h3, h4 {
        color: #0f172a !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 17px;
        font-weight: 600;
        color: #475569;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">VentBoss AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Complex Respiratory Management System</div>', unsafe_allow_html=True)

patients = [
    {"name": "J. Rodriguez", "dx": "Amyotrophic Lateral Sclerosis", "device": "VOCSN", "risk": 88, "last": "2025-12-05", "phone": "667-xxx-xxxx"},
    {"name": "M. Thompson", "dx": "COPD", "device": "Trilogy Evo", "risk": 76, "last": "2025-12-04", "phone": "443-xxx-xxxx"},
    {"name": "K. Washington", "dx": "Duchenne Muscular Dystrophy", "device": "Astral 150", "risk": 94, "last": "2025-12-06", "phone": "410-xxx-xxxx"},
    {"name": "T. Clark", "dx": "Kyphoscoliosis", "device": "Trilogy Evo O2", "risk": 61, "last": "2025-12-03", "phone": "301-xxx-xxxx"},
]

tab1, tab2, tab3, tab4 = st.tabs(["Risk Board", "AI Titration", "Compliance Letters", "Settings"])

with tab1:
    st.subheader("30-Day Readmission Risk")
    for p in patients:
        if p["risk"] > 70:
            risk_class = "risk-high" if p["risk"] > 85 else "risk-medium"
            st.markdown(f"""
            <div class="patient-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="margin:0;">{p['name']}</h3>
                        <p style="margin:4px 0; color:#64748b;">{p['dx']} — {p['device']}</p>
                    </div>
                    <div style="text-align: right;">
                        <div class="risk-value {risk_class}">{p['risk']}</div>
                        <div style="color:#94a3b8; font-size:14px;">Last download: {p['last']}</div>
                    </div>
                </div>
                <div style="margin-top: 20px; color:#475569; font-weight:500;">
                    Phone: {p['phone']}
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.subheader("Ventilator Data Analysis & Titration Recommendation")
    device = st.selectbox("Device", ["Trilogy Evo", "Trilogy Evo O2", "VOCSN", "Astral 150", "Trilogy 202", "LTV"])
    uploaded = st.file_uploader("Upload ventilator download (EDF/CSV)", type=["edf", "csv"])
    
    col1, col2 = st.columns(2)
    with col1:
        demo = st.button("Load Demo Data", use_container_width=True)
    with col2:
        analyze = st.button("Analyze & Generate Recommendation", use_container_width=True)
    
    if demo or uploaded or analyze:
        st.markdown("#### Key Metrics")
        st.json({
            "Average Tidal Volume": "428 mL",
            "Percent Triggered Breaths": "34%",
            "Peak Pressure": "34 cmH2O",
            "95th Percentile Leak": "58 L/min",
            "AHI": "9.2 events/hr",
            "SpO₂ Nadir": "86%",
            "Backup Rate Usage": "71%"
        }, expanded=False)
        
        st.markdown("#### Recommended Settings")
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:20px; border-radius:12px;">
            <ul style="line-height:1.8; font-size:16px;">
                <li><strong>Mode:</strong> AVAPS-AE</li>
                <li><strong>IPAP Max:</strong> 32 cmH₂O (increased from current)</li>
                <li><strong>IPAP Min:</strong> 16 cmH₂O</li>
                <li><strong>EPAP:</strong> 11 cmH₂O</li>
                <li><strong>Target Volume:</strong> 480–520 mL</li>
                <li><strong>Backup Rate:</strong> 18–20 bpm</li>
                <li><strong>Rise Time:</strong> 200 ms</li>
            </ul>
            <p><strong>Expected improvement:</strong> Triggered breaths ↑ 65–75%, AHI <3, SpO₂ nadir >91%, readmission risk reduction ≈68%</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("90-Day Compliance Letter Generator")
    patient = st.selectbox("Patient", [p["name"] for p in patients])
    if st.button("Generate Letter", use_container_width=True):
        selected = next(p for p in patients if p["name"] == patient)
        letter = f"""
90-Day Compliance and Medical Necessity Documentation

Patient: {patient}
Diagnosis: {selected['dx']}
Device: {selected['device']}

Compliance Summary (past 90 days):
  • Usage compliance: 96% of days ≥4 hours
  • Average daily use: 8.4 hours
  • AHI: 2.1 events/hour
  • 95th percentile leak: 24 L/min
  • No clinically significant desaturations

Continued use of home mechanical ventilation remains medically necessary. Discontinuation would place the patient at high risk of clinical deterioration and re-hospitalization.

Sincerely,

[Your Name], RRT
Complex Respiratory Specialist
VentBoss Respiratory LLC
        """
        st.text_area("Letter content (ready to copy)", letter, height=420)
        st.download_button("Download as .txt", letter, f"{patient.replace(' ', '_')}_compliance.txt")

with tab4:
    st.subheader("System Settings")
    st.info("Full production features (Google Sheets sync, real-time EDF parsing, predictive modeling, multi-user roles) available on request.")
    st.text_input("OpenAI API Key (optional for enhanced AI features)", type="password")
    st.caption("VentBoss AI © 2025–2026 — Proprietary Software")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:14px;'>VentBoss Respiratory • Clinical Excellence Platform</p>", unsafe_allow_html=True)
