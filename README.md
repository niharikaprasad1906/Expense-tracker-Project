# Expense Tracker Project

A simple Python-based personal expense tracker that lets you add, view, search, update, delete, and summarize your expenses using a CSV file for persistence.

## Features

- Add new expenses with title, amount, category, and date
- View all recorded expenses in a clean table format
- Search for an expense by ID
- Update existing expense details
- Delete expenses with confirmation
- View summary metrics including:
  - grand total
  - total number of records
  - category-wise spending breakdown

## Project Files

- Expense tracker.py - Main CLI application
- expenses.csv - Persistent storage for expenses

## How to Run

1. Make sure Python 3 is installed on your system.
2. Open the project folder in a terminal.
3. Run:

```bash
python "Expense tracker.py"
```

## Example Usage

The application provides a menu-driven interface with the following options:

1. Add New Expense
2. View All Expenses
3. Search Expense
4. Update Expense
5. Delete Expense
6. View Summary Metrics
7. Exit & Save Data

## Notes

- Amounts must be numeric and non-negative.
- Dates must follow the DD-MM-YYYY format.
- If no date is provided, the program uses today's date automatically.

