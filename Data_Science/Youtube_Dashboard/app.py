import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import plotly.express as px

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="YouTube Analytics Dashboard",
    page_icon="📺",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>
[data-testid="stHeader"]{
    background: #020617 !important;
}

/* remove header transparency gap */
header{
    background: #020617 !important;
}
/* whole app */
.stApp{
    background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
    color: white;
}

/* main container */
.main{
    background: transparent;
    color: white;
}

/* sidebar */
section[data-testid="stSidebar"]{
    background: #020617;
    border-right: 1px solid #334155;
}

/* input box */
.stTextInput > div > div > input{
    background: #111827;
    color: white;
    border: 1px solid #334155;
    border-radius: 10px;
}

/* metric cards */
.metric-card{
    background: rgba(30,41,59,0.9);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,.35);
    text-align:center;
    border:1px solid #334155;
}

/* titles */
.big-title{
    text-align:center;
    font-size:44px;
    font-weight:700;
    color:white;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:#94a3b8;
    margin-bottom:35px;
    font-size:18px;
}

/* remove white block backgrounds */
div[data-testid="stVerticalBlock"]{
    background: transparent;
}

/* chart container */
div[data-testid="stPlotlyChart"]{
    background: rgba(15,23,42,.65);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #334155;
}

/* info box */
div[data-testid="stAlert"]{
    background:#111827;
    color:white;
    border-radius:12px;
    border:1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------
st.markdown(
    "<div class='big-title'>📺 YouTube Analytics Dashboard</div>",
    unsafe_allow_html=True
)

# -------------------------
# API
# -------------------------
API_KEY = "AIzaSyB_JvWZtiI3axd3yD2oaqebTMu3gcbkOrs"  # regenerate your old exposed key
youtube = build("youtube", "v3", developerKey=API_KEY)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("🔍 Search Channel")
channel_id = st.sidebar.text_input(
    "Enter Channel ID",
    placeholder="Example: UC_x5XG1OV2P6uZZ5FSM9Ttw"
)

st.sidebar.markdown("---")
st.sidebar.info("Paste a valid YouTube Channel ID")

# -------------------------
# FETCH
# -------------------------
def get_channel_stats(channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        if "items" not in response or len(response["items"]) == 0:
            return None

        data = response["items"][0]

        return {
            "Channel": data["snippet"]["title"],
            "Subscribers": int(data["statistics"].get("subscriberCount", 0)),
            "Views": int(data["statistics"].get("viewCount", 0)),
            "Videos": int(data["statistics"].get("videoCount", 0))
        }

    except:
        return None


# -------------------------
# DISPLAY
# -------------------------
if channel_id:

    stats = get_channel_stats(channel_id)

    if stats:

        st.success(f"Loaded: {stats['Channel']}")

        # KPI Cards
        c1, c2, c3 = st.columns(3)

        c1.markdown(f"""
        <div class="metric-card">
            <h2>👥 Subscribers</h2>
            <h1>{stats["Subscribers"]:,}</h1>
        </div>
        """, unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="metric-card">
            <h2>👁 Views</h2>
            <h1>{stats["Views"]:,}</h1>
        </div>
        """, unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="metric-card">
            <h2>🎥 Videos</h2>
            <h1>{stats["Videos"]:,}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## 📊 Performance Analytics")

        df = pd.DataFrame({
            "Metric": ["Subscribers", "Views", "Videos"],
            "Count": [
                stats["Subscribers"],
                stats["Views"],
                stats["Videos"]
            ]
        })

        fig = px.bar(
            df,
            x="Metric",
            y="Count",
            text="Count",
            template="plotly_dark",
            title="YouTube Channel Metrics"
        )

        fig.update_layout(
            height=500,
            title_x=0.35
        )

        st.plotly_chart(fig, use_container_width=True)

        # Pie Chart
        st.markdown("## 🥧 Distribution")

        pie = px.pie(
            df,
            names="Metric",
            values="Count",
            hole=0.45,
            template="plotly_dark"
        )

        st.plotly_chart(pie, use_container_width=True)

    else:
        st.error("Invalid Channel ID")

else:
    st.info("👈 Enter Channel ID in sidebar")