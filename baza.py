#-*- coding: utf-8 -*-
import pymysql
import getpass
#from Conn_Package.password import passwrd, db
from Conn_Package.connection import conn

class DBconn:
    def __init__(self):
        self.conn=conn
        self.cursor = self.conn.cursor()
        print('Połączenie ustanowione')
        while(True):
            choice = input('Co chcesz zrobić? [Z]zaloguj [Q]wyjdz')
            if (choice.upper() == 'Z'):
                self.log_in()
            elif (choice.upper() == 'Q'):
                print('Zamykam połączenie')
                self.conn.close()
                break
            
    def log_in(self):
        user_email = input('Podaj email: ')
        user_passwd = getpass.getpass('Podaj haslo: ', '********')
        self.cursor.execute('SELECT * FROM logowanie;')
        results = self.cursor.fetchall()
        
        print("%3s \t| %20s \t|%20s \t|%20s" %('Id', 'Imie', 'Nazwisko','Pozycja'))
            

