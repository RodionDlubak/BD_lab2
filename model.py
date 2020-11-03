import psycopg2
from pprint import pprint


class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname = 'lab1' user='postgres' host='127.0.0.1' password='03rod06ion01' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Cannot connect to database")

    def get_column_names(self):
        return [d[0] for d in self.cursor.description]

    def showtable(self, tablename, condition):
        try:
            query = f'SELECT * FROM {tablename}'

            if condition:
                query += ' WHERE ' + condition

            self.cursor.execute(query)
            return self.get_column_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

        self.cursor.close()

    def insert(self, tablename, columns,  new_record):
        try:
            query = f'INSERT INTO {tablename} ({columns}) VALUES ({new_record});'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

        #self.cursor.close()

    def delete(self, tablename, condition):
        try:
            query = f'DELETE FROM {tablename} WHERE {condition};'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def update(self, tablename, condition, statement):
        try:
            query = f'UPDATE {tablename} SET {statement} WHERE {condition}'

            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def get_table_id(self, tablename):
        try:
            query = f'SELECT {tablename}_id FROM {tablename}'

            self.cursor.execute(query)
            return self.get_column_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def get_accounts_and_games(self, condition):
        try:
            query = f'''
                    SELECT * from account
                    JOIN game on account_id=account'''
            if condition:
                query += condition
            self.cursor.execute(query)
            return self.get_column_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def get_games_and_items(self, condition):
        try:
            query = f'''
                    SELECT * from game
                    JOIN item on game_id=game'''
            if condition:
                query += condition
            self.cursor.execute(query)
            return self.get_column_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def get_accounts_games_and_items(self, condition):
        try:
            query = f'''
                    SELECT * from account
                    JOIN game on account_id=account
                    JOIN item on game_id=game'''
            if condition:
                query += condition
            self.cursor.execute(query)
            return self.get_column_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def fill_account_with_random_data(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomAccounts()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > 10;
                INSERT INTO account (login, password, created)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 10),
					timestamp '2014-01-10 20:00:00' + random() * (timestamp '2020-12-30 20:00:00' - timestamp '2014-01-10 10:00:00'));
					step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomAccounts();
        """
        try:
            self.cursor.execute(sql)
        finally:
            self.connection.commit()



