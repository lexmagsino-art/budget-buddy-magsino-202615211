import streamlit as st
import datetime
from data_loader import load_budget_data, load_expense_data, add_expense
from shared import DEFAULT_CATEGORIES, get_month_name

st.title("Expenses")

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

