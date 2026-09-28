import csv
import json
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
JSON_FILE = "expenses.json"


# ---------------- CSV FUNCTIONS ----------------

def load_expenses():
    expenses = []

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)

    return expenses


def save_expenses(expenses):
    with open(CSV_FILE, "w", newline="") as file:
        fieldnames = ["id", "date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(expenses)


# ---------------- JSON FUNCTION ----------------

def save_json(expenses):
    with open(JSON_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------------- ADD EXPENSE ----------------

def add_expense():
    expenses = load_expenses()

    expense_id = str(len(expenses) + 1)

    date = input("Enter date (DD-MM-YYYY): ")

    # Validate date
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format!")
        return

    category = input("Enter category: ")
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Please enter a valid amount.")
        return

    expense = {
        "id": expense_id,
        "date": date,
        "category": category,
        "description": description,
        "amount": str(amount)
    }

    expenses.append(expense)

    save_expenses(expenses)
    save_json(expenses)

    print("\nExpense added successfully!")


# ---------------- VIEW EXPENSES ----------------

def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n---------------- EXPENSE LIST ----------------")

    print(f"{'ID':<5}{'Date':<15}{'Category':<15}"
          f"{'Description':<25}{'Amount':>10}")

    print("-" * 70)

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"{expense['date']:<15}"
            f"{expense['category']:<15}"
            f"{expense['description']:<25}"
            f"₹{float(expense['amount']):>9.2f}"
        )

    print("-" * 70)


# ---------------- UPDATE EXPENSE ----------------

def update_expense():
    expenses = load_expenses()

    expense_id = input("Enter expense ID to update: ")

    for expense in expenses:

        if expense["id"] == expense_id:

            print("\nLeave blank to keep the old value.")

            category = input(
                f"Category ({expense['category']}): "
            )

            description = input(
                f"Description ({expense['description']}): "
            )

            amount = input(
                f"Amount ({expense['amount']}): "
            )

            if category:
                expense["category"] = category

            if description:
                expense["description"] = description

            if amount:
                try:
                    float(amount)
                    expense["amount"] = amount
                except ValueError:
                    print("Invalid amount.")
                    return

            save_expenses(expenses)
            save_json(expenses)

            print("\nExpense updated successfully!")
            return

    print("\nExpense ID not found.")


# ---------------- DELETE EXPENSE ----------------

def delete_expense():
    expenses = load_expenses()

    expense_id = input("Enter expense ID to delete: ")

    for expense in expenses:

        if expense["id"] == expense_id:

            expenses.remove(expense)

            # Re-number IDs
            for index, item in enumerate(expenses, start=1):
                item["id"] = str(index)

            save_expenses(expenses)
            save_json(expenses)

            print("\nExpense deleted successfully!")
            return

    print("\nExpense ID not found.")


# ---------------- TOTAL EXPENSE ----------------

def total_expense():
    expenses = load_expenses()

    total = 0

    for expense in expenses:
        total += float(expense["amount"])

    print(f"\nTotal Expense: ₹{total:.2f}")


# ---------------- CATEGORY ANALYSIS ----------------

def category_analysis():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses found.")
        return

    categories = {}

    for expense in expenses:

        category = expense["category"]
        amount = float(expense["amount"])

        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    print("\n--------- CATEGORY-WISE EXPENSE ---------")

    for category, amount in categories.items():
        print(f"{category:<20} ₹{amount:.2f}")


# ---------------- MAIN MENU ----------------

def main():

    while True:

        print("\n===================================")
        print("       EXPENSE TRACKER")
        print("===================================")

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Total Expense")
        print("6. Category-wise Analysis")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            update_expense()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            total_expense()

        elif choice == "6":
            category_analysis()

        elif choice == "7":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please try again.")


# ---------------- START PROGRAM ----------------

if __name__ == "__main__":
    main()
