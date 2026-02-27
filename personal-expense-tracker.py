"""
Personal Expense Tracker Module
AUTHOR: MOHAMAD MUSADIQ (@arqoryn)
DATE: 27/02/2026
The application supports the following operations: - Add new expenses with date, category, and amount - Remove existing expenses by index - Edit existing expense details (date, category, or amount) - View all expenses in a formatted table - View expenses grouped by category - Calculate and display total spending by category
Expense categories include: 1. Housing and Utilities 2. Food 3. Transportation 4. Health 5. Family Care 6. Entertainment 7. EMI/Loans 8. Miscellaneous
Data Storage: All expense data is persisted in 'personalExpense.csv' with columns: index, date, category, amount

"""

FILE_PATH = "personalExpense.csv"

def loadData():
    data = []

    with open(FILE_PATH, "r") as f:
        lines = f.readlines()

    for line in lines[1:]:
        line = line.strip()
        entry = line.split(",")

        dataItem = {
            "index": int(entry[0]),
            "date" : str(entry[1]),
            "category": str(entry[2]),
            "amount": float(entry[3])
        }

        data.append(dataItem)

    return data

def saveData(data):
    with open(FILE_PATH, "w") as f:
        f.write("index,date,category,amount")
        f.write('\n')

        for d in data:
            line = f"{d['index']},{d['date']},{d['category']},{d['amount']}\n"
            f.write(line)
    

def show_menu():
    print("MENU")
    print("1. Add expense")
    print("2. Remove expense")
    print("3. Edit expense")
    print("4. View All expenses")
    print("5. View Grouped expenses")
    print("6. Calculate Total Spending")
    print("7. Exit")

def get_choice():
    choice = int(input("Enter your choice: "))
    return choice


def print_all_categories():
    print("1-Housing And Utilities")
    print("2-Food")
    print("3-Transportaion")
    print("4-Health")
    print("5-Family Care")
    print("6-Entertainment")
    print("7-EMI/Loans")
    print("8-Misc")

def get_cat_from_int(categoryInt):
    if categoryInt == 1:
        cat = 'housing_and_utilities'
    elif categoryInt == 2:
        cat = 'food'
    elif categoryInt == 3:
        cat = 'transportation'
    elif categoryInt == 4:
        cat = 'health'
    elif categoryInt == 5:
        cat = 'family_care'
    elif categoryInt == 6:
        cat = 'entertainment'
    elif categoryInt == 7:
        cat = 'emi_or_loans'
    elif categoryInt == 8:
        cat = 'miscellaneous'

    return cat

def add_expense(data):
    valid = 0
    while not valid:
        date = str(input("Enter the date (DD-MM-YYYY): "))
        date_pieces = date.split("-")
        if (31 >= int(date_pieces[0]) >= 1) is False:
            valid = 0
            print("Invalid Date! Enter again...")
            continue
        elif (12 >= int(date_pieces[1]) >= 1) is False:
            valid = 0
            print("Invalid Date! Enter again...")
            continue
        elif (9999 >= int(date_pieces[2]) >= 2000) is False:
            valid = 0
            print("Invalid Date! Enter again...")
            continue
        elif len(date) != 10:
            valid = 0
            print("Invalid Date! Enter again...")
            continue
        else:
            valid = 1


    print_all_categories()
    categoryInt = int(input("Enter the Category: (1-8):  "))
    cat = get_cat_from_int(categoryInt)
    
    amount_valid = 0
    while not amount_valid:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            amount_valid = 0
            print("Amount can't be negative or zero! Enter again...")
            continue
        else:
            amount_valid = 1


    next_index = max((d["index"] for d in data), default = 0) + 1

    data.append({
        "index": int(next_index),
        "date": str(date),
        "category": str(cat),
        "amount":float(amount)
    })

    return data

def remove_expense(data):
    index = int(input("Enter the index to remove expense: "))
    for d in data:
        if int(d['index']) == index:
            data.remove(d)
            print("Expense deleted! ")
            return
    print("Expense not found!")
        

def edit_expense(data):
    edit_index = int(input("Enter the index to edit the expense: "))
    for d in data:
        if int(d['index']) == edit_index:
            option = int(input("What do you want to edit? (1-date, 2-category, 3-amount): "))
            if option == 1:
                new_date = input("Enter new date: ")
                d['date'] = new_date
                print("Date Updated! ")
            elif option == 2:
                print_all_categories()
                new_cat_int = int(input("Enter new Category: "))
                new_cat_str = get_cat_from_int(new_cat_int)
                d['category'] = new_cat_str
                print("Category Updated! ")
            elif option == 3:
                new_amount = float(input("Enter new amount: "))
                d['amount'] = new_amount
                print("Amount Updated! ")

def view_all_expenses(data):
    total_money_spent = 0
    print("ALL EXPENSES")
    print("="*85)
    print("%-10s | %-15s | %-30s | %-15s"% ("Index", "Date", "Category", "Amount"))
    print("="*85)
    for d in data:
        total_money_spent = total_money_spent + float(d["amount"])
        print("%-10d | %-15s | %-30s | %-15.2f" % (d["index"], d["date"], d["category"], d["amount"]))
    print("="*85)
    print("Total Money Spent: %53.2f" % total_money_spent)

def view_grouped_expenses(data):
    print_all_categories()
    group = int(input("Choose category to view expenses: "))
    cat = get_cat_from_int(group)
    total_money_spent = 0
    print("="*85)
    print("%-10s | %-15s | %-30s | %-15s"% ("Index", "Date", "Category", "Amount"))
    print("="*85)
    for d in data:
        if d['category'] == cat:
            total_money_spent = total_money_spent + float(d["amount"])
            print("%-10d | %-15s | %-30s | %-15.2f" % (d["index"], d["date"], d["category"], d["amount"]))
    print("="*85)
    print("Total Money Spent on %-15s: %30.2f" % (cat, total_money_spent))

def calculate_total_spending(data):
    category_totals = {
        "housing_and_utilities": 0,
        "food":0,
        "transportation":0,
        "health":0,
        "family_care":0,
        "entertainment":0,
        "emi_or_loans":0,
        "miscellaneous":0
    }

    for d in data:
        if d["category"] == "housing_and_utilities":
            category_totals["housing_and_utilities"] += d["amount"]
        elif d["category"] == "food":
            category_totals["food"] += d["amount"]
        elif d["category"] == "transportation":
            category_totals["transportation"] += d["amount"]
        elif d["category"] == "health":
            category_totals["health"] += d["amount"]
        elif d["category"] == "family_care":
            category_totals["family_care"] += d["amount"]
        elif d["category"] == "entertainment":
            category_totals["entertainment"] += d["amount"]
        elif d["category"] == "emi_or_loans":
            category_totals["emi_or_loans"] += d["amount"]
        elif d["category"] == "miscellaneous":
            category_totals["miscellaneous"] += d["amount"]

    return category_totals

def main():
    data = loadData()
    while True:
        show_menu()
        choice = get_choice()
        if choice == 1:
            add_expense(data)
            saveData(data)
        elif choice == 2:
            remove_expense(data)
            saveData(data)
        elif choice == 3:
            edit_expense(data)
            saveData(data)
        elif choice == 4:
            view_all_expenses(data)
        elif choice == 5:
            view_grouped_expenses(data)
        elif choice == 6:
            dict = calculate_total_spending(data)
            print("%-25s | %-30s" % ("Category Type", "Total Amount Spent"))
            print("=" * 50)
            for category_type, total_amount in dict.items():
                print("%-25s | %-10.2f" % (category_type, total_amount))
        else:
            print("Personal Expense Tracker (c) 2026")
            break

main()
