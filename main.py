import streamlit as st
 
st.set_page_config(page_title="Budget Buddy", page_icon="💰", layout="wide")
 

st.markdown("""
<style>
/* bold text for headings, field labels, tab names and button text */
h1, h2, h3, label p, [role="tab"] p, button p { font-weight: 700; }
 
/* keep the page content from stretching across very wide screens */
.st-key-page { max-width: 1150px; margin: 0 auto; }
 
/* any container whose key starts with "card" or "hover" becomes a rounded card */
[class*="st-key-card"], [class*="st-key-hover"] {
    background: #F8FBFF;
    border-radius: 16px;
    box-shadow: 0 25px 20px rgba(11, 31, 75, 0.1);
}

/* cards whose key starts with "hover" lift up when the mouse is over them */
[class*="st-key-hover"] { transition: transform 0.2s, box-shadow 0.2s; }
[class*="st-key-hover"]:hover { transform: translateY(-3px); box-shadow: 0 8px 22px rgba(11, 31, 75, 0.18); }
 
/* the banner on the home page */
.st-key-hero { background: #BFDBFE; border-radius: 20px; padding: 2rem 2.25rem; }
 
/* action buckets on the home page */
.bucket-emoji { font-size: 2.6rem; line-height: 1; margin-bottom: 0.4rem; }
[class*="st-key-hover_cta"] { padding: 0.75rem 0.5rem; }
[class*="st-key-hover_cta"] a {
    background: #2563EB; display: flex; justify-content: center;
    padding: 0.9rem 1rem; border-radius: 12px; margin-top: 0.5rem;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35); transition: background 0.2s;
}
[class*="st-key-hover_cta"] [data-testid="stPageLink-NavLink"],
[class*="st-key-hover_cta"] [data-testid="stPageLink-NavLink"] * { color: white !important; font-weight: 700; font-size: 1.05rem; }
[class*="st-key-hover_cta"] [data-testid="stPageLink-NavLink"]:hover { background: #1D4ED8; transform: translateY(-1px); }
 
[data-testid="stMetricValue"] { color: #14305F; font-weight: 700; }
</style>

""", unsafe_allow_html=True)
pages = [
    st.Page("home.py", title="Home", icon=":material/home:"),
    st.Page("dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("budget_tab.py", title="Budget", icon=":material/account_balance_wallet:"),
    st.Page("expenses_tab.py", title="Expenses", icon=":material/receipt_long:")
]
 
pg = st.navigation(pages, position="top")
pg.run()