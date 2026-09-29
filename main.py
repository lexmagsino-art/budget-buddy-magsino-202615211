import streamlit as st

# Group the pages into a dictionary for navigation
pages = {
    "Main": [
        st.Page("home.py", title="Home", icon="🏠"),
        st.Page("dashboard.py", title="Dashboard", icon="📊"),
        st.Page("budget_tab.py", title="Budget", icon="💰"),
        st.Page("expenses_tab.py", title="Expenses", icon="🛒")
    ]
}

# Initialize the navigation system
pg = st.navigation(pages)
pg.run()
