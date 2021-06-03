#!/usr/bin/env python3
import sys

# Record is used to store each record input by the user
class Record:
    """Represents a record."""
    def __init__(self, category, item, money):
        self._category = category
        self._item = item
        self._money = money
    @property
    def category(self):
        return self._category
    @property
    def item(self):
        return self._item
    @property
    def money(self):
        return self._money

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""

    def __init__(self):
        try:
            with open('records.txt', 'r') as fh:
                lis = fh.read().splitlines()        # lis is a list in the form ['total', 'category item money', 'category2 item2 money2', ...]
                self._initial_money = int(lis[0])
                self._records = lis[1:]
                print('Welcome back!')
        except FileNotFoundError:
            try:
                self._initial_money = int(input('How much money do you have? '))
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default.')
                self._initial_money = 0
            self._records = []

    def add(self, record, categories):        # record is in the form 'category item money'
        """This is a method that can add record. Please enter in the form 'category item money'."""

        t = record.split()      # t is a temporary list in form of ['category', 'item', 'money']
        if len(t) != 3:
            sys.stderr.write('The format of a record should be like this: meal breakfast -50.\n'\
                'Fail to add a record.\n')
        else:
            r = Record(t[0], t[1], t[2])          # r is an object created by the class Record
            p = categories.is_category_valid(r._category)
            if p != True:
                sys.stderr.write('The specified category is not in the category list.\n'\
                    'You can check the category list by command "view categories".\n'\
                    'Fail to add a record.\n')
            else:
                try:
                    t[2] = int(t[2])
                except ValueError:
                    sys.stderr.write('Invalid value for money. Should be an integer.\nFail to add a record.\n')
                else:
                    self._records.append(record)
    
    def view(self):
        """This is a method that can view all the records."""

        print('Here\'s your expense and income records:\n'+' '*3+'Category'+' '*7+\
            'Description'+' '*4+'Amount\n'+'='*40)
        line = 1
        amount = self._initial_money
        for n in self._records:
            m = n.split()        # m is a list in the form ['category', 'item', 'money']
            print(f'{line:<3}{m[0]:<15}{m[1]:<15}{m[2]}')
            amount += int(m[2])
            line += 1
        print('='*40 + f'\nNow you have {amount} dollars.')
    
    def delete(self, record):
        """This is a method that can delete a record. Please enter in the form 'category item money.
        If there are more than one record, please enter the line of the record being deleted."""

        s = record.split()
        if len(s) != 3:
            sys.stderr.write('The format of the input should be like this: meal breakfast -50.\
                \nFail to delete a record.\n')
        elif self._records.count(record) > 1:
            try:
                d = int(input(f'Which line of the record "{record}" is going to be deleted? '))
                testlist = []
                for i, v in enumerate(self._records):
                    if v == record:
                        testlist.append(i+1)        # testlist contains the records that is identical to the input
                assert d in testlist
            except ValueError:
                sys.stderr.write('Invalid input. Should be an integer.\nFail to delete a record.\n')
            except AssertionError:
                sys.stderr.write(f'Invalid input number. No record of "{record}" in line {d}.\
                    \nFail to delete a record')
            else:
                del(self._records[d-1])
        elif self._records.count(record) == 1:
            self._records.remove(record)
        else:
            sys.stderr.write(f'There\'s no record with "{record}".\nFail to delete a record.\n')
        
    def find(self, lis_sub):
        """This method is used to find records in specific category."""

        if lis_sub == []:
            sys.stderr.write(f'There is no category "{category}".\
                \nYou can check the categories with command "view categories".\n')
        else:
            lis_find = []
            lis_find.extend(list(filter(lambda x:x.split()[0] in lis_sub, self._records)))
            # Print the find result
            if len(lis_find) == 0:
                sys.stderr.write(f'There is no record with category "{category}".\n')
            else:
                total = 0
                print(f'Here\'s your expense and income records under category "{category}":\n'\
                    +' '*3+'Category'+' '*7+'Description'+' '*4+'Amount\n'+'='*40)
                line = 1
                for n in lis_find:
                    m = n.split()        # m is a list in the form ['category', 'item', 'money']
                    print(f'{line:<3}{m[0]:<15}{m[1]:<15}{m[2]}')
                    total += int(m[2])
                    line += 1
                print('='*40 + f'\nThe total amount above is {total}.')
    
    def save(self):
        """This is the method that will write the records to records.txt."""

        print('Bye!')
        try:
            with open('records.txt', 'w') as fh:
                fh.write(str(self._initial_money))
                for n in self._records:
                    fh.write('\n'+n)
        except OSError:
            sys.stderr.write('Cannot open file.\n')

class Categories:
    """Maintain the category list and provide some method."""

    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation',\
        ['bus', 'railway']], 'income', ['salary', 'bonus']]

    def view(self):
        """This is a method that will show all the categories."""

        def view_recurs(cat, level = 0):
            if type(cat) == list:
                for n in cat:
                    view_recurs(n, level + 1)
            else:
                print(f'{" "*2*(level-1)}- {cat}')
        view_recurs(self._categories)
    
    def is_category_valid(self, category):
        """This is a method used in add command to check if the category being added exists."""

        def valid_recurs(categories, target):
            if type(categories) == list:
                for n in categories:
                    p = valid_recurs(n, target)
                    if p == True:
                        return True
            else:
                return categories == target

        return valid_recurs(self._categories, category)

    def find_subcategories(self, category_find):
        """This is a method used in find command to return the subcategories of the category being found."""

        def find_subcategories_gen(category_find, categories, found = False):        # found flag is to indicate if the target is found
            if type(categories) in {list, tuple}:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category_find, child, found)
                    if child == category_find \
                        and index+1 < len(categories) \
                        and type(categories[index+1]) == list:        # Check if child has subcategories
                        yield from find_subcategories_gen(category_find, categories[index+1], True)
            else:
                if categories == category_find or found == True:
                    yield categories

        return list(find_subcategories_gen(category_find, self._categories))

# Processing each command
categories = Categories()
records = Records()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    
    if command == 'add':
        record = input('Add an expense or income record with description and amount: ')
        records.add(record, categories)

    elif command == 'view':
        records.view()

    elif command == 'delete':
        delete_record = input('Which record do you want to delete? ')
        records.delete(delete_record)

    elif command == 'view categories':
        categories.view()

    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)

    elif command == 'exit':
        records.save()
        break
    
    else:
        sys.stderr.write('Invalid command. Try again.\n')