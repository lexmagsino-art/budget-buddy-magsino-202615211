import streamlit as st
import datetime
from data_loader import load_expense_data, add_expense

st.title("Expenses")

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expense_data()

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
    if not expense_description.strip():
        st.error("Enter a description before adding this expense.")
    elif expense_amount <= 0:
        st.error("Enter an amount greater than $0.")
    else:
        new_expense = {
            "date": expense_date.isoformat(),
            "month": expense_date.strftime("%Y-%m"),
            "category": expense_category,
            "description": expense_description.strip(),
            "amount": expense_amount
        }
        st.session_state.expenses.append(new_expense)
        add_expense(new_expense)
        st.success("Expense added.")

st.subheader("Expense History")

if not st.session_state.expenses:
    st.info("No expenses recorded yet.")
else:
    st.dataframe(st.session_state.expenses, use_container_width=True)