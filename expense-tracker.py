import argparse
import json
import os

def load_expenses():
    if not os.path.exists("expenses.json"):
        return[]
    try:
        with open("expenses.json","r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("error: expense.json is corrupted. Starting with empty json file")
        return []

def save_expenses(expenses):
    with open("expenses.json","w") as file:
        json.dump(expenses,file,indent=2)

def add_expense(args):
    print("adding")

def delete_expense(args):
    print("deleting")

def update_expense(args):
    print("updating")

def summary_expense(args):
    print ("summary")

def list_expense(args):
    print("listing")

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
    update_parser.add_argument("--amount",required=False,type=float)

    #list
    list_parser = subparsers.add_parser("list")

    #summary
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", required=False, type=int)

    args = parser.parse_args()
    return args


def main():
    args =parse_command()
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


        
if __name__ == "__main__":
    main()
