from record import Record
from adressbook import AddressBook
from datetime import datetime


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone(s) please."
        except IndexError:
            return "Give me name"
        except KeyError:
            return "There is no such name in the contact list"
        except AssertionError: 
            return "Phone should include 10 digits"

    return inner

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error    
def change_username_phone(args, book: AddressBook):
    # if len(args) < 3:
    #     raise ValueError("Not enough values to change phone. Usage: change <name> <old phone> <new phone>")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        # try:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
        # except ValueError as e:
        #     return str(e)
    else:
        return "Contact not found."

@input_error
def phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        if record.phones:
            return ', '.join(phone.value for phone in record.phones)
        else:
            return "No phone numbers available for this contact."
    else:
        return "Contact not found."
    
def all(book):
    list = []
    for name, record in book.items():
        list.append(f"{name}: {', '.join(phone.value for phone in record.phones)}")
    return list


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        if record.birthday:
            return "Record already has date of Birth"
        else:
            record.add_birthday(birthday)
            return "Birthday added"
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday is {record.birthday.value.strftime("%d.%m.%Y")}"
        else:
            return "Record hasn't Birthday"
    else:
        return "Contact not found."

nowday = datetime.now()

@input_error
def birthdays(book):
    upcoming_birthdays_list = []
    for name, record in book.items():
        if record.birthday:
            this_year_birthday = record.birthday.value.replace(year=nowday.year)
            difference = (nowday - this_year_birthday).days
            if difference >= -7 and difference <= 0:
                upcoming_birthdays_list.append(f"{name}'s birthday is coming up on {this_year_birthday.strftime("%d.%m.%Y")}")
    return upcoming_birthdays_list



def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_username_phone(args, book))
        elif command == "phone":
            print(phone(args, book))
        elif command == "all":
            print(all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()