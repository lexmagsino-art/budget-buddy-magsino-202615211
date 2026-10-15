import streamlit as st
 
st.set_page_config(page_title="Budget Buddy", page_icon="💰", layout="wide")
 
# A flat list of pages shows as a row of tabs along the top
pages = [
    st.Page("home.py", title="Home", icon=":material/home:"),
    st.Page("dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("budget_tab.py", title="Budget", icon=":material/account_balance_wallet:"),
    st.Page("expenses_tab.py", title="Expenses", icon=":material/receipt_long:")
]
 
# position="top" moves the navigation from the sidebar to the top bar
pg = st.navigation(pages, position="top")
pg.run()