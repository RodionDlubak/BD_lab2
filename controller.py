from consolemenu import *
from consolemenu.items import *
from model import Model
from view import View

TABLES_NAMES = ['account', 'game', 'item']
TABLES = {
'account': ['account_id', 'login', 'password', 'created'],
'game': ['game_id', 'game_name', 'hours_played', 'account'],
'item': ['item_name', 'price', 'game', 'item_id']
}


def getInput(msg, tableName=''):
    print(msg)
    if tableName:
        print(' | '.join(TABLES[tableName]), end='\n\n')
    return input()


def getInsertInput(msg, tableName):
    print(msg)
    print(' | '.join(TABLES[tableName]), end='\n\n')
    return input(), input()


def pressEnter():
    input()


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_main_menu(self, msg=''):
        menu = SelectionMenu(TABLES_NAMES + ['Get accounts and games'] +
                                            ['Get games and items'] +
                                            ['Get accounts, games and items'] +
                                            ['Fill table "account" with random data (10 items)'], "Main menu", msg)
        menu.show()

        index = menu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == 3:
            self.get_accounts_and_games()
        elif index == 4:
            self.get_games_and_items()
        elif index == 5:
            self.get_accounts_games_and_items()
        elif index == 6:
            self.fillByRandom()
        else:
            print('Goodbye')

    def show_entity_menu(self, tableName, msg=''):
        options = ['Get', 'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        selectionMenu = SelectionMenu(options, f'Name of table: {tableName}', msg,
        exit_option_text='Back')
        selectionMenu.show()
        try:
            function = functions[selectionMenu.selected_option]
            function(tableName)
        except IndexError:
            self.show_main_menu()

    def get(self, tableName):
        try:
            condition = getInput(
            f'GET {tableName}\nEnter condition (SQL) or leave empty:', tableName)
            data = self.model.showtable(tableName, condition)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def insert(self, tableName):
        try:
            columns, values = getInsertInput(
            f"INSERT {tableName}\nEnter colums divided with commas, then do the same for values in format: ['value1', 'value2', ...]", tableName)

            self.model.insert(tableName, columns, values)
            self.show_entity_menu(tableName, 'Inserted successfully')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def delete(self, tableName):
        try:
            condition = getInput(
            f'DELETE {tableName}\n Enter condition (SQL):', tableName)
            self.model.delete(tableName, condition)
            self.show_entity_menu(tableName, 'Deleted successfully')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def update(self, tableName):
        try:
            condition = getInput(
            f'UPDATE {tableName}\nEnter condition (SQL):', tableName)
            statement = getInput(
            "Enter SQL statement in format [<key>='<value>']", tableName)

            self.model.update(tableName, condition, statement)
            self.show_entity_menu(tableName, 'Updated successfully')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def get_accounts_and_games(self):
        try:
            print(f"GET accounts and games\nEnter date of creation range. First date (like: '2020-01-01'),"
                  f" then second (like: '2020-10-10') or leave empty")
            created = input()
            if created:
                created2 = input()
            print(f"Enter game name (like: 'CS:GO') or leave empty")
            game_name = input()
            print(f"Enter game hours range. First number (like: '1200'), "
                  f" then second (like: '2000') or leave empty")
            hours_played = input()
            if hours_played:
                hours_played2 = input()

            condition = ''
            flag = 0
            if created:
                condition = f" WHERE NOT (created > '{created2}' OR created < '{created}')"
                flag = 1
            if game_name:
                if flag == 1:
                    condition += f" AND game_name='{game_name}'"
                else:
                    condition = f" WHERE game_name='{game_name}'"
                    flag = 1
            if hours_played:
                if flag == 1:
                    condition += f" AND NOT (hours_played > '{hours_played2}' OR hours_played < '{hours_played}')"
                else:
                    condition = f" WHERE NOT (hours_played > '{hours_played2}' OR hours_played < '{hours_played}')"

            data = self.model.get_accounts_and_games(condition)
            self.view.print_2(data)
            pressEnter()
            self.show_main_menu()
        except Exception as err:
            self.show_main_menu(str(err))

    def get_games_and_items(self):
        try:
            print(f"GET games and items\nEnter game name (like: 'CS:GO') or leave empty")
            game_name = input()
            print(f"Enter game hours range. First number (like: '1200'), "
                  f" then second (like: '2000') or leave empty")
            hours_played = input()
            if hours_played:
                hours_played2 = input()
            print(f"Enter item price. First number (like: '10'), "
                  f" then second (like: '1000') or leave empty")
            price = input()
            if price:
                price2 = input()

            condition = ''
            flag = 0
            if game_name:
                condition = f" WHERE game_name='{game_name}'"
                flag = 1
            if hours_played:
                if flag == 1:
                    condition += f" AND NOT (hours_played > '{hours_played2}' OR hours_played < '{hours_played}')"
                else:
                    condition = f" WHERE NOT (hours_played > '{hours_played2}' OR hours_played < '{hours_played}')"
                    flag = 1
            if price:
                if flag == 1:
                    condition += f" AND NOT (price > '{price2}' OR price < '{price}')"
                else:
                    condition = f" WHERE NOT (price > '{price2}' OR price < '{price}')"
            data = self.model.get_games_and_items(condition)
            self.view.print_2(data)
            pressEnter()
            self.show_main_menu()
        except Exception as err:
            self.show_main_menu(str(err))

    def get_accounts_games_and_items(self):
        try:
            print(f"GET accounts, games and items\nEnter date of creation range. First date (like: '2020-01-01'),"
                  f" then second (like: '2020-10-10') or leave empty")
            created = input()
            if created:
                created2 = input()
            print(f"Enter game name (like: 'CS:GO') or leave empty")
            game_name = input()
            print(f"Enter game hours range. First number (like: '1200'), "
                  f" then second (like: '2000') or leave empty")
            hours_played = input()
            if hours_played:
                hours_played2 = input()
            print(f"Enter item price. First number (like: '10'), "
                  f" then second (like: '1000') or leave empty")
            price = input()
            if price:
                price2 = input()

            condition = ''
            flag = 0
            if created:
                if flag == 1:
                    condition += f" AND NOT (created > '{created2}' OR created < '{created}')"
                else:
                    condition = f" WHERE NOT (created > '{created2}' OR created < '{created}')"
                    flag = 1
            if game_name:
                condition = f" WHERE game_name='{game_name}'"
                flag = 1
            if hours_played:
                if flag == 1:
                    condition += f" AND NOT (hours_played > '{hours_played2}' OR hours_played < '{hours_played}')"
                else:
                    condition = f" WHERE NOT (hours_played > '{hours_played2}' OR hours_played < '{hours_played}')"
                    flag = 1
            if price:
                if flag == 1:
                    condition += f" AND NOT (price > '{price2}' OR price < '{price}')"
                else:
                    condition = f" WHERE NOT (price > '{price2}' OR price < '{price}')"

            data = self.model.get_accounts_games_and_items(condition)
            self.view.print_3(data)
            pressEnter()
            self.show_main_menu()
        except Exception as err:
            self.show_main_menu(str(err))

    def fillByRandom(self):
        try:
            self.model.fill_account_with_random_data()
            self.show_main_menu('Generated successfully')

        except Exception as err:
            self.show_main_menu(str(err))

