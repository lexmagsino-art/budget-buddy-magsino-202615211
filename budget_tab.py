import streamlit as st
import datetime
from data_loader import load_budget_data, load_expense_data, save_budget_data
from shared import DEFAULT_CATEGORIES, get_month_options, get_default_month

def load_month_if_changed(month):
    """Load saved data the first time a month is shown, and whenever the month changes."""
    if st.session_state.get("loaded_month") != selected_month:
        st.session_state.loaded_month = selected_month
        load_month_into_session(month)

def load_month_into_session(month):
    """Load a month's saved budget into session state, or start from the defaults."""
    month_rows = [row for row in load_budget_data() if row["month"] == month]

    if month_rows:
        st.session_state.income_source = month_rows[0]["income_source"]
        st.session_state.expected_income = month_rows[0]["income"]
        st.session_state.categories = {row["category"]: row["planned_amount"] for row in month_rows}
    else:
        st.session_state.income_source = "Salary"
        st.session_state.expected_income = 0.0
        st.session_state.categories = {name: 0.0 for name in DEFAULT_CATEGORIES}

def get_previous_month(month):
    """Return the month before `month` in the month options, or None if there isn't one."""
    months = get_month_options()
    position = months.index(month)
    return months[position - 1] if position > 0 else None
 
 
def copy_previous_month(month):
    """Button callback: replace the on-screen budget with last month's saved budget."""
    previous_month = get_previous_month(month)
    if previous_month is None:
        st.session_state.copy_result = ("warning", "There is no earlier month to copy from.")
        return
 
    previous_rows = [row for row in load_budget_data() if row["month"] == previous_month]
    if not previous_rows:
        st.session_state.copy_result = ("warning", f"No saved budget found for {previous_month}.")
        return
 
    st.session_state.income_source = previous_rows[0]["income_source"]
    st.session_state.expected_income = previous_rows[0]["income"]
    st.session_state.categories = {row["category"]: row["planned_amount"] for row in previous_rows}
 
    for key in list(st.session_state.keys()):
        if key.startswith(f"amount_{month}_"):
            del st.session_state[key]
 
    st.session_state.copy_result = (
        "success",
        f"Copied {previous_month}'s budget. Review it, then click Save Budget to keep it.",
    )

def get_month_spending(month):
    """Total actual spending per category for a month (from the expense records)."""
    spending = {}
    for row in load_expense_data():
        if row["month"] == month:
            spending[row["category"]] = spending.get(row["category"], 0.0) + row["amount"]
    return spending

def rename_category(old_name, new_name):
    """Rename a category, keeping its amount and its place in the list."""
    renamed = {}
    for name, amount in st.session_state.categories.items():
        if name == old_name:
            renamed[new_name] = amount
        else:
            renamed[name] = amount
    st.session_state.categories = renamed

def calculate_totals(income, categories):
    """Return (total planned expenses, unallocated income)."""
    total_planned = sum(categories.values())
    return total_planned, income - total_planned

def validate_budget(income_source, categories):
    """Return an error message, or None if the budget can be saved."""
    if not income_source.strip():
        return "Enter an income source before saving."
    if not categories:
        return "Add at least one category before saving."
    return None


def build_budget_rows(month, income_source, income, categories):
    """One CSV row per category, matching the budget file's columns."""
    rows = []
    for name, amount in categories.items():
        rows.append({
            "month": month,
            "income_source": income_source.strip(),
            "income": income,
            "category": name,
            "planned_amount": amount
        })
    return rows

def save_budget(month, income_source, income, categories):
    """Replace this month's rows in the CSV and keep every other month's rows."""
    other_months_rows = [row for row in load_budget_data() if row["month"] != month]
    this_month_rows = build_budget_rows(month, income_source, income, categories)
    save_budget_data(other_months_rows + this_month_rows)


def show_copy_previous_button(month):
    """Show the button to copy the previous month's budget and display any result."""
    if st.button("Copy Previous Month"):
        copy_previous_month(month)

    if "copy_result" in st.session_state:
        result_type, message = st.session_state.copy_result
        if result_type == "success":
            st.success(message)
        elif result_type == "warning":
            st.warning(message)
        elif result_type == "error":
            st.error(message)
        del st.session_state.copy_result


def show_month_selector():
    months = get_month_options()
    default_month = get_default_month()
    return st.selectbox("Select Month:", months, index=months.index(default_month))


def show_income_inputs():
    income_source = st.text_input("Enter your income source:", value=st.session_state.income_source)
    expected_income = st.number_input(
        "Enter your expected monthly income:",
        min_value=0.0,
        step=100.0,
        value=st.session_state.expected_income
        )
    st.session_state.income_source = income_source
    st.session_state.expected_income = expected_income
    return income_source, expected_income

def show_add_and_remove():
    col1, col2 = st.columns(2)
    with col1:
        new_cat = st.text_input("New Category Name:").strip()
        if st.button("Add Category") and new_cat:
            if new_cat in st.session_state.categories:
                st.warning("A category with that name already exists.")
            else:
                st.session_state.categories[new_cat] = 0.0
                st.rerun()

    with col2:
        cat_to_remove = st.selectbox(
            "Select Category to Remove:",
            ["-- None --"] + list(st.session_state.categories.keys())
        )
        if st.button("Remove Category") and cat_to_remove != "-- None --":
            del st.session_state.categories[cat_to_remove]
            st.rerun()


def show_rename():
    col1, col2 = st.columns(2)
 
    with col1:
        to_rename = st.selectbox(
            "Select Category to Rename:",
            ["-- None --"] + list(st.session_state.categories.keys())
        )
 
    with col2:
        new_name = st.text_input("New name:").strip()
        if st.button("Rename Category", icon=":material/edit:") and to_rename != "-- None --" and new_name:
            if new_name in st.session_state.categories:
                st.warning("A category with that name already exists.")
            else:
                rename_category(to_rename, new_name)
                st.rerun()

def show_planned_amounts(month):
    spending = get_month_spending(month)
 
    for name in st.session_state.categories:
        col_name, col_amount = st.columns([2, 1])
 
        with col_amount:
            st.session_state.categories[name] = st.number_input(
                f"Planned amount for {name}",
                min_value=0.0,
                step=100.0,
                value=st.session_state.categories[name],
                key=f"amount_{month}_{name}",
                label_visibility="collapsed"
            )
 
        planned = st.session_state.categories[name]
        spent = spending.get(name, 0.0)
 
        with col_name:
            st.write(f"**{name}**")
            if planned > 0 or spent > 0:
                fraction = min(spent / planned, 1.0) if planned > 0 else 1.0
                st.progress(fraction, text=f"Php{spent:,.2f} spent of Php{planned:,.2f}")
                if spent > planned:
                    st.caption(f":red[Over by Php{spent - planned:,.2f}]")
 


def show_summary(income):
    st.subheader("Budget Summary")
 
    total_planned, unallocated_income = calculate_totals(income, st.session_state.categories)
 
    st.metric("Total Planned Expenses", f"Php{total_planned:,.2f}")
    st.metric("Unallocated Income", f"Php{unallocated_income:,.2f}")
 
    if income > 0:
        allocated = total_planned / income
        st.progress(min(allocated, 1.0), text=f"{allocated:.0%} of your income is allocated")
    else:
        st.caption("Enter your expected income to see how much is allocated.")
 
    if unallocated_income < 0:
        st.warning(f"Your planned expenses exceed your income by Php{abs(unallocated_income):,.2f}.")

def show_save_button(month, income_source, income):
    if st.button("Save Budget", type="primary"):
        error = validate_budget(income_source, st.session_state.categories)
        if error:
            st.error(error)
        else:
            save_budget(month, income_source, income, st.session_state.categories)
            st.success(f"Budget for {month} saved.")

st.title("Budget Planner")
st.write("Plan your budget by allocating amounts to different categories.")
 
with st.container(border=True, key="card_setup"):
    selected_month = show_month_selector()
    load_month_if_changed(selected_month)
    income_source, expected_income = show_income_inputs()
    st.session_state.selected_month = selected_month
    st.caption("Save your budget before switching months. Unsaved changes aren't kept.")
    show_copy_previous_button(selected_month)
 
col_left, col_right = st.columns([3, 2])
 
with col_left:
    with st.container(border=True, key="card_amounts"):
        st.subheader("Planned Amounts")
        with st.expander("Add, remove or rename categories"):
            show_add_and_remove()
            show_rename()
        show_planned_amounts(selected_month)
 
with col_right:
    with st.container(border=True, key="card_summary"):
        show_summary(expected_income)
        show_save_button(selected_month, income_source, expected_income)