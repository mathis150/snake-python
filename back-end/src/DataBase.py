import mysql.connector as mysql
from dotenv import load_dotenv
import os

class DataBase:
    def __init__(self, host, user, password, database):
        self.load_dotenv()
        self.__host = os.getenv('DATABASE_HOST', host)
        self.__user = os.getenv('DATABASE_USER', user)
        self.__password = os.getenv('DATABASE_PASSWORD', password)
        self.__database = os.getenv('DATABASE_NAME', database)
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database
            )
            print("Connection to the database was successful.")
        except mysql.Error as err:
            print(f"Error: {err}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to the database was closed.")