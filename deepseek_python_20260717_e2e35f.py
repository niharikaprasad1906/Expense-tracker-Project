#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Personal Expense Tracker
Final Project Implementation
All requirements met – OOD, CSV persistence, validation, summaries.
"""

import csv
import os
import re
from datetime import datetime


class Expense:
    """Blueprint for a single transaction."""
    def __init__(self, expense_id, title, amount, category, date):
        self.id = expense_id
        self.title = title
        self.amount = amount
        self.category = category
        self.date = date

    def to_list(self):
        """Return expense data as a list (for CSV writing)."""
        return [self.id, self.title, self.amount, self.category, self.date]

    def __str__(self):
        return (f"ID: {self.id} | {self.title} | "
                f"${self.amount:.2f} | {self.category} | {self.date}")


class ExpenseTracker:
    """Manager class – holds expenses in memory and controls all operations."""
    FILE_NAME = "expenses.csv"
    HEADER = ["id", "title", "amount", "category", "date"]

    def __init__(self):
        self.expenses = []          # list of Expense objects
        self.load_from_disk()

    # ---------- File Persistence ----------
    def load_from_disk(self):
        """Load existing expenses from CSV file (if present)."""
        self.expenses = []
        if not os.path.isfile(self.FILE_NAME):
            # Create file with header if it doesn't exist
            with open(self.FILE_NAME, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADER)
            return

        with open(self.FILE_NAME, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    exp = Expense(
                        int(row["id"]),
                        row["title"],
                        float(row["amount"]),
                        row["category"],
                        row["date"]
                    )
                    self.expenses.append(exp)
                except (ValueError, KeyError):
                    # skip malformed rows
                    continue

    def save_to_disk(self):
        """Write all expenses back to CSV."""
        with open(self.FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            for exp in self.expenses:
                writer.writerow(exp.to_list())

    # ---------- ID Generation ----------
    def _generate_new_id(self):
        """Return a unique integer ID (max existing + 1, or 1 if empty)."""
        if not self.expenses:
            return 1
        max_id = max(exp.id for exp in self.expenses)
        return max_id + 1

    # ---------- Validation Helpers ----------
    @staticmethod
    def validate_amount(value):
        """Return float if valid, else raise ValueError."""
        try:
            amount = float(value)
            if amount < 0:
                raise ValueError("Amount must be non-negative.")
            return amount
        except ValueError:
            raise ValueError("Invalid monetary value. Please enter a valid numerical decimal amount.")

    @staticmethod
    def validate_date(date_str):
        """
        Validate DD-MM-YYYY format.
        Return the string if valid, else raise ValueError.
        Also accepts empty string -> returns today's date.
        """
        if not date_str.strip():
            # Blank -> auto-assign today
            return datetime.now().strftime("%d-%m-%Y")

        # Check format with regex
        pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$"
        if not re.match(pattern, date_str):
            raise ValueError("Date must be in DD-MM-YYYY format.")

        # Additional validation: does the date actually exist?
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid date (e.g., 31-02-2025).")
        return date_str

    @staticmethod
    def validate_id(id_str):
        """Return int if valid, else raise ValueError."""
        try:
            return int(id_str)
        except ValueError:
            raise ValueError("ID must be a number.")

    # ---------- CRUD Operations ----------
    def add_expense(self, title, amount, category, date):
        """Create and add a new expense. Returns the generated ID."""
        # Validate all fields
        amount = self.validate_amount(amount)
        date = self.validate_date(date)
        # Auto-generate unique ID
        new_id = self._generate_new_id()
        # Create expense and add to list
        expense = Expense(new_id, title.strip(), amount, category.strip(), date)
        self.expenses.append(expense)
        return new_id

    def view_all(self):
        """Return a list of all expenses (for display)."""
        return self.expenses

    def search_by_id(self, expense_id):
        """Return Expense object if found, else None."""
        for exp in self.expenses:
            if exp.id == expense_id:
                return exp
        return None

    def update_expense(self, expense_id, title=None, amount=None, category=None, date=None):
        """
        Update fields of an existing expense.
        Only fields provided (not None) are updated.
        Returns True if successful, False if not found.
        """
        exp = self.search_by_id(expense_id)
        if not exp:
            return False

        if title is not None:
            exp.title = title.strip()
        if amount is not None:
            exp.amount = self.validate_amount(amount)
        if category is not None:
            exp.category = category.strip()
        if date is not None:
            exp.date = self.validate_date(date)
        return True

    def delete_expense(self, expense_id):
        """Remove expense by ID. Return True if deleted, False if not found."""
        exp = self.search_by_id(expense_id)
        if not exp:
            return False
        self.expenses.remove(exp)
        return True

    # ---------- Summary Metrics ----------
    def get_grand_total(self):
        """Return sum of all expense amounts."""
        return sum(exp.amount for exp in self.expenses)

    def get_category_breakdown(self):
        """Return dict {category: total_amount}."""
        breakdown = {}
        for exp in self.expenses:
            breakdown[exp.category] = breakdown.get(exp.category, 0.0) + exp.amount
        return breakdown


# ---------- CLI Menu ----------
def display_menu():
    print("\n" + "=" * 50)
    print("PERSONAL EXPENSE TRACKER")
    print("=" * 50)
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. Search Expense")
    print("4. Update Expense")
    print("5. Delete Expense")
    print("6. View Summary Metrics")
    print("7. Exit & Save Data")
    print("-" * 50)


def view_all_expenses(tracker):
    """Display all expenses in a clean tabular format."""
    expenses = tracker.view_all()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n" + "-" * 80)
    print(f"{'ID':<6} {'Title':<20} {'Amount':<12} {'Category':<15} {'Date':<12}")
    print("-" * 80)
    for exp in expenses:
        print(f"{exp.id:<6} {exp.title[:20]:<20} ${exp.amount:<11.2f} {exp.category[:15]:<15} {exp.date:<12}")
    print("-" * 80)


def add_expense_flow(tracker):
    """Interactive add expense with validation."""
    print("\n--- Add New Expense ---")
    title = input("Enter Expense Title: ").strip()
    if not title:
        print("[ERROR] Title cannot be empty.")
        return

    # Amount – loop until valid
    while True:
        amount_str = input("Enter Expense Amount: ").strip()
        try:
            amount = tracker.validate_amount(amount_str)
            break
        except ValueError as e:
            print(f"[ERROR] {e}")

    category = input("Enter Expense Category: ").strip()
    if not category:
        print("[ERROR] Category cannot be empty.")
        return

    # Date – validation, blank allowed for today
    while True:
        date_str = input("Enter Expense Date (DD-MM-YYYY) or leave blank for today: ").strip()
        try:
            date = tracker.validate_date(date_str)
            break
        except ValueError as e:
            print(f"[ERROR] {e}")

    # Add the expense
    new_id = tracker.add_expense(title, amount, category, date)
    print(f"\nSuccess: New record securely appended! [Generated ID: {new_id}]")


def search_expense_flow(tracker):
    """Search and display an expense by ID."""
    print("\n--- Search Expense ---")
    id_str = input("Enter Expense ID to search: ").strip()
    try:
        exp_id = tracker.validate_id(id_str)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    exp = tracker.search_by_id(exp_id)
    if exp:
        print("\nExpense found:")
        print(f"ID: {exp.id}")
        print(f"Title: {exp.title}")
        print(f"Amount: ${exp.amount:.2f}")
        print(f"Category: {exp.category}")
        print(f"Date: {exp.date}")
    else:
        print(f"[ERROR] No expense with ID {exp_id} found.")


def update_expense_flow(tracker):
    """Interactive update of an expense."""
    print("\n--- Update Expense ---")
    id_str = input("Enter Expense ID to update: ").strip()
    try:
        exp_id = tracker.validate_id(id_str)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    exp = tracker.search_by_id(exp_id)
    if not exp:
        print(f"[ERROR] No expense with ID {exp_id} found.")
        return

    print("Leave field blank to keep current value.")
    print(f"Current Title: {exp.title}")
    title = input("New Title: ").strip()
    if title == "":
        title = None

    print(f"Current Amount: ${exp.amount:.2f}")
    amount_str = input("New Amount: ").strip()
    amount = None
    if amount_str:
        try:
            amount = tracker.validate_amount(amount_str)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return

    print(f"Current Category: {exp.category}")
    category = input("New Category: ").strip()
    if category == "":
        category = None

    print(f"Current Date: {exp.date}")
    date_str = input("New Date (DD-MM-YYYY): ").strip()
    date = None
    if date_str:
        try:
            date = tracker.validate_date(date_str)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return

    # Perform update
    success = tracker.update_expense(exp_id, title, amount, category, date)
    if success:
        print("Expense updated successfully.")
    else:
        print("[ERROR] Update failed.")


def delete_expense_flow(tracker):
    """Delete an expense by ID with confirmation."""
    print("\n--- Delete Expense ---")
    id_str = input("Enter Expense ID to delete: ").strip()
    try:
        exp_id = tracker.validate_id(id_str)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    exp = tracker.search_by_id(exp_id)
    if not exp:
        print(f"[ERROR] No expense with ID {exp_id} found.")
        return

    print(f"Expense to delete: {exp}")
    confirm = input("Are you sure? (y/n): ").strip().lower()
    if confirm == 'y':
        tracker.delete_expense(exp_id)
        print("Expense deleted successfully.")
    else:
        print("Deletion cancelled.")


def show_summary(tracker):
    """Display grand total and category breakdown."""
    print("\nFINANCIAL TELEMETRY DASHBOARD")
    print("=" * 40)

    total = tracker.get_grand_total()
    count = len(tracker.expenses)
    print(f"\nCOMPREHENSIVE STATUS SUMMARY")
    print(f"Grand Combined Total Expenditures : {total:,.2f}")
    print(f"Total Active Unique Tracked Items : {count} Records")

    breakdown = tracker.get_category_breakdown()
    if breakdown:
        print("\nDYNAMIC CATEGORY-WISE BREAKDOWN")
        # Sort categories by total descending
        for cat, amt in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
            print(f"{cat:20} : {amt:,.2f}")

        # Optional mini bar chart (bonus)
        max_amt = max(breakdown.values()) if breakdown else 1
        print("\nCategory Spending Chart (relative to max):")
        for cat, amt in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
            bar_len = int((amt / max_amt) * 30) if max_amt else 0
            bar = "█" * bar_len
            print(f"{cat:15} {bar} {amt:,.2f}")
    else:
        print("\nNo expenses recorded.")


def main():
    tracker = ExpenseTracker()

    while True:
        display_menu()
        choice = input("Choose option (1-7): ").strip()

        if choice == "1":
            add_expense_flow(tracker)
        elif choice == "2":
            view_all_expenses(tracker)
        elif choice == "3":
            search_expense_flow(tracker)
        elif choice == "4":
            update_expense_flow(tracker)
        elif choice == "5":
            delete_expense_flow(tracker)
        elif choice == "6":
            show_summary(tracker)
        elif choice == "7":
            tracker.save_to_disk()
            print("\nData saved successfully. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please enter a number from 1 to 7.")

        # Pause before menu refresh
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()