import streamlit as st

default_categories = ["Food", "Transportation", "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"]

st.title("Budget Planner")
st.write("Plan your budget by allocating amounts to different categories.")

if "categories" not in st.session_state:
    st.session_state.categories = default_categories.copy()

st.subheader("Monthly Budget Allocation")

months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
selected_month = st.selectbox("Select Month:", months)

income_source = st.text_input("Enter your income source:", "Salary")
expected_income = st.number_input("Enter your expected monthly income:", min_value=0.0, step=100.0)

st.session_state.selected_month = selected_month
st.session_state.income_source = income_source
st.session_state.expected_income = expected_income

st.divider()
st.subheader("Category Allocations")

col1, col2 = st.columns(2)
with col1:
    new_cat = st.text_input("New Category Name:")
    if st.button("Add Category") and new_cat:
        if new_cat not in st.session_state.categories:
            st.session_state.categories[new_cat] = 0.0
            st.rerun()

with col2:
    cat_to_remove = st.selectbox("Select Category to Remove:", ["-- None --"] + list(st.session_state.categories.keys()))
    if st.button("Remove Category") and cat_to_remove != "-- None --":
        del st.session_state.categories[cat_to_remove]
        st.rerun()
