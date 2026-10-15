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
    col_date, col_category = st.columns(2)
    with col_date:
        expense_date = st.date_input("Date", value=datetime.date.today())
    month = get_month_name(expense_date)
 
    category_names = get_saved_categories(month)
    using_defaults = not category_names
    if using_defaults:
        category_names = DEFAULT_CATEGORIES.copy()
 
    with col_category:
        category = st.selectbox("Category", category_names)
    if using_defaults:
        st.info(f"No saved budget for {month}, so the default categories are shown.")
 
    col_description, col_amount = st.columns([2, 1])
    with col_description:
        description = st.text_input("Description").title()
    with col_amount:
        amount = st.number_input("Amount (Php)", min_value=0.0, step=100.0)
 
    if st.button("Add expense", type="primary", icon=":material/add_card:"):
        error = validate_expense(category, description, amount)
        if error:
            st.error(error)
        else:
            save_expense(build_expense(expense_date, category, description, amount))
            st.success(f"Added Php{amount:,.2f} to {category} for {month}.")
 
def show_history():
    if not st.session_state.expenses:
        st.info("No expenses recorded yet.")
        return
 
    newest_first = sorted(st.session_state.expenses, key=get_expense_date, reverse=True)
 
    display_rows = []
    for expense in newest_first:
        expense_date = datetime.date.fromisoformat(expense["date"])
        display_rows.append({
            "date": expense_date,
            "month": expense_date.strftime("%B %Y"),   # e.g. October 2026
            "category": expense["category"],
            "description": expense["description"],
            "amount": expense["amount"],
        })
 
    biggest = max(row["amount"] for row in display_rows)
    st.dataframe(
        display_rows,
        width="stretch",
        hide_index=True,
        column_order=["date", "month", "category", "description", "amount"],
        column_config={
            "date": st.column_config.DateColumn("Date", format="MMM D, YYYY"),
            "month": st.column_config.TextColumn("Month"),
            "category": st.column_config.TextColumn("Category"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "amount": st.column_config.ProgressColumn(
                "Amount", format="Php %.2f", min_value=0, max_value=max(biggest, 1)
            ),
        },
    )
 

st.title("Expenses")

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expense_data()

show_expense_form() 
show_history()