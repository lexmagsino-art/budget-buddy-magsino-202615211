import streamlit as st
import datetime
from data_loader import load_budget_data, save_budget_data
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

def show_income_inputs():
    income_source = st.text_input("Enter your income source:", value=st.session_state.income_source)
    expected_income = st.number_input(
        "Enter your expected monthly income:",
        min_value=0.0,
        step=100.0,
        value=st.session_state.expected_income
        )


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
    rename_col1, rename_col2 = st.columns(2)

    with rename_col1:
        cat_to_rename = st.selectbox(
            "Select Category to Rename:",
            ["-- None --"] + list(st.session_state.categories.keys())
        )

    with rename_col2:
        new_name = st.text_input("New name:").strip()
        if st.button("Rename Category") and cat_to_rename != "-- None --" and new_name:
            if new_name in st.session_state.categories:
                st.warning("A category with that name already exists.")
            else:
                renamed = {}
                for name, amount in st.session_state.categories.items():
                    if name == cat_to_rename:
                        renamed[new_name] = amount
                    else:
                        renamed[name] = amount
                st.session_state.categories = renamed
                st.rerun()

def show_planned_amounts(month):
    for name in st.session_state.categories:
        col_name, col_amount = st.columns([2, 1])
        with col_name:
            st.write(name)
        with col_amount:
            st.session_state.categories[name] = st.number_input(
                f"Planned amount for {name}",
                min_value=0.0,
                step=10.0,
                value=st.session_state.categories[name],
                key=f"amount_{selected_month}_{name}",
                label_visibility="collapsed"
            )


def show_summary(income):
    st.subheader("Budget Summary")

    total_planned, unallocated_income = calculate_totals(income, st.session_state.categories)

    st.metric("Total Planned Expenses", f"Php{total_planned:,.2f}")
    st.metric("Unallocated Income", f"Php{unallocated_income:,.2f}")

    if unallocated_income < 0:
        st.warning(f"Your planned expenses exceed your income by Php{abs(unallocated_income):,.2f}.")


def show_save_button(month, income_source, income):
    if st.button("Save Budget"):
        if not income_source.strip():
            st.error("Enter an income source before saving.")
            st.stop()
        if not st.session_state.categories:
            st.error("Add at least one category before saving.")
            st.stop()
        
    other_months_rows = [row for row in load_budget_data() if row["month"] != selected_month]

    this_month_rows = []
    for category_name, amount in st.session_state.categories.items():
        this_month_rows.append({
            "month": selected_month,
            "income_source": income_source,
            "income": expected_income,
            "category": category_name,
            "planned_amount": amount
        })

    save_budget_data(other_months_rows + this_month_rows)
    st.success("Budget saved.")

st.title("Budget Planner")
st.write("Plan your budget by allocating amounts to different categories.")

st.subheader("Monthly Budget Allocation")