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