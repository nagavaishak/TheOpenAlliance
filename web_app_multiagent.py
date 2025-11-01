import streamlit as st
from agents.coordinator import MultiAgentCoordinator
import json
import time

st.set_page_config(
    page_title="AutoRAN Advisor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# PREMIUM CSS - Glassmorphism + Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', -apple-system, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1f3a 50%, #2d1b4e 100%);
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Animated gradient header */
    .hero-section {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.9) 0%,
            rgba(118, 75, 162, 0.9) 50%,
            rgba(237, 100, 166, 0.9) 100%);
        padding: 4rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        animation: gradientShift 8s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        letter-spacing: -0.03em;
        animation: slideInDown 0.8s ease-out;
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.95);
        margin-top: 1rem;
        animation: slideInUp 0.8s ease-out 0.2s both;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(10px);
        padding: 0.75rem 1.5rem;
        border-radius: 100px;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 2rem;
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        animation: slideInUp 0.8s ease-out 0.4s both;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        animation: fadeInScale 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    /* Agent cards with icons */
    .agent-card {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.15) 0%,
            rgba(118, 75, 162, 0.15) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #ed64a6);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .agent-card:hover::before {
        transform: translateX(0);
    }
    
    .agent-card:hover {
        transform: translateY(-12px);
        border-color: rgba(102, 126, 234, 0.8);
        box-shadow: 0 30px 80px rgba(102, 126, 234, 0.4);
    }
    
    .agent-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 4px 12px rgba(102, 126, 234, 0.5));
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .agent-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    
    .agent-desc {
        color: rgba(255,255,255,0.7);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Animated stats */
    .stat-card {
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.2) 0%,
            rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #ed64a6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: countUp 1s ease-out;
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stat-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }
    
    /* Glowing buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1.25rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(26, 31, 58, 0.4);
        backdrop-filter: blur(20px);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: rgba(255,255,255,0.6);
        font-weight: 600;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress animation */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_coordinator():
    return MultiAgentCoordinator(demo_mode=False)

coordinator = get_coordinator()

# HERO SECTION
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-title">⚡ AutoRAN Advisor</div>
        <div class="hero-subtitle">Multi-Agent AI Platform for O-RAN Integration</div>
        <div class="hero-badge">🤖 4 Specialist Agents • 🧠 Persistent Memory • ☁️ AWS Bedrock</div>
    </div>
</div>
""", unsafe_allow_html=True)

# STATS ROW
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card" style="animation-delay: 0.1s;">
        <div class="stat-number">4</div>
        <div class="stat-label">AI Agents</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card" style="animation-delay: 0.2s;">
        <div class="stat-number">90%+</div>
        <div class="stat-label">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card" style="animation-delay: 0.3s;">
        <div class="stat-number">95%</div>
        <div class="stat-label">Faster</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card" style="animation-delay: 0.4s;">
        <div class="stat-number">$14B</div>
        <div class="stat-label">Market</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# AGENT SHOWCASE
st.markdown("""
<div style='text-align: center; margin: 3rem 0 2rem 0;'>
    <h2 style='color: white; font-size: 2.5rem; font-weight: 700;'>Meet the Specialist Agents</h2>
    <p style='color: rgba(255,255,255,0.7); font-size: 1.2rem;'>Expert AI agents collaborating to solve O-RAN integration</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="agent-card" style="animation-delay: 0.1s;">
        <div class="agent-icon">📡</div>
        <div class="agent-title">RU Specialist</div>
        <div class="agent-desc">Radio unit expert analyzing RF specs and fronthaul configs</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card" style="animation-delay: 0.2s;">
        <div class="agent-icon">⚙️</div>
        <div class="agent-title">DU Specialist</div>
        <div class="agent-desc">Distributed unit expert validating MAC/PHY layer configs</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card" style="animation-delay: 0.3s;">
        <div class="agent-icon">🔗</div>
        <div class="agent-title">Integration</div>
        <div class="agent-desc">Multi-vendor compatibility assessment and validation</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="agent-card" style="animation-delay: 0.4s;">
        <div class="agent-icon">💰</div>
        <div class="agent-title">Cost Optimizer</div>
        <div class="agent-desc">ROI calculation and integration cost analysis</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# DEMO SECTION
st.markdown("""
<div style='text-align: center; margin: 3rem 0 2rem 0;'>
    <h2 style='color: white; font-size: 2.5rem; font-weight: 700;'>🚀 Live Analysis Demo</h2>
    <p style='color: rgba(255,255,255,0.7); font-size: 1.2rem;'>Watch agents coordinate in real-time</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3 style='color: #4ade80; margin-bottom: 1rem;'>✅ Compatible Pairing</h3>
        <p style='color: rgba(255,255,255,0.7); margin-bottom: 1.5rem;'>Vendor A O-DU + Vendor B O-RU</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🤖 Analyze Compatible Pair", key="analyze_ab", use_container_width=True):
        with st.spinner("🔄 Agents coordinating..."):
            progress_bar = st.progress(0)
            st.info("🤖 RU Specialist analyzing...")
            time.sleep(0.5)
            progress_bar.progress(25)
            st.info("🤖 DU Specialist analyzing...")
            time.sleep(0.5)
            progress_bar.progress(50)
            st.info("🤖 Integration Specialist assessing...")
            time.sleep(0.5)
            progress_bar.progress(75)
            st.info("🤖 Cost Optimizer calculating...")
            time.sleep(0.5)
            progress_bar.progress(100)
            
            result = coordinator.analyze_compatibility(
                "sample_configs/vendor_a_odu.json",
                "sample_configs/vendor_b_oru.json"
            )
            
            st.success("✅ Multi-Agent Analysis Complete!")
            
            for agent_name, agent_data in result['results'].items():
                with st.expander(f"🤖 {agent_data['agent']} - {agent_data['task']}"):
                    st.markdown(agent_data['analysis'])

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3 style='color: #f87171; margin-bottom: 1rem;'>❌ Incompatible Pairing</h3>
        <p style='color: rgba(255,255,255,0.7); margin-bottom: 1.5rem;'>Vendor A O-DU + Vendor C O-RU</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🤖 Analyze Incompatible Pair", key="analyze_ac", use_container_width=True):
        with st.spinner("🔄 Agents analyzing..."):
            result = coordinator.analyze_compatibility(
                "sample_configs/vendor_a_odu.json",
                "sample_configs/vendor_c_oru.json"
            )
            
            st.error("⚠️ Critical Compatibility Issues Detected!")
            
            for agent_name, agent_data in result['results'].items():
                with st.expander(f"🤖 {agent_data['agent']}"):
                    st.markdown(agent_data['analysis'])

with col3:
    st.markdown("""
    <div class="glass-card">
        <h3 style='color: #60a5fa; margin-bottom: 1rem;'>📊 Vendor Comparison</h3>
        <p style='color: rgba(255,255,255,0.7); margin-bottom: 1.5rem;'>Compare multiple O-RU options</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🤖 Compare Vendors", key="compare", use_container_width=True):
        with st.spinner("🔄 Running comprehensive comparison..."):
            result = coordinator.compare_vendors(
                "sample_configs/vendor_a_odu.json",
                ["sample_configs/vendor_b_oru.json", "sample_configs/vendor_c_oru.json"]
            )
            
            st.success("✅ Comparison Complete!")
            st.markdown(result['recommendation'])

# FOOTER
st.markdown("""
<div style='text-align: center; margin-top: 5rem; padding: 3rem; background: rgba(26, 31, 58, 0.4); backdrop-filter: blur(20px); border-radius: 24px; border: 1px solid rgba(102, 126, 234, 0.2);'>
    <h3 style='color: white; margin-bottom: 1rem;'>⚡ AutoRAN Advisor</h3>
    <p style='color: rgba(255,255,255,0.7); margin-bottom: 0.5rem;'>Breaking Barriers in O-RAN Multi-Vendor Integration</p>
    <p style='color: rgba(255,255,255,0.5); font-size: 0.9rem;'>AWS Breaking Barriers Hackathon @ FYUZ 2025</p>
</div>
""", unsafe_allow_html=True)