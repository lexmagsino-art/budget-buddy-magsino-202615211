import streamlit as st
 
st.title("Hello! Welcome to Budget Buddy!")
st.write("This is a simple budgeting app to help you manage your finances." \
"        You can plan your budget, record your expenses, and view insights on your spending habits.")
 
buckets = [
    ("budget", "Plan your budget", "Set your income and give every peso a job.",
     "budget_tab.py", "Open Budget", ":material/account_balance_wallet:"),
    ("expense", "Record an expense", "Log what you just spent in a few clicks.",
     "expenses_tab.py", "Open Expenses", ":material/receipt_long:"),
]
for col, (key, title, text, page, link_label, link_icon) in zip(st.columns(2), buckets):
    with col:
        with st.container(border=True, key=f"hover_cta_{key}"):
            st.markdown(f'<div class="bucket-emoji"></div>', unsafe_allow_html=True)
            st.subheader(title)
            st.write(text)
            st.page_link(page, label=link_label, icon=link_icon)
 
st.write("")
 
features = [
    (":material/dashboard:", "Budgeting", "Set your monthly income and give each category a planned amount."),
    (":material/receipt_long:", "Expense tracking", "Log what you spend and keep a history of it."),
    (":material/insights:", "Insights", "Compare planned and actual spending on the dashboard."),
]
for col, (icon, title, text) in zip(st.columns(3), features):
    with col:
        with st.container(border=True):
            st.subheader(f"{icon} {title}")
            st.write(text)
