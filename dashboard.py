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