#-*- coding: utf-8 -*-
import pymysql
# import getpass
#from Conn_Package.password import passwrd, db
from Conn_Package.connection import conn

class DBconn:
    def __init__(self):
        self.conn=conn
        self.cursor = self.conn.cursor()
        print('Połączenie ustanowione.\n'+
        '__________    _____  __________  _____ \n'+
        '\______   \  /  _  \ \____    / /  _  \ \n'+                                        
        ' |    |  _/ /  /_\  \  /     / /  /_\  \ \n'+                                        
        ' |    |   \/    |    \/     /_/    |    \  \n'+                                      
        ' |______  /\____|__  /_______ \____|__  /    \n'+                                    
        '        \/         \/        \/       \/       \n'+                                  
        ' ______________________________________________________________________  __      __  ____ \n'+
        '/   _____/\______   \______   \____    /\_   _____/\__    ___/\_____  \/  \    /  \/  _  \  \n'+
        '\_____  \  |     ___/|       _/ /     /  |    __)_   |    |    /   |   \   \/\/   /  /_\  \ \n'+
        '/        \ |    |    |    |   \/     /_  |        \  |    |   /    |    \        /    |    \ \n'+
        '/_______  /|____|    |____|_  /_______ \/_______  /  |____|   \_______  /\__/\  /\____|__  / \n'+
        '        \/                  \/        \/        \/                    \/      \/         \/')
                
        
        while(True):
            choice = input('Co chcesz zrobić? [Z]zaloguj [Q]wyjdz ')
            if (choice.upper() == 'Z'):
                self.log_in()
            elif (choice.upper() == 'Q'):
                print('Wylogowano.')
                self.conn.close()
                break
            
    def log_in(self):
        user_email = input('Podaj email: ')
        user_passwd = input('Podaj hasło: ')
        self.cursor.execute("SELECT k.imie, k.nazwisko, k.uprawnienia, k.email as email FROM klubowicze as k JOIN logowanie as l where l.haslo COLLATE utf8_bin ='"
                             +user_passwd+"' and (k.email = l.email);")
        
        results = self.cursor.fetchall()
        
#        nie przepuszcza niepoprawnego emaila (Case sensitive) ale brakuje monitu tak jak z emailem
#        
       
        for row in results:
            imie = row[0]
            nazwisko = row[1]
            uprawnienia = row[2]
            email = row[3]
#             print ('%-15s| %-20s| %-12s| %-20s' % (imie, nazwisko, uprawnienia, email))
            if (email == user_email):
                print('Witaj '+imie+'!\n')
                print('%-15s| %-20s| %-12s| %-20s' %('Imie', 'Nazwisko','uprawnienia','email'))
                print ('%-15s| %-20s| %-12s| %-20s' % (imie, nazwisko, uprawnienia, email))
            else: 
                print('Niepoprawny email')
#                 self.conn.close()
            break
            
        
#         print("%3s \t| %20s \t|%20s \t|%20s" %('Imie', 'Nazwisko','uprawnienia','email'))
    
  
        

o1=DBconn()
