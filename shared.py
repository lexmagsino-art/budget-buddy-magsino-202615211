import datetime
import streamlit as st

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


DEFAULT_CATEGORIES = ["Food", "Transportation", "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"]


def get_month_name(date):
    """Turn a date into the label used on every page, like 'October 2027'."""
    return f"{MONTHS[date.month - 1]} {date.year}"


def get_month_options(years_back=1, years_ahead=2):
    """Every 'Month Year' label, from years_back before this year to years_ahead after it."""
    this_year = datetime.date.today().year
    options = []
    for year in range(this_year - years_back, this_year + years_ahead + 1):
        for month in MONTHS:
            options.append(f"{month} {year}")
    return options


def get_default_month():
    """The month last chosen on any page, or the current month if none (or an old-style one)."""
    current = get_month_name(datetime.date.today())
    chosen = st.session_state.get("selected_month", current)
    if chosen not in get_month_options():
        return current
    return chosen