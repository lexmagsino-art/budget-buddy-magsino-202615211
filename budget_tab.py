import streamlit as st
import datetime
from data_loader import load_budget_data, save_budget_data

default_categories = ["Food", "Transportation", "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"]

st.title("Budget Planner")
st.write("Plan your budget by allocating amounts to different categories.")

st.subheader("Monthly Budget Allocation")

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

current_month_name = months[datetime.date.today().month - 1]
default_month = st.session_state.get("selected_month", current_month_name)
selected_month = st.selectbox("Select Month:", months, index=months.index(default_month))

if st.session_state.get("loaded_month") != selected_month:
    st.session_state.loaded_month = selected_month

    month_rows = [row for row in load_budget_data() if row["month"] == selected_month]

    if month_rows:
        st.session_state.income_source = month_rows[0]["income_source"]
        st.session_state.expected_income = month_rows[0]["income"]
        st.session_state.categories = {row["category"]: row["planned_amount"] for row in month_rows}
    else:
        st.session_state.income_source = "Salary"
        st.session_state.expected_income = 0.0
        st.session_state.categories = {name: 0.0 for name in default_categories}

income_source = st.text_input("Enter your income source:", value=st.session_state.income_source)
expected_income = st.number_input(
    "Enter your expected monthly income:",
    min_value=0.0,
    step=100.0,
    value=st.session_state.expected_income
)

st.session_state.selected_month = selected_month
st.session_state.income_source = income_source
st.session_state.expected_income = expected_income

st.divider()
st.subheader("Category Allocations")

col1, col2 = st.columns(2)
with col1:
    new_cat = st.text_input("New Category Name:").strip()
    if st.button("Add Category") and new_cat:
        if new_cat not in st.session_state.categories:
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

st.divider()
st.subheader("Planned Amounts")

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

st.divider()
st.subheader("Budget Summary")

total_planned = sum(st.session_state.categories.values())
unallocated_income = expected_income - total_planned

st.metric("Total Planned Expenses", f"Php{total_planned:,.2f}")
st.metric("Unallocated Income", f"Php{unallocated_income:,.2f}")

if unallocated_income < 0:
    st.warning(f"Your planned expenses exceed your income by Php{abs(unallocated_income):,.2f}.")