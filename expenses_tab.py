import streamlit as st
import datetime

st.title("Expenses")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "categories" not in st.session_state or not st.session_state.categories:
    st.warning("Set up your budget categories on the Budget tab first.")
    category_names = []
else:
    category_names = [category["name"] for category in st.session_state.categories]

st.subheader("Record an Expense")

expense_date = st.date_input("Date", value=datetime.date.today())
expense_category = st.selectbox("Category", category_names)