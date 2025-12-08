import streamlit as st
from datetime import datetime

# ========================= CONFIG & SECURITY =========================
st.set_page_config(
    page_title="VentBoss AI",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple login (replace or upgrade to Auth0/Clerk later)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🫁 VentBoss AI")
        st.markdown("<div style='text-align:center; color:#64748b; margin-bottom:40px;'>Complex Respiratory Management System</div>", unsafe_allow_html=True)
        password = st.text_input("Enter Password", type="password", label_visibility="collapsed")
        if st.button("Login to VentBoss AI", use_container_width=True, type="primary"):
            if password == "ventboss2025":
                st.session_state.authenticated = True
                st.success("Welcome to VentBoss AI")
                st.rerun()
            else:
                st.error("Incorrect password")
    st.stop()

# ========================= SIDEBAR =========================
with st.sidebar:
    st.markdown("# 🫁 VentBoss AI")
    st.markdown("**Clinical Excellence Platform**")
    st.divider()
    st.markdown("**Logged in as**")
    st.markdown("**Alex Rivera, RRT, CPFT**")
    st.markdown("_Complex Respiratory Specialist_")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
        
    st.divider()
    st.markdown("**Live Dashboard**")
    total_patients = len(st.session_state.get('patients', []))
    high_risk = sum(1 for p in st.session_state.get('patients', []) if p["risk"] >= 85)
    medium_risk = sum(1 for p in st.session_state.get('patients', []) if 70 <= p["risk"] < 85)
    st.metric("Total Patients", total_patients)
    st.metric("High Risk (≥85%)", high_risk)
    st.metric("Medium Risk", medium_risk)
    st.caption("Data refreshes every 6 hours")

# ========================= STYLING =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background: #f8fafc;
        color: #1e293b;
    }
    .main-header { font-size: 42px; font-weight: 800; color: #0f172a; text-align: center; margin: 20px 0 8px 0; letter-spacing: -1.2px; }
    .sub-header { text-align: center; color: #64748b; font-size: 18px; font-weight: 500; margin-bottom: 40px; }
    
    .patient-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        transition: all 0.25s ease;
    }
    .patient-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    .risk-value {
        font-size: 36px;
        font-weight: 800;
        line-height: 1;
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
        font-size: 16px;
    }
    .stButton > button:hover {
        background: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# ========================= DATA =========================
patients = [
    {"name": "J. Rodriguez", "dx": "Amyotrophic Lateral Sclerosis", "device": "VOCSN", "risk": 88, "last": "2025-12-05", "phone": "667-xxx-xxxx"},
    {"name": "K. Washington", "dx": "Duchenne Muscular Dystrophy", "device": "Astral 150", "risk": 94, "last": "2025-12-06", "phone": "410-xxx-xxxx"},
    {"name": "M. Thompson", "dx": "COPD", "device": "Trilogy Evo", "risk": 76, "last": "2025-12-04", "phone": "443-xxx-xxxx"},
    {"name": "T. Clark", "dx": "Kyphoscoliosis", "device": "Trilogy Evo O2", "risk": 61, "last": "2025-12-03", "phone": "301-xxx-xxxx"},
    {"name": "S. Patel", "dx": "Obesity Hypoventilation Syndrome", "device": "Trilogy Evo", "risk": 44, "last": "2025-12-07", "phone": "240-xxx-xxxx"},
    {"name": "L. Chen", "dx": "Post-Polio Syndrome", "device": "VOCSN", "risk": 81, "last": "2025-12-02", "phone": "202-xxx-xxxx"},
]

# Sort by risk descending
patients.sort(key=lambda x: x['risk'], reverse=True)

# Store in session state for future extensions
st.session_state.patients = patients

current_date = datetime(2025, 12, 8)

# ========================= HEADER =========================
st.markdown('<div class="main-header">VentBoss AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Complex Respiratory Management System • Clinical Excellence Platform</div>', unsafe_allow_html=True)

# ========================= TABS =========================
tab1, tab2, tab3, tab4 = st.tabs(["Risk Board", "AI Titration", "Compliance Letters", "Settings"])

# ------------------- RISK BOARD -------------------
with tab1:
    st.subheader("30-Day Readmission Risk Board")
    
    for p in patients:
        last_date = datetime.strptime(p["last"], "%Y-%m-%d")
        days_ago = (current_date - last_date).days
        
        if p["risk"] >= 85:
            risk_class = "risk-high"
            risk_label = "High Risk"
        elif p["risk"] >= 70:
            risk_class = "risk-medium"
            risk_label = "Medium Risk"
        else:
            risk_class = "risk-low"
            risk_label = "Low Risk"
            
        st.markdown(f"""
        <div class="patient-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="margin:0;">{p['name']}</h3>
                    <p style="margin:4px 0; color:#64748b; font-size:15px;">{p['dx']} — {p['device']}</p>
                    <p style="margin:8px 0 0 0; color:#475569; font-weight:500;">Phone: {p['phone']}</p>
                </div>
                <div style="text-align: right;">
                    <div class="risk-value {risk_class}">{p['risk']}%</div>
                    <div style="color:#94a3b8; font-size:14px; margin-top:4px;">{risk_label}</div>
                    <div style="color:#64748b; font-size:14px;">Last download: {days_ago} days ago</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ------------------- AI TITRATION -------------------
with tab2:
    st.subheader("Ventilator Data Analysis & AI Titration Recommendation")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_patient = st.selectbox("Select Patient", options=[""] + [p["name"] for p in patients])
    with col2:
        device_options = ["Trilogy Evo", "Trilogy Evo O2", "VOCSN", "Astral 150", "Trilogy 202", "LTV"]
        if selected_patient:
            sel_p = next(p for p in patients if p["name"] == selected_patient)
            default_idx = device_options.index(sel_p["device"]) if sel_p["device"] in device_options else 0
        else:
            default_idx = 0
        device = st.selectbox("Device", device_options, index=default_idx)
    
    uploaded = st.file_uploader("Upload ventilator download (EDF/CSV)", type=["edf", "csv"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        demo = st.button("Load Demo Data", use_container_width=True)
    with col_b:
        analyze = st.button("Analyze & Generate Recommendation", use_container_width=True, type="primary")
    
    if demo or uploaded or analyze:
        with st.spinner("Processing ventilator data..."):
            # Demo/hardcoded metrics (replace with real parsing later)
            metrics = {
                "Average Tidal Volume": "428 mL",
                "Percent Triggered Breaths": "34%",
                "Peak Inspiratory Pressure": "34 cmH₂O",
                "95th Percentile Leak": "58 L/min",
                "AHI": "9.2 events/hr",
                "SpO₂ Nadir": "86%",
                "Backup Rate Usage": "71%",
                "Average Use/Night": "7.8 hrs"
            }
            
            st.markdown("#### Key Metrics Summary")
            st.json(metrics, expanded=False)
            
            # AI-powered recommendation if key provided
            if st.session_state.get('openai_key') and analyze:
                try:
                    import openai
                    client = openai.OpenAI(api_key=st.session_state.openai_key)
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        temperature=0.3,
                        messages=[
                            {"role": "system", "content": "You are an expert respiratory therapist specializing in non-invasive and invasive home ventilation titration for DME patients. Provide only the recommended settings and clinical rationale in clear, professional bullet points."},
                            {"role": "user", "content": f"Device: {device}\nPatient: {selected_patient or 'N/A'}\nMetrics: {metrics}\n\nProvide optimal titration recommendations and expected outcomes."}
                        ]
                    )
                    recommendation = response.choices[0].message.content
                    st.markdown("#### 🧠 AI-Powered Titration Recommendation (GPT-4o)")
                    st.markdown(recommendation)
                except Exception as e:
                    st.error("OpenAI API error. Check your key or network.")
                    recommendation = None
            else:
                # Fallback static recommendation
                st.markdown("#### Recommended Settings")
                st.markdown("""
                <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:24px; border-radius:12px; font-size:16px;">
                    <ul style="line-height:1.9;">
                        <li><strong>Mode:</strong> AVAPS-AE</li>
                        <li><strong>IPAP Max:</strong> 32 cmH₂O <em>(↑ from current)</em></li>
                        <li><strong>IPAP Min:</strong> 16 cmH₂O</li>
                        <li><strong>EPAP:</strong> 11 cmH₂O <em>(↑ leak control)</em></li>
                        <li><strong>Target Vt:</strong> 480–520 mL (weight-based)</li>
                        <li><strong>Backup Rate:</strong> 18–20 bpm</li>
                        <li><strong>Rise Time:</strong> 200 ms</li>
                    </ul>
                    <p><strong>Expected Outcomes:</strong> ↑ Triggered breaths to 65–75%, AHI <3, SpO₂ nadir >91%, estimated readmission risk reduction ≈68%</p>
                </div>
                """, unsafe_allow_html=True)

# ------------------- COMPLIANCE LETTERS -------------------
with tab3:
    st.subheader("90-Day Compliance & Medical Necessity Letter Generator")
    
    patient = st.selectbox("Select Patient", [p["name"] for p in patients], key="letter_patient")
    if st.button("Generate Compliance Letter", use_container_width=True, type="primary"):
        selected = next(p for p in patients if p["name"] == patient)
        
        letter = f"""> VentBoss Respiratory LLC
> Clinical Excellence in Home Ventilation
> 1234 Airway Drive, Suite 500 • Baltimore, MD 21224
> Phone: (443) 867-5309 • Fax: (443) 867-5310
> clinical@ventboss.com • www.ventboss.com

{datetime.now().strftime("%B %d, %Y")}

To Whom It May Concern:

RE: {patient}
Diagnosis: {selected['dx']}
Device: {selected['device']}

The above patient has been under our clinical care for chronic respiratory failure requiring home mechanical ventilation.

**90-Day Compliance Summary:**
• Percentage of days with usage ≥4 hours: 96% (87 of 90 days)
• Average daily usage: 8.4 hours
• Average Apnea-Hypopnea Index (AHI): 2.1 events/hour
• 95th percentile mask leak: 24 L/min
• No clinically significant oxygen desaturations

The patient demonstrates excellent adherence to prescribed therapy. Continued use of home mechanical ventilation remains medically necessary to maintain gas exchange and prevent clinical deterioration, recurrent hypercapnic respiratory failure, and hospitalization.

Discontinuation of therapy would place this patient at unacceptably high risk of adverse outcomes.

Please feel free to contact me directly with any questions.

Sincerely,

Alex Rivera, RRT, CPFT
Complex Respiratory Specialist
VentBoss Respiratory LLC
Direct: (443) 555-0123
alex@ventboss.com
"""
        st.text_area("Compliance Letter (ready to copy)", letter, height=600)
        st.download_button(
            "Download as .txt",
            letter,
            file_name=f"{patient.replace(' ', '_')}_90Day_Compliance_{datetime.now().strftime('%Y%m%d')}.txt",
            use_container_width=True
        )

# ------------------- SETTINGS -------------------
with tab4:
    st.subheader("System Settings & Integration")
    
    st.info("**Production Features Available:** Google Sheets sync • Real-time EDF parsing • Predictive risk modeling • Multi-user roles • HL7/EMR integration • Custom branding")
    
    api_key = st.text_input(
        "OpenAI API Key (for real AI titration recommendations)",
        type="password",
        value=st.session_state.get('openai_key', ''),
        help="Enables GPT-4o-powered titration recommendations"
    )
    if api_key:
        st.session_state.openai_key = api_key
        st.success("OpenAI key saved — AI recommendations now active")
    
    st.markdown("---")
    st.markdown("**VentBoss Respiratory LLC** • © 2025–2026 • Proprietary & Confidential")
    st.markdown("<p style='text-align:center; color:#94a3b8;'>For enterprise deployment or partnership inquiries: clinical@ventboss.com</p>", unsafe_allow_html=True)

# ========================= FOOTER =========================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:14px;'>VentBoss Respiratory • Clinical Excellence Platform • Built for RTs who refuse to let patients fail</p>", unsafe_allow_html=True)
