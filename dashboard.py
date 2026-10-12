import streamlit as st
import matplotlib.pyplot as plt
import datetime
from data_loader import load_budget_data, load_expense_data

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def get_month_budget(month):
    income = 0.0
    planned_by_category = {}
    for row in load_budget_data():
        if row["month"] == month:
            income = row["income"]
            planned_by_category[row["category"]] = row["planned_amount"]
    return income, planned_by_category

def get_month_actuals(month):
    actual_by_category = {}
    for row in load_expense_data():
        if row["month"] == month:
            category = row["category"]
            actual_by_category[category] = actual_by_category.get(category, 0.0) + row["amount"]
    return actual_by_category

def build_breakdown(planned_by_category, actual_by_category):
    all_categories = list(planned_by_category.keys())
    for category in actual_by_category:
        if category not in planned_by_category:
            all_categories.append(category)

    breakdown = []
    for category in all_categories:
        breakdown.append({
            "category": category,
            "planned": planned_by_category.get(category, 0.0),
            "actual": actual_by_category.get(category, 0.0)
        })
    return breakdown


def format_money(amount):
    if amount < 0:
        return f"-Php{abs(amount):,.2f}"
    return f"Php{amount:,.2f}"

def show_summary(income, total_planned, total_actual):
    remaining = income - total_actual
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Income", format_money(income))
    col2.metric("Planned Expenses", format_money(total_planned))
    col3.metric("Actual Expenses", format_money(total_actual))
    col4.metric("Money Remaining", format_money(remaining))

def show_pie_chart(planned_by_category):
    labels = []
    sizes = []
    for category, amount in planned_by_category.items():
        if amount > 0:
            labels.append(category)
            sizes.append(amount)

    if not sizes:
        st.info("No planned amounts above $0 to chart for this month.")
        return

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    ax.set_title("Planned Budget by Category")
    st.pyplot(fig)
    plt.close(fig)

def show_comparison_chart(breakdown):
    categories = [item["category"] for item in breakdown]
    planned = [item["planned"] for item in breakdown]
    actual = [item["actual"] for item in breakdown]

    positions = list(range(len(categories)))
    width = 0.4

    fig, ax = plt.subplots()
    ax.bar([p - width / 2 for p in positions], planned, width, label="Planned")
    ax.bar([p + width / 2 for p in positions], actual, width, label="Actual")
    ax.set_xticks(positions)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.set_ylabel("Amount (Php)")
    ax.set_title("Planned vs Actual Spending")
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
