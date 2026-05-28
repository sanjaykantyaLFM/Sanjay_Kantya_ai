import json


def show_menu():
    print("Expenses:")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. delete expenses")
    print("4. Filter Expenses")
    print("5. Exit")




def add_expense():
    title = input("Enter expense title: ")

    while True:
        try:
            amount = float(input("Enter expense amount: "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    new_expense = {
        "title": title,
        "amount": amount
    }

    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    expenses.append(new_expense)

    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

    print("Expense added successfully!")






def view_expenses():
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)

        if not expenses:
            print("No expenses found.")
            return

        total = 0

        print("\nYour Expenses:")
        for expense in expenses:
            print(f"Title: { expense['title'] }, Amount: ₹{expense['amount']}")
            total += expense["amount"]

        print(f"\nTotal Expenses: ₹{total}")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No expense data available.")



def delete_expense():
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
        
        if not expenses:
            print("No expenses to delete")
            return

        print("\nexpenses list")
        for index, expense in enumerate(expenses , start = 1):  # enumarate give number to list
            print(f"{index}. {expense['title']} - {expense['amount']}")

        try:
            choice = int(input("Enter expense num to delete"))

            if choice < 1 or choice > len(expenses):
                print("print invalid no. ")
                return 

            deleted_expense = expenses.pop(choice -1)

            with open("expenses.json", "w") as file:
                json.dump(expenses, file, indent = 4)
            
            print(f"{deleted_expense['title']} deleted successfully!")
        
        except ValueError:
            print("Please enter a valid number")
    
    except (FileNotFoundError, json.JSONDecodeError):
        print("No expense data available")
        
def filter_expenses():
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)

        if not expenses:
            print("No expenses found.")
            return

        keyword = input("Enter title to search: ").lower()

        filtered = []

        for expense in expenses:
            if keyword in expense["title"].lower():
                filtered.append(expense)

        if not filtered:
            print("No matching expenses found.")
            return

        print("\nMatching Expenses:")
        for expense in filtered:
            print(f"{expense['title']} - ₹{expense['amount']}")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No expense data available.")

        

while True:
    show_menu()
    choice = int(input("Enter choice:"))

    if choice == 1:
        add_expense()
        #print("add expense Selected")
    elif  choice == 2:
        view_expenses()
        #print("view Expense Selected")
    elif choice == 3:
        delete_expense()
        # print("delete expense")
    
    elif choice == 4:
        filter_expenses()

    elif choice == 5:
        print("Exit the loop")
        break
    
    else:
        print("Invalid choice")

