import argparse
import json
import os
import datetime
import calendar
import csv

def load_expenses():
    if not os.path.exists("expenses.json"):
        return[]
    try:
        with open("expenses.json","r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("error: expense.json is corrupted. Starting with empty json file")
        return []
def check_amount(amount):
    if amount < 0:
        print ("amount can't be negative")
        return False
    return True


def save_expenses(expenses):
    with open("expenses.json","w") as file:
        json.dump(expenses,file,indent=2)

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def add_expense(args):
    loaded_expenses = load_expenses()
    new_Id = max ((i['id'] for i in loaded_expenses),default=0)+1
    date = now()
    if not check_amount(args.amount):
        return
    expense = {
        "id": new_Id,
        "date": date,
        "description": args.description,
        "amount": args.amount,
    }
    loaded_expenses.append(expense)
    save_expenses(loaded_expenses)
    print(f"sucessfully added expense id:{new_Id}")


def delete_expense(args):
    loaded_expenses = load_expenses()
    for i,expense in enumerate(loaded_expenses):
        if expense['id'] == args.id:
            del loaded_expenses[i]
            print(f"Sucessfully deleted id {args.id}")
            save_expenses(loaded_expenses)
            return
    print (f"Id not Found:{args.id}")


def list_expense(args):
    loaded_expenses= load_expenses()
    if not loaded_expenses:
        print("No expenses found")
        return
    print(f"{'ID':<5} {'Date':<26}{'Description':<20} {'Amount'}")

    for e in loaded_expenses:
        print(f"{e['id']:<5} {e['date']:<26} {e['description']:<20} ${e['amount']:.2f}")


def update_expense(args):
    loaded_expense = load_expenses()
    for e in loaded_expense:
        if e['id'] == args.id:
            if args.description is not None:
                e['description'] = args.description
            if args.amount is not None:
                if not check_amount(args.amount):
                    return
                e['amount'] = args.amount
            save_expenses(loaded_expense)
            print("Sucessfully updated the expense")
            return
    print("error: not found")
    return

def summary_expense(args):
    loaded_expense = load_expenses()
    total_amount = 0

    if args.month is not None:
        if not (1 <= args.month <= 12): 
            print("Error: Invalid month") 
            return    
        current_year = datetime.datetime.now().year
        for e in loaded_expense:
            date_obj = datetime.datetime.strptime(e['date'],"%Y-%m-%d")
            if date_obj.month == args.month and date_obj.year == current_year:
                total_amount += e['amount']

           
        month_name = calendar.month_name[args.month]
        print(f"Total expense for {month_name} : ${total_amount:.2f}")
    else:
        for e in loaded_expense:
           total_amount += e['amount']
        print(f"total expenses  ${total_amount:.2f}")


def export_expense(args):
    expenses = load_expenses()
    if not expenses:
        print("no Expenses to export")
        return
    with open (args.filename,"w",newline='') as file:
        #getting dictionary keys to use as headers
        headers = expenses[0].keys()
        #initializing the writer
        writer = csv.DictWriter(file, fieldnames=headers)

        #writing the header row
        writer.writeheader()
        #writing the data row
        writer.writerows(expenses)
    

def parse_command():
    parser = argparse.ArgumentParser(description="tracks expenses")
    subparsers = parser.add_subparsers(dest= "command")

    #add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required = True)
    add_parser.add_argument("--amount", type=float, required=True)

    #delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type = int, required = True)

    # update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id",required=True, type=int)
    update_parser.add_argument("--description", required=False)
    update_parser.add_argument("--amount",required=False,type=float)

    #list
    list_parser = subparsers.add_parser("list")

    #summary
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", required=False, type=int)

    #export
    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--filename",required= False, default="expenses.csv")


    args = parser.parse_args()
    return args, parser


def main():
    args, parser =parse_command()
    if args.command =="add":
        add_expense (args)
    elif args.command == "delete":
        delete_expense(args)
    elif  args.command == "list":
        list_expense(args)
    elif args.command == "update":
        update_expense(args)

    elif args.command == "summary":
        summary_expense(args)

    elif args.command == "export":
        export_expense(args)
    
    else:
        parser.print_help()

        
if __name__ == "__main__":
    main()
