from AddressBook import AddressBook, Record, Address, Birthday
from SortFunc import sorting
from Levenshtein import ratio
import os

if os.path.exists(os.path.join(os.path.dirname('.'), 'AddressBook.dat')):
    addressbook = AddressBook.read_from_file('AddressBook.dat')
else:
    addressbook = AddressBook()

def corrector(handler):
    def wrapper(*args, **kwargs):
        try:
            result = handler(*args, **kwargs)
            return result
        except KeyError:
            return 'Enter user name.'
        except ValueError as e:
            return e.args[0]
        except IndexError:
            return 'Give me name and phone'
        except TypeError:
            return 'Give me name and phone'
    return wrapper
@corrector
def hello():
    return "Hello! How can I help you?"

@corrector
def add_new_contact(data):
    name, *_ = create(data)
    record_add = Record(name)
    addressbook.add_record(record_add)
    return f'New contact {name}'

@corrector
def delete(data):
    name, *_ = create(data)
    if addressbook.delete_name(name) is True:
        return f'{name} has been deleted'
    else:
        return 'The phone number not exist'

@corrector
def add_phones(data):
    name, phone = create(data)
    if name in addressbook:
        record_add_phones = addressbook.data[name]
        record_add_phones.add_phone(phone)
    else:
        record_add_phones = Record(name, phone)
        addressbook.add_record(record_add_phones)
    return f"{addressbook.data[name].name.value} : {list(map(lambda x: x.value, addressbook.data[name].phones))}"

@corrector
def add_emails(data):
    name, email = create(data)
    record_add_emails = addressbook.data[name]
    record_add_emails.add_email(email)
    return f"In contact {name} successfully add email {email}"

@corrector
def add_birthdays(data):
    name, birthday = create(data)
    record_add_birthdays = addressbook.data[name]
    record_add_birthdays.add_birthday(birthday)
    return f"In contact {name} successfully add birthday {birthday}"
@corrector
def add_addresses(data):
    name, address = create(data)
    record_add_addresses = addressbook.data[name]
    record_add_addresses.add_address(address)
    return f"In contact {name} successfully add adress {address}"
# add_address / (data) Maria 08021 м.Київ, в.Гончара, add_address maria 65125 м.Одеса, в.Вільямса

    

def delete_phone(data):
    name, old_phone = create(data)
    record = addressbook.data[name]
    record.delete_phone(old_phone)
    return f'In contact {name} successfully deleted phone {old_phone}'


def delete_email(data):
    name, *_ = create(data)
    record = addressbook.data[name]
    record.delete_email()
    return f'In contact {name} successfully deleted email '

def delete_birthday(data):
    name, *_ = create(data)
    record = addressbook.data[name]
    record.delete_birthday()
    return f'In contact {name} successfully deleted birthday '
    
def delete_address(data):
    name, *_ = create(data)
    record = addressbook.data[name]
    record.delete_address()
    return f'In contact {name} successfully deleted address '

def birthday(data):
    days, *_ = create(data)
    if days.isdigit():
        names = addressbook.show_birthday(int(days))
        return f'after {days} days birthday for {names}'
    else:
        return 'Enter number of days'

def create(data):
    data = data.strip().split()
    lst_data = [data[0]]
    if len(data) > 1:
        lst_data.append(' '.join(data[1:]))
    return tuple(lst_data)




@corrector
def answer_exit():
    return 'Good bye!'

@corrector
def command_error(user_command = ''):
    similar_answer =  {ratio(user_command, key) : key for key in COMMANDS}
    similar_answer = sorted(similar_answer.items(), reverse=True)
    return f'Wrong command. May be you wont to write "{similar_answer[0][1]}", please try again.'

def get_answer_function(answer):
    return COMMANDS.get(answer, command_error)


COMMANDS = {
    'hello': hello,
    'add_name': add_new_contact,
    'add_phone': add_phones,
    'delete': delete,
    'add_email': add_emails,
    'add_birthday': add_birthdays,
    'add_address': add_addresses,
    'delete_birthday': delete_birthday,
    'search_contact': addressbook.search_contact,
    'add_note': addressbook.add_note,
    'add_desc_to_note': addressbook.add_desc_to_note,
    'replace_desc_of_note': addressbook.add_desc_to_note,
    'search_notes_by_name': addressbook.search_notes_by_name,
    'add_tag_to_note': addressbook.add_tag_to_note,
    'search_note_by_tags': addressbook.search_notes_by_tags,
    'delete_note': addressbook.remove_note,
    'delete_phone': delete_phone,
    'delete_email': delete_email,
    'delete_address': delete_address,
    'sort_func': sorting,
    'birthday': birthday,
    'close': answer_exit 
}



@corrector
def run_command(user_command):
    command = user_command
    params = ''
    for key in COMMANDS:
        if user_command.lower().startswith(key + ' '):
            command = key
            params = user_command[len(command):]
            break
    if params:
        return get_answer_function(command)(params.strip())
    else:
        answer_function = get_answer_function(command)
        if answer_function == command_error:
            return answer_function(user_command)
        else:
            return answer_function()



def main():
    while True:
        user_command = input('Введіть команду для бота: ')
        answer = run_command(user_command.strip())
        print(answer)
        if answer == 'Good bye!':
            break
    addressbook.save_to_file('AddressBook.dat')

if __name__ == '__main__':
    main()
