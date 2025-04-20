import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# PAGE CONFIG
st.set_page_config(page_title="SilentFlag Dashboard", layout="wide")

# LOAD STORE
file_path = "data/user_logs.csv"

try:
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour

    # FLAG ANOMALIES
    df['risk_level'] = df.apply(lambda row: "⚠️ High" if row['downloads'] > 30 or row['hour'] < 6 else "✅ Normal", axis=1)

    # SIDEBAR (LEFT)
    with st.sidebar:
        st.title("📊 SilentFlag Panel")
        st.subheader("🔎 Filters")
        selected_user = st.selectbox("Select User", options=["All"] + sorted(df['username'].unique().tolist()))
        st.markdown("—" * 10)

        total_logs = len(df)
        total_flags = len(df[df['risk_level'] == "⚠️ High"])

        st.metric("📂 Total Logs", total_logs)
        st.metric("🚨 Flags Detected", total_flags)
        st.markdown("—" * 10)

        if st.button("💾 Save Anomalies"):
            df[df['risk_level'] == "⚠️ High"].to_csv("data/flagged_users.csv", index=False)
            st.toast("Anomalies saved to data/flagged_users.csv")

    # FILTER BY USER
    if selected_user != "All":
        df = df[df['username'] == selected_user]

    # TITLE
    st.markdown("""
    <div style='text-align: center; padding-bottom: 10px;'>
        <h1 style='color:#0dcaf0;'>🛡️ SilentFlag Dashboard</h1>
        <h5>Monitoring User Behavior to Detect Insider Threats</h5>
        <hr>
    </div>
    """, unsafe_allow_html=True)

    # CHART ROWS
    col1, col2 = st.columns(2)

    with col1:
        chart = df.groupby('username')['downloads'].sum().reset_index()
        fig = px.bar(chart, x='username', y='downloads', color='username',
                     title="📥 Total File Downloads per User", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        time_chart = df.groupby('hour')['downloads'].sum().reset_index()
        fig2 = px.area(time_chart, x='hour', y='downloads', title="🕒 Activity by Hour",
                       color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig2, use_container_width=True)

    # LOG CARDS
    st.markdown("### 📋 User Activity Logs")

    for index, row in df.iterrows():
        bg_color = "#ffe6e6" if row['risk_level'] == "⚠️ High" else "#e6ffe6"

        st.markdown(f"""
            <div style='background-color: {bg_color}; padding: 12px; margin: 10px 0; 
                        border-left: 6px solid #444; border-radius: 8px; color: black;'>
                <strong>👤 User:</strong> {row['username']}<br>
                <strong>🕒 Timestamp:</strong> {row['timestamp']}<br>
                <strong>📦 Downloads:</strong> {row['downloads']}<br>
                <strong>🔒 Risk:</strong> {row['risk_level']}
            </div>
        """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Log file not found. Run `generate_logs.py` to create logs first.")
