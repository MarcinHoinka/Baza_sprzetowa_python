#-*- coding: utf-8 -*-
import pymysql
# import modules
# import getpass
#from Conn_Package.password import passwrd, db
from Conn_Package.connection import conn

class DBconn:
    def __init__(self):
        self.conn=conn
        self.cursor = self.conn.cursor()
        print(        '_________ \n'+                    
        '\______  \_____  _____________ \n'+                            
        '|    |  _/\__  \ \___   /\__  \ \n'+                       
        '|    |   \ / __ \_/    /  / __ \_ \n'+                     
        '|______  /(____  /_____ \(____  / \n'+                    
        '       \/      \/      \/     \/ \n'+  
        ' _________                           __ \n'+                        
        '/   _____/___________________ ______/  |_  ______  _  _______ \n'+   
        '\_____  \\____   \__  \___   // __  \   __\/  _ \ \/ \/ /\__  \  \n'+
        ' /        \  |_> >  |\/ /   /\  ___/|  | (  <_> )     /  / __ \_ \n'+
        '/_______  /   __/|__|  /_____ \\___  >__|  \____/ \/\_/  (____  / \n'+
        '        \/|__|               \/   \/                         \/ \n'+      
        
        
        
        'Połączenie ustanowione.\n')
        
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
# nie przepuszcza niepoprawnego emaila (Case sensitive) ale brakuje monitu tak jak z emailem
        for row in results:
            imie = row[0]
            nazwisko = row[1]
            uprawnienia = row[2]
            email = row[3]
#             print ('%-15s| %-20s| %-12s| %-20s' % (imie, nazwisko, uprawnienia, email))
            if (email == user_email):
                print('-----------------------------------\nWitaj '+imie+'!')
                print('%-15s| %-20s| %-12s| %-20s' %('Imie', 'Nazwisko','uprawnienia','email')) 
                print ('%-15s| %-20s| %-12s| %-20s' % (imie, nazwisko, uprawnienia, email))
#                 print(uprawnienia) - podglad uprawnien w zmiennej - DO SKASOWANIA NA KONIEC
                if uprawnienia == '1':
                    print('Status: klubowicz')
                    self.menu_user()
                elif uprawnienia == '2':
                    print('Status: sprzetowiec')
                    self.menu_root()
                else:
                    print('Brak nadanych uprawnień \n Skontaktuj się ze sprzętowcem!')
            else: 
                print('Niepoprawny email')
#                 self.conn.close()
            break

    def menu_root(self):
        self.cursor = self.conn.cursor()
#         print('Połączenie ustanowione')
        while(True):
            c = input('Co chcesz zrobić: n\(S)elect, n\(I)nsert, n\(U)pdate, n\(D)elete, n\(Q)uit \n')
            if(c.upper() == 'S'):
                self.select()
            elif(c.upper() == 'I'):
                self.insert()
                self.conn.commit()    #z pythona musimy zacommitowaÄ‡ zmiany - potwierdziÄ‡
                self.select()
            elif(c.upper() == 'U'):
                self.select()
                self.update()
                self.conn.commit()
                self.select()
            elif(c.upper() == 'D'):
                self.delete() 
                self.conn.commit()
            elif(c.upper() == 'Q'):
                print('Zrywamy połączenie')
                self.conn.close()
                break  
        
    def menu_user(self):
        self.cursor = self.conn.cursor()
        while(True):
            c = input('Co chcesz zrobić: \n [R]rezerwacja \n [Z]zmień swoje dane \n [Q]wyjdz \n')
            if(c.upper() == 'R'):
                self.rezerwacja()
            elif(c.upper() == 'Z'):
                self.user_upadte()
            elif(c.upper() == 'Q'):
                print('Zrywamy połączenie')
                self.conn.close()
                break
p1 = DBconn()
