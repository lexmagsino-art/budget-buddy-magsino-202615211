# Budget Buddy

Budget Buddy is a simple personal finance dashboard built with Python, Streamlit and Matplotlib. You set a monthly budget, record your expenses, and see how your spending compares with your plan. 

## Features

- Budget: Choose a month, enter your income source and expected income, then add, rename, remove and set planned amounts for budget categories. The page shows your total planned expenses, your unallocated income and how much of your income is allocated, and warns you when planned expenses are higher than your income. You can save each month's budget or copy the previous month's.
- Expenses: Record the date, category, description and amount of an expense. Incomplete or invalid entries are rejected. Your full history is shown newest first.
- Dashboard: Pick a month to see your income, total budget, total expenses and remaining budget, a donut chart of the planned budget by category, a planned vs actual chart, and a per-category breakdown that flags categories that went over budget.
- Saved data: Budgets and expenses are stored in CSV files through the provided `data_loader.py`, so they are still there after you restart the app.

## Setup and run

You need Python 3 and an internet connection to install the libraries.

1. Open a terminal in the project folder, the one that contains `main.py`.

2. Create a virtual environment named `SP1`:

   python3 -m venv SP1
   
   On Windows, use `python -m venv SP1` instead.

3. Activate it.

   macOS / Linux:

   source SP1/bin/activate

   Windows (PowerShell):

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   SP1\Scripts\activate

   Your terminal prompt should now start with `(SP1)`.

4. Install the libraries :

   pip install streamlit matplotlib

5. Start the app:

   streamlit run main.py

   The app opens in your browser, usually at http://localhost:8501. Stop it with `Ctrl+C`, and leave the virtual environment with `deactivate`.

## How to use

1. Budget: pick a month, enter your income, set a planned amount for each category, then click **Save Budget**.
2. Expenses: add what you spend. The category list comes from that month's saved budget, or a default list if none is saved yet.
3. Dashboard: pick a month to see how your spending compares with your plan. The Dashboard only shows saved data, so save your budget first.

## Known issues and limitations

- Unsaved budget changes are lost when you switch months or refresh the browser. Click Save Budget first.
- Copy Previous Month fills in the categories and amounts straight away, but the income fields and the summary may not update until your next click.
- Renaming or removing a category does not change expenses already recorded under it. Those expenses keep the old name and appear on the Dashboard as a separate category with no planned amount, so they show as over budget.
- Expenses in a month with no saved budget use the default categories and also appear on the Dashboard as over budget, because nothing was planned.
- Expenses cannot be edited or deleted in the app. 
- Limited month range. The month dropdowns cover last year through two years ahead by default. Expenses dated outside that range are saved but cannot be viewed on the Dashboard.
- Add-expense form: the description and amount stay filled after you add an expense, and descriptions are capitalized word by word, so "mcdonald's lunch" becomes "Mcdonald'S Lunch".
- Single user, local data. There is no login, data is stored in plain CSV files on your computer, and the currency is fixed to Philippine pesos (Php).
