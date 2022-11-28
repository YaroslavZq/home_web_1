from datetime import date, datetime
from collections import UserDict
from re import search, match
import pickle

class AddressBook(UserDict):

    def __init__(self, data = None):
        super().__init__(data)
        self.notes = []

    def add_record(self, record):
        self.data[record.name.value] = record
        return 'Record was added'

    def return_record_by_name(self, name):
        return self.data[name]

    def remove_record(self, record):
        del self.data[record.name.value]
        return 'Record was deleted'

    def search_contact(self, name):
        if name in self.data:
            record = self.data[name]
            return f'{record}'
        else:
            return 'Contact not found'


    def add_note(self, note, description = None, tag = None):
        self.notes.append(Note(note, description, tag.lower() if tag else ''))
        return f'Note "{note}" was create'

    def add_desc_to_note(self, note):
        for book_note in self.notes:
            if not note.startswith(book_note.note):
                continue
            description = note[len(book_note.note):].strip()
            book_note.description = description
            return 'description is added'
        return 'Note not found'

    def add_tag_to_note(self, note):
        for book_note in self.notes:
            if not note.startswith(book_note.note):
                continue
            tags = note[len(book_note.note):].strip()
            lst_tags = book_note.tags.split(',')
            lst_tags.extend([tag.strip() for tag in tags.lower().split(',')])
            lst_tags.sort()
            book_note.tags = ','.join(tag for tag in lst_tags if tag != '')
            return 'Tags is added'
        return 'Note not found'

    def search_notes_by_tags(self, tags):
        tags_answer = []
        lst_tags = tags.split(',')
        lst_tags = [item.lower() for item in lst_tags if item != '']
        for book_note in self.notes:
            if set(book_note.tags.split(',')) & set(lst_tags) == set(lst_tags):
                tags_answer.append(book_note)
        return tags_answer or f'Tags {tags} not found'

    def sort_notes_by_tags(self):
        self.notes = sorted(self.notes, key=lambda x: x.tags)

    def search_notes_by_name(self, note):
        for book_note in self.notes:
            if book_note.note == note:
                return book_note
        return 'Note not found'

    def remove_note(self, note):
        book_note = self.search_notes_by_name(note)
        if book_note:
            self.notes.remove(book_note)
            return 'Note was removed'
        else:
            return 'Note not found'

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def read_from_file(cls, filename):
        with open(filename, "rb") as file:
            content = pickle.load(file)
        return content

    def delete_name(self, name):  
        if name in self.data:
            del self.data[name]
            return True

    def show_birthday(self, user_input):
        s = []
        for name, record in self.data.items(): 
            if record.days_to_birthday() == user_input:
                s.append(name)       
            else:
                continue
        return ', '.join(s)

class Record():
    def __init__(self, name, phone = None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.email = None
        self.birthday = None
        self.address = None
       
    def __repr__(self) -> str:
        phones = ', '.join([phone.value for phone in self.phones if not phone.value is None])
        name = self.name
        email = self.email or ''
        birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else ''
        address = self.address or ''
        return f'{name} : phones {phones}, email: {email}, birthday: {birthday}, address: {address}'

    def add_phone(self, phone):
        for rec_phone in self.phones:
            if rec_phone.value == phone:
                raise ValueError("""This contact {self.name} 
                            already have phone : {phone}
                            if you want to change tis date try "change_email | new_email"
                            """)                
        self.phones.append(Phone(phone))


    def delete_phone(self, phone):
         for rec_phone in self.phones:
            if not rec_phone.value == phone:
                continue
            self.phones.remove(rec_phone)
            return True
    
    


    def add_email(self, email):
        if self.email is None:
            self.email = Email(email)
        else:
            raise ValueError("""This contact {self.name} 
            already have date of email: {self.email}
            if you want to change tis date try "change_email | new_email"
            """)


    def delete_email(self):
        self.email = None
        return True

    def add_birthday(self, birthday):
        if birthday:
            self.birthday = Birthday(birthday)
            return 'Birthday {self.name.value} is changed'
        else:
            raise('Enter a birthday')


    def delete_birthday(self):
        self.birthday = None
        return True

    def delete_address(self):
        self.address = None
        return True


    def add_address(self, address):
        if self.address is None:
            self.address = Address(address)
        else:
            raise ValueError("""This contact {self.name} 
            already have date of address: {self.address}
            if you want to change tis date try "change_address | new_address"
            """)
 

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            if self.birthday.value.replace(year=today.year) >= today:
                result = self.birthday.value.replace(year=today.year) - today
            else:
                result = self.birthday.value.replace(
                    year=today.year) - today.replace(year=today.year - 1)
            return result.days
        else:
            return 'Empty'        

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __repr__(self) -> str:
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Address(Field):

    @Field.value.setter
    def value(self, value):
        if value:
            self._value = self.check_address(value)
        else:
            self._value = ''

    @staticmethod
    def check_address(value):
        clean_address = (
                        value.strip()
                        .replace("(", "")
                        .replace(")", "")
                        .replace("-", "")
                        .replace(" ", "")
                        .replace(",", " ")
                    )
        match_value = search(r"\d{5}\ \м.\w+\ \в.\w+(\d+|\D+)+", clean_address)
        if not match_value:
            raise ValueError(f"Invalide address format {clean_address}. Address format should be IIII, м.Місто, в.Вулиця, дод.записи")
        return str(value)

class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        self._value = self.check_date(value)

    @staticmethod
    def check_date(value):
        value = value.strip()

        for separator in (".", ",", "-", ":", "/"):
            value, *args = value.split(separator)

            if args:
                break

        if not args or len(args) > 2:
            raise ValueError("Invalide date format. Date format should be YYYY.MM.DD or DD.MM.YYYY.")

        if int(value) > 31:
            return date(int(value), int(args[0]), int(args[1]))

        return date(int(args[1]), int(args[0]), int(value))

class Phone(Field):

    def __repr__(self):
        return self.value


    @Field.value.setter
    def value(self, value:str):
        if not all((value.startswith('+380'), len(value) == 13, value[1:].isdigit())):
            raise ValueError(f"""Phone number {value} is not valid, 
            please enter correcct phone '+380XXXXXXX'""")
        self._value = value



class Email(Field):
    
    @Field.value.setter
    def value(self, value:str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (match(regex, value)):
            raise ValueError(f""""Email {value} is not valid,
            please enter correct email.
            Example of emails: my.ownsite@our-earth.org
                                ankitrai326@gmail.com""")
        self._value = value

class Name(Field):
    pass

class Note:
    def __init__(self, note, description = '', tags= ''):
        self.note = note
        self.description = description if description else ''
        self.tags = ','.join((tag for tag in tags.split(' '))) if tags else ''

    def __repr__(self) -> str:
        return f'{self.note}: {self.description} ({self.tags})'
          
