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

expense_description = st.text_input("Description")
expense_amount = st.number_input("Amount", min_value=0.0, step=1.0)

if st.button("Add expense"):
    st.session_state.expenses.append({
        "date": expense_date,
        "category": expense_category,
        "description": expense_description,
        "amount": expense_amount
    })
    st.success("Expense added.")

st.write(st.session_state.expenses)