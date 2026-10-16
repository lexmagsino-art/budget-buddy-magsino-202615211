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
    box-shadow: 0 4px 16px rgba(11, 31, 75, 0.1);
}
""", unsafe_allow_html=True)

pages = [
    st.Page("home.py", title="Home", icon=":material/home:"),
    st.Page("dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("budget_tab.py", title="Budget", icon=":material/account_balance_wallet:"),
    st.Page("expenses_tab.py", title="Expenses", icon=":material/receipt_long:")
]
 
pg = st.navigation(pages, position="top")
pg.run()