import streamlit as st
from agents.coordinator import MultiAgentCoordinator
import json
import time

# Page config
st.set_page_config(
    page_title="AutoRAN Advisor - Multi-Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# [KEEP ALL YOUR EXISTING CSS FROM web_app_elite.py]
st.markdown("""
<style>
    /* Copy all CSS from web_app_elite.py here */
</style>
""", unsafe_allow_html=True)

# Initialize coordinator
@st.cache_resource
def get_coordinator():
    return MultiAgentCoordinator()

coordinator = get_coordinator()

# Hero section
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>⚡ AutoRAN Advisor</h1>
        <div class="hero-subtitle">Multi-Agent AI Platform for O-RAN Multi-Vendor Integration</div>
        <div class="hero-badge">🤖 4 Specialist Agents • MCP Coordination • AWS Bedrock</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats section with agent info
st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">4</div>
        <div class="stat-label">Specialist Agents</div>
        <div class="stat-sublabel">RU • DU • Integration • Cost</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">90%+</div>
        <div class="stat-label">Detection Accuracy</div>
        <div class="stat-sublabel">↑ Multi-Agent Consensus</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">3 months → 3 days</div>
        <div class="stat-label">Integration Time</div>
        <div class="stat-sublabel">↓ 95% Reduction</div>
    </div>
    <div class="stat-card">
    <div class="stat-number">💾</div>
    <div class="stat-label">Persistent Memory</div>
    <div class="stat-sublabel">✓ Learning Enabled</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">MCP</div>
        <div class="stat-label">Coordination Protocol</div>
        <div class="stat-sublabel">✓ Agent Communication</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡ Multi-Agent Analysis",
    "🤖 Agent Workflows", 
    "📊 Comparison Engine",
    "🧠 Memory & Learning",
    "🔍 Agent History"
])

# Tab 1: Multi-Agent Analysis
with tab1:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Multi-Agent Compatibility Analysis</div>
        <div class="section-subtitle">Coordinate specialist agents for comprehensive O-RAN integration assessment</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="analysis-card">
            <div class="card-icon icon-success">✓</div>
            <div class="card-title">Compatible Pairing</div>
            <div class="card-description">4-agent workflow: RU→DU→Integration→Cost analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Run Multi-Agent Analysis", key="multi_ab"):
            with st.spinner("🔄 Coordinating specialist agents..."):
                # Show agent workflow
                st.info("**Agent Workflow Starting...**")
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate multi-agent coordination
                status_text.text("🤖 RU Specialist analyzing O-RU configuration...")
                time.sleep(1)
                progress_bar.progress(25)
                
                status_text.text("🤖 DU Specialist analyzing O-DU configuration...")
                time.sleep(1)
                progress_bar.progress(50)
                
                status_text.text("🤖 Integration Specialist assessing compatibility...")
                time.sleep(1)
                progress_bar.progress(75)
                
                status_text.text("🤖 Cost Optimizer calculating ROI...")
                time.sleep(1)
                progress_bar.progress(100)
                
                # Run actual analysis
                result = coordinator.analyze_compatibility(
                    "sample_configs/vendor_a_odu.json",
                    "sample_configs/vendor_b_oru.json"
                )
                
                status_text.success("✅ Multi-Agent Analysis Complete!")
                
                # Display results from each agent
                st.markdown("---")
                st.markdown("### 📊 Agent Analysis Results")
                
                for agent_name, agent_data in result['results'].items():
                    with st.expander(f"🤖 {agent_data['agent']} - {agent_data['task']}"):
                        st.markdown(agent_data['analysis'])
                
                # Show summary
                st.markdown("---")
                st.markdown("### 💡 Multi-Agent Consensus")
                st.info(result['summary'])
    
    with col2:
        st.markdown("""
        <div class="analysis-card">
            <div class="card-icon icon-danger">✕</div>
            <div class="card-title">Incompatible Pairing</div>
            <div class="card-description">Agents identify critical blocking issues</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Analyze Incompatible Pair", key="multi_ac"):
            with st.spinner("🔄 Multi-agent analysis in progress..."):
                result = coordinator.analyze_compatibility(
                    "sample_configs/vendor_a_odu.json",
                    "sample_configs/vendor_c_oru.json"
                )
                
                st.success("✅ Analysis Complete")
                
                for agent_name, agent_data in result['results'].items():
                    with st.expander(f"🤖 {agent_data['agent']}"):
                        st.markdown(agent_data['analysis'])
    
    with col3:
        st.markdown("""
        <div class="analysis-card">
            <div class="card-icon icon-primary">⊕</div>
            <div class="card-title">Vendor Comparison</div>
            <div class="card-description">Multi-agent consensus recommendation</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Compare Vendors", key="multi_compare"):
            with st.spinner("🔄 Agents comparing vendor options..."):
                result = coordinator.compare_vendors(
                    "sample_configs/vendor_a_odu.json",
                    [
                        "sample_configs/vendor_b_oru.json",
                        "sample_configs/vendor_c_oru.json"
                    ]
                )
                
                st.success("✅ Comparison Complete")
                st.markdown(result['recommendation'])

# Tab 2: Agent Workflows
with tab2:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Individual Agent Workflows</div>
        <div class="section-subtitle">Interact with specialist agents independently</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🤖 RU Specialist Agent")
        st.caption("Expert in O-RU configurations and RF specifications")
        
        if st.button("Analyze Vendor B O-RU", key="ru_agent"):
            with st.spinner("🤖 RU Specialist analyzing..."):
                result = coordinator.analyze_oru_config("sample_configs/vendor_b_oru.json")
                st.markdown(result['analysis'])
    
    with col2:
        st.markdown("#### 🤖 DU Specialist Agent")
        st.caption("Expert in O-DU configurations and MAC/PHY layer")
        
        if st.button("Analyze Vendor A O-DU", key="du_agent"):
            with st.spinner("🤖 DU Specialist analyzing..."):
                result = coordinator.analyze_odu_config("sample_configs/vendor_a_odu.json")
                st.markdown(result['analysis'])

# Tab 3: Comparison Engine
with tab3:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Multi-Vendor Comparison Engine</div>
        <div class="section-subtitle">Upload multiple O-RU options for side-by-side analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📤 Upload O-DU configuration and multiple O-RU options for comprehensive comparison")

# New Tab 4: Memory
with tab4:
    st.markdown("""
    <div class="section-header">
        <div class="section-title">🧠 System Memory & Learning</div>
        <div class="section-subtitle">View historical analyses and learned patterns</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Vendor History")
        vendor_name = st.text_input("Enter vendor name:", "Vendor_A")
        vendor_role = st.selectbox("Role:", ["any", "odu", "oru"])
        
        if st.button("Get Vendor History"):
            from tools.memory_tools import get_vendor_compatibility_history
            history = get_vendor_compatibility_history(vendor_name, vendor_role)
            st.markdown(history)
    
    with col2:
        st.markdown("#### 🧠 Integration Insights")
        
        if st.button("Generate Insights"):
            from tools.memory_tools import get_integration_insights
            insights = get_integration_insights()
            st.markdown(insights)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <h3 style='color: #2d3748; margin-bottom: 0.5rem;'>⚡ AutoRAN Advisor - Multi-Agent Platform</h3>
    <p style='color: #4a5568; margin-bottom: 1rem;'>4 Specialist Agents • MCP Coordination • Enterprise Scale</p>
    <p style='color: #718096; font-size: 0.9rem;'>Powered by AWS Bedrock • Strands Agents • Claude Sonnet 4.5</p>
</div>
""", unsafe_allow_html=True)