#-*- coding: utf-8 -*-
import pymysql
from Conn_Package.connection import conn

# import modules
# import getpass
#from Conn_Package.password import passwrd, db

class DBconn:
    def __init__(self):
#         self.user_email=''
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
                    l1 = Logowanie(user_email)
                    l1.menu_user()
                elif uprawnienia == '2':
                    print('Status: sprzetowiec')
                    self.menu_root()
                else:
                    print('Brak nadanych uprawnień \n Skontaktuj się ze sprzętowcem!')
            else: 
                print('Niepoprawny email')
#                 self.conn.close()
            break
        
class Logowanie:
    def __init__(self,user_email):
        self.user_email = user_email
        self.conn=conn
        #jak uruchomic odpowiednią metode zaleznie od uprawnień
    
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
            elif(c.upper() == 'H'):
                self.passwd_change()
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                self.conn.close()
                break  
        
    def menu_user(self):
        self.cursor = self.conn.cursor()
        while(True):
            c = input('Co chcesz zrobić: \n [R]rezerwacja \n [Z]zmień swoje dane \n [H]zmien hasło \n [Q]wyjdz \n')
            if(c.upper() == 'R'):
                self.rezerwacja()
            elif(c.upper() == 'Z'):
                self.user_update()
            elif(c.upper() == 'H'):
                self.passwd_change()
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                self.conn.close()
                break
    
    def user_update(self):
#         print(self.user_email)
        # brak wartosci dla zmiennej user_email a co za tym idzie rezultatu w 116!!! 
        self.cursor.execute('SELECT imie, nazwisko, ksywka, plec, data_ur, waga, email, telefon, uprawnienia FROM klubowicze WHERE email =\''+
                            self.user_email+'\';')
#         self.cursor.execute('SELECT * from klubowicze;')
        results = self.cursor.fetchall()
        print(results)
        
        
#         self.cursor.execute('update user set imie=%s, nazwisko=%s, pozycja=%s where id=%s;', (imie,nazwisko,pozycja,id))
#         
#         self.cursor = self.conn.cursor()


# passwd_change wciąż rozpoznaje tylko po hasle bez potwierdzenia maila! 

    def passwd_change(self):
        user_passwd = input('Podaj hasło: ')
        self.cursor.execute('SELECT email from logowanie WHERE haslo =\''+user_passwd+'\';') 
        # DODAĆ w select'ie >>> user_email <<< jak zacznie działać
        results = self.cursor.fetchall()
        for row in results:
            email = row[0]
            print('email:'+email+'\n') 
            passwd_new = input('Wpisz nowe hasło: ')
            passwd_new2 = input('Wpisz nowe hasło ponownie: ')
            if(passwd_new == passwd_new2):
                self.cursor.execute('UPDATE logowanie SET haslo = \''+passwd_new+'\' WHERE email = \''+email+'\';')
                self.conn.commit()
                print('Hasło zmienione poprawnie.\n')
            else:
                print('Hasła nie są jednakowe! Wpisz dwa razy to samo hasło. \n')
            break
        
    
p1 = DBconn()
