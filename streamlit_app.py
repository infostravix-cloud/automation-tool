# streamlit_app.py
import streamlit as st
import threading
import automation  # Aapki core automation.py file ko import karega
from datetime import datetime

# Page configuration and styling
st.set_page_config(
    page_title="Zoom Automation - Anti-CAPTCHA",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
    .main-title {
        color: #667eea;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
        font-size: 14px;
    }
    .feature-box {
        background-color: #e8f4f8;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 4px;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        font-size: 13px;
        color: #856404;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_gradient=True)

# UI Header Section
st.markdown('<div class="main-title">🤖 Zoom Automation</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Anti-CAPTCHA Version - B.Tech CSE Project</div>', unsafe_allow_html=True)

# Features Information Box
st.markdown("""
<div class="feature-box">
    <strong>🛡️ Anti-CAPTCHA Features:</strong>
    <ul style="margin-left: 20px; margin-top: 5px;">
        <li>✅ Undetected ChromeDriver Setup</li>
        <li>✅ Human-like typing behaviors</li>
        <li>✅ Custom delay intervals between actions</li>
        <li>✅ Dynamic Indian profile generation</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Warnings/Notes Box
st.markdown("""
<div class="warning-box">
    <strong>⚠️ Important Notes:</strong><br>
    • Educational purposes only. Use responsibly with authorization.<br>
    • Cloud deployment runs in optimized Headless mode to fit container allocation.<br>
    • Automated pacing adds a safe 10-second buffer delay between sequential bots.
</div>
""", unsafe_allow_html=True)

# Interactive Form Settings
with st.form("automation_form", clear_on_submit=False):
    st.subheader("Configuration Panel")
    
    number = st.number_input(
        "Number of Participants:", 
        min_value=1, 
        max_value=1000, 
        value=1,
        help="Maximum 1000 bots can run sequentially to respect RAM boundaries."
    )
    
    meeting_code = st.text_input(
        "Meeting Code:", 
        placeholder="e.g., 7372825415",
        help="Provide the 10-11 digit Zoom Meeting ID."
    )
    
    passcode = st.text_input(
        "Passcode:", 
        placeholder="e.g., stravix",
        type="default",
        help="Meeting password (case-sensitive)."
    )
    
    end_time = st.text_input(
        "End Time (HHMM):", 
        placeholder="e.g., 2000",
        max_chars=4,
        help="Provide 24-hour format (e.g., 1430 for 2:30 PM)."
    )
    
    # Form Submit Button
    submit_btn = st.form_submit_button("🚀 Start Automation Pipeline")

# Logic Handling on Click
if submit_btn:
    # Basic Validations
    if not meeting_code or not passcode or not end_time:
        st.error("❌ Mismatch: All fields (Meeting Code, Passcode, End Time) are strictly required!")
    elif len(end_time) != 4 or not end_time.isdigit():
        st.error("❌ Validation Error: End Time format must be exactly 4 digits (HHMM)!")
    else:
        # User Feedback Notification
        st.info(f"⏳ Spawning an isolated backend thread to handle {number} bots safely...")
        
        # Async invocation without freezing or timing out the user interface
        automation_thread = threading.Thread(
            target=automation.run_zoom_automation,
            args=(int(number), str(meeting_code), str(passcode), str(end_time)),
            daemon=True
        )
        automation_thread.start()
        
        # Success Alert Box
        st.success(f"✅ Pipeline triggered successfully! Bots will start joining shortly.")
        st.balloons()
        
        # Terminal Logs instruction layout
        st.markdown("""
        ---
        📊 **Live Execution Context:** *Threads have safely decoupled from the UI. You can monitor the progress, proxy logs, and join logs live in the **Streamlit Cloud Web Console Logs view** (bottom-right flyout panel).*
        """)