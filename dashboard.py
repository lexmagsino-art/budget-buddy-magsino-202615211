from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, Patch
import streamlit as st
import matplotlib.pyplot as plt
from data_loader import load_budget_data, load_expense_data
from shared import get_month_options, get_default_month

CHART_COLORS = ["#1E3A8A", "#93C5FD", "#2563EB", "#BFDBFE", "#0EA5E9", "#0C4A6E", "#60A5FA", "#3730A3"]
NAVY = "#14305F"       
MUTED = "#5B7DB1"       
ACCENT = "#0EA5E9"      
CHART_BG = "#F8FBFF"   
GRID = "#DBE7FA"        

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

def format_percent(pct):
    """Label for a donut slice: hide labels on slices under 6%."""
    return f"{pct:.0f}%" if pct >= 6 else ""

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
 
    total = sum(sizes)
    colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(sizes))]
 
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_alpha(0)  


    wedges, _texts, autotexts = ax.pie(
        sizes, colors=colors, startangle=90, counterclock=False,
        autopct=format_percent,
        pctdistance=0.79,
        wedgeprops={"width": 0.42, "edgecolor": CHART_BG, "linewidth": 2},
    )
    for text, color in zip(autotexts, colors):
        red, green, blue = to_rgb(color)
        is_light = 0.299 * red + 0.587 * green + 0.114 * blue > 0.6
        text.set_color(NAVY if is_light else "white")  
        text.set_fontsize(9)
        text.set_fontweight("bold")
 
    ax.text(0, 0.1, "Total planned", ha="center", fontsize=8, color=MUTED)
    ax.text(0, -0.1, f"Php{total:,.0f}", ha="center", fontsize=11, fontweight="bold", color=NAVY)
 
    legend_labels = [f"{label} (Php{size:,.0f})" for label, size in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, loc="upper center", bbox_to_anchor=(0.5, 0.02),
              ncol=2, frameon=False, labelcolor=NAVY, fontsize=8)
    ax.set_title("Planned Budget by Category", color=NAVY, fontsize=13, fontweight="bold", pad=12)
    ax.axis("equal")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def draw_rounded_bar(ax, x, width, height, color, aspect):
    radius = min(width / 2, 0.1)
    bottom = -2 * radius * aspect
    bar = FancyBboxPatch(
        (x, bottom), width, height - bottom,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        mutation_aspect=aspect, facecolor=color, edgecolor="none",
    )
    ax.add_patch(bar)

def short_amount(value):
    """5400 -> 5.4k, 8000 -> 8k, 650 -> 650 (short labels keep the bars uncluttered)."""
    if value >= 1000:
        return f"{value / 1000:.1f}".rstrip("0").rstrip(".") + "k"
    return f"{value:,.0f}"

def show_comparison_chart(breakdown):
    categories = [item["category"] for item in breakdown]
    planned = [item["planned"] for item in breakdown]
    actual = [item["actual"] for item in breakdown]
    planned_color, actual_color = CHART_COLORS[1], CHART_COLORS[0]
 
    count = len(categories)
    width = 0.34
    top = max(planned + actual + [1])
 
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
 
    ax.set_xlim(-0.6, count - 0.4)
    ax.set_ylim(0, top * 1.3)
    ax.set_xticks(range(count))
    ax.set_xticklabels(categories, rotation=30, ha="right", color=NAVY, fontsize=9)
    ax.set_yticks([])  
    ax.tick_params(axis="x", length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.spines["bottom"].set_linewidth(1.5)
    ax.set_title("Planned vs Actual Spending", color=NAVY, fontsize=13, fontweight="bold", pad=12, loc="left")
    fig.tight_layout()

    position = ax.get_position()
    x_per_inch = (count + 0.2) / (position.width * fig.get_figwidth())
    y_per_inch = (top * 1.3) / (position.height * fig.get_figheight())
    aspect = y_per_inch / x_per_inch
    
    for i in range(count):
        for value, offset, color in ((planned[i], -width - 0.02, planned_color), (actual[i], 0.02, actual_color)):
            if value > 0:
                draw_rounded_bar(ax, i + offset, width, value, color, aspect)
                ax.text(i + offset + width / 2, value + top * 0.02, short_amount(value),
                        ha="center", va="bottom", fontsize=7.5, fontweight="bold", color=NAVY)
    
    ax.legend(
        handles=[Patch(color=planned_color, label="Planned"), Patch(color=actual_color, label="Actual")],
        loc="upper right", ncol=2, frameon=False, labelcolor=NAVY, fontsize=9,
    )
    st.pyplot(fig)
    plt.close(fig)

def show_breakdown(breakdown):
    for item in breakdown:
        planned, actual = item["planned"], item["actual"]
        remaining = planned - actual
 
        if planned > 0:
            fraction = min(actual / planned, 1.0)
        else:
            fraction = 1.0 if actual > 0 else 0.0
 
        col_name, col_bar, col_status = st.columns([2, 4, 2])
        col_name.write(f"**{item['category']}**")
        with col_bar:
            st.progress(fraction, text=f"{format_money(actual)} of {format_money(planned)}")
        if remaining < 0:
            col_status.write(f":red[Over by {format_money(abs(remaining))}]")
        else:
            col_status.write(f":green[{format_money(remaining)} left]")

st.title("Dashboard")

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
    show_summary(income, total_planned, total_actual)

    st.write("")
    tab_charts, tab_breakdown = st.tabs(["Charts", "Breakdown"])
 
    with tab_charts:
        col_pie, col_bar = st.columns(2)
        with col_pie:
            with st.container(border=True, key="card_pie"):
                show_pie_chart(planned_by_category)
        with col_bar:
            with st.container(border=True, key="card_bar"):
                show_comparison_chart(breakdown)
 
    with tab_breakdown:
        with st.container(border=True, key="card_breakdown"):
            show_breakdown(breakdown)