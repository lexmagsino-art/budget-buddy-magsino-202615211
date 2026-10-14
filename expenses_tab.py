import streamlit as st
import datetime
from data_loader import load_budget_data, load_expense_data, add_expense
from shared import DEFAULT_CATEGORIES, get_month_name

def get_saved_categories(month):
    """Category names saved in that month's budget (empty list if none saved)."""
    names = []
    for row in load_budget_data():
        if row["month"] == month and row["category"] not in names:
            names.append(row["category"])
    return names


def validate_expense(category, description, amount):
    """Return an error message, or None if the entry is valid."""
    if not category:
        return "Choose a category."
    if not description.strip():
        return "Enter a description before adding this expense."
    if amount <= 0:
        return "Enter an amount greater than Php0."
    return None

def build_expense(expense_date, category, description, amount):
    """Build one expense record matching the CSV columns."""
    return {
        "date": expense_date.isoformat(),
        "month": get_month_name(expense_date),
        "category": category,
        "description": description.strip(),
        "amount": amount
    }


def save_expense(expense):
    """Keep the expense on screen and write it to the CSV right away."""
    st.session_state.expenses.append(expense)
    add_expense(expense)


def get_expense_date(expense):
    """Sort key for the history table."""
    return expense["date"]

def show_expense_form():
    st.subheader("Record an Expense")

    expense_date = st.date_input("Date", value=datetime.date.today())
    month = get_month_name(expense_date)

    category_names = get_saved_categories(month)
    if not category_names:
        category_names = DEFAULT_CATEGORIES.copy()
        st.info(f"No saved budget for {month}, so the default categories are shown.")

    category = st.selectbox("Category", category_names)
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, step=100.0)

    if st.button("Add expense"):
        error = validate_expense(category, description, amount)
        if error:
            st.error(error)
        else:
            save_expense(build_expense(expense_date, category, description, amount))
            st.success(f"Added Php{amount:,.2f} to {category} for {month}.")