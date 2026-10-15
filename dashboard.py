import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import datetime
from data_loader import load_budget_data, load_expense_data
from shared import get_month_options, get_default_month

CHART_COLORS = ["#2563EB", "#F59E0B", "#14B8A6", "#8B5CF6", "#17365D", "#F87171", "#38BDF8", "#22C55E"]
NAVY = "#17365D"
SOFT = "#DBEAFE"
CHART_BG = "#F3E3C3"   
GRID = "#DCC8A0"        
BLUE = "#2563EB"
SKY = "#6BA8F7"

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
    if total_planned > 0:
        used_hint = f"{total_actual / total_planned:.0%} of budget used"
    else:
        used_hint = "No budget planned yet"
    remaining = total_planned - total_actual
 
    cards = [
        ("Available Balance", income - total_actual, f"Income: {format_money(income)}"),
        ("Total Budget", total_planned, "Planned for the month"),
        ("Total Expenses", total_actual, used_hint),
        ("Remaining Budget", remaining, "Over budget!" if remaining < 0 else "Still available to spend"),
    ]
    for i, (col, (label, value, hint)) in enumerate(zip(st.columns(4), cards)):
        with col:
            with st.container(border=True, key=f"card_metric_{i}"):
                st.metric(label, format_money(value))
                st.caption(hint)
 
    if total_planned > 0:
        used = total_actual / total_planned
        st.progress(min(used, 1.0), text=f"Overall budget used: {used:.0%}")

def show_pie_chart(planned_by_category):
    labels = []
    sizes = []
    for category, amount in planned_by_category.items():
        if amount > 0:
            labels.append(category)
            sizes.append(amount)

    if not sizes:
        st.info("No planned amounts above Php0 to chart for this month.")
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

def show_breakdown(breakdown):
    widths = [2, 1, 1, 1.5]

    header = st.columns(widths)
    header[0].write("**Category**")
    header[1].write("**Planned**")
    header[2].write("**Actual**")
    header[3].write("**Status**")

    for item in breakdown:
        remaining = item["planned"] - item["actual"]
        row = st.columns(widths)
        row[0].write(item["category"])
        row[1].write(format_money(item["planned"]))
        row[2].write(format_money(item["actual"]))
        if remaining < 0:
            row[3].write(f":red[Over by {format_money(abs(remaining))}]")
        else:
            row[3].write(f":green[{format_money(remaining)} left]")

st.title("Dashboard")

current_month_name = MONTHS[datetime.date.today().month - 1]
default_month = st.session_state.get("selected_month", current_month_name)
months = get_month_options()
selected_month = st.selectbox(
    "Select Month:", months,
    index=months.index(st.session_state.get("selected_month", get_default_month())),
    key="dashboard_month"
)

income, planned_by_category = get_month_budget(selected_month)
actual_by_category = get_month_actuals(selected_month)

if not planned_by_category and not actual_by_category:
    st.info(f"Nothing saved for {selected_month} yet. Set up a budget on the Budget tab and click Save Budget.")
else:
    breakdown = build_breakdown(planned_by_category, actual_by_category)
    total_planned = sum(planned_by_category.values())
    total_actual = sum(actual_by_category.values())

    st.subheader("Monthly Financial Summary")
    show_summary(income, total_planned, total_actual)

    st.divider()
    st.subheader("Budget Visualization")
    show_pie_chart(planned_by_category)
    show_comparison_chart(breakdown)

    st.divider()
    st.subheader("Budget Breakdown")
    show_breakdown(breakdown)