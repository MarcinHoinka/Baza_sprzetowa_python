#-*- coding: utf-8 -*-
import pymysql
# import getpass
from Conn_Package.connection import conn

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
#                 break
            elif (choice.upper() == 'Q'):
                print('Wylogowano.')
                self.conn.close()
                break
            
    def log_in(self):
        self.user_email = input('Podaj email: ')
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
            if (email == self.user_email):
                print('-----------------------------------\nWitaj '+imie+'!')
                print('%-15s| %-20s| %-12s| %-20s' %('Imie', 'Nazwisko','uprawnienia','email')) 
                print ('%-15s| %-20s| %-12s| %-20s' % (imie, nazwisko, uprawnienia, email))
#                 print(uprawnienia) - podglad uprawnien w zmiennej - DO SKASOWANIA NA KONIEC
                if uprawnienia == '1':
                    print('Status: klubowicz')
                    l1 = Logowanie(self.user_email)
                    l1.menu_user()
                elif uprawnienia == '2':
                    print('Status: sprzętowiec')
                    l2 = Logowanie(self.user_email)
                    l2.menu_root()
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
        
    def menu_root(self):
        self.cursor = self.conn.cursor()
#         print('Połączenie ustanowione')
        #self.user_email = user_email
        while(True):
            c = input('--------------- \nCo chcesz zrobić: \n [S]Pokaż listę użytkowaników \n [I]insert \n [R]rezerwacje\n [U]update \n [D]usuń użytkownika \n [H]zmień hasło \n [Q]Wyloguj \n')
            if(c.upper() == 'S'):
                self.select_klubowicze()
            elif(c.upper() == 'I'):
                self.insert()
                self.conn.commit()    #z pythona musimy zacommitować zmiany - potwierdził
                self.select()
            elif(c.upper() == 'R'):
                r1 = Rezerwacje(self.user_email)
                r1.rez_menu()
            elif(c.upper() == 'U'):
                self.select()
                self.update()
                self.conn.commit()
                self.select()
            elif(c.upper() == 'D'):
                self.delete_user() 
                self.conn.commit()
            elif(c.upper() == 'H'):
                self.passwd_change() #dlaczego hasło sie zmienia bez commitów?
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                #self.conn.close()
                # self.conn.close tylko na początku!
                break
        
    def menu_user(self):
        self.cursor = self.conn.cursor()
        while(True):
            c = input('--------------- \nCo chcesz zrobić: \n [R]rezerwacja \n [Z]zmień swoje dane \n [H]zmien hasło \n [Q]Wyloguj \n')
            if(c.upper() == 'R'):
                self.rezerwacja()
            elif(c.upper() == 'Z'):
                self.user_update()
            elif(c.upper() == 'H'):
                self.passwd_change()
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                #self.conn.close()
                break
    

#     -------------------- FUNKCJONALNOŚĆ DLA menu_user -------------------------------
    
    def user_update(self):
        print(self.user_email)
        self.cursor.execute('SELECT imie, nazwisko, ksywka, plec, data_ur, waga, email, telefon FROM klubowicze WHERE email =\''+
                            self.user_email+'\';')
        results = self.cursor.fetchall()
#         print(results)
        for row in results:
            imie = row[0]
            nazwisko = row[1]
            ksywa = row[2]
            plec = row[3]
            data_ur = row[4]
            waga = row[5]
            email = row[6]
            telefon = row[7]
            print ('%-15s| %-20s| %-10s| %-5s| %-14s| %-5s| %-20s| %-10s|' % ('imie', 'nazwisko', 'ksywa', 'płeć', 'Data urodzenia', 'waga', 'email', 'telefon'))
            print ('%-15s| %-20s| %-10s| %-5s| %-14s| %-5i| %-20s| %-10s|' % (imie, nazwisko, ksywa, plec, data_ur, waga, email, telefon))
        
        print('-------------\nPodaj dane do edycji. \nUwaga! Puste pola nadpiszą stare wartości!')    
        imie = input('Podaj imie: ')
        nazwisko = input('Podaj nazwisko: ')
        ksywa = input('Podaj swoją ksywkę: ')
        plec = input('Podaj płeć: ')
        data_ur = input('Podaj datę urodzenia: ')
        waga = input('Podaj wage: ')
        email = input('Podaj email: ')
        telefon = input('Podaj nr. telefonu: ')    
        self.cursor.execute('update klubowicze=%s imie=%s, nazwisko=%s, ksywa=%s, plec=%s, data_ur=%s, waga=%s, email=%s, telefon=%i;' , +
                            +(imie, nazwisko, ksywa, plec, data_ur, waga, email, telefon))
        
#   update z 140-150 - nie działa
# ----------------------------------------------------------

#     zmienia hasło usera, wymagane potwierdzenie aktualnym hasłem
    def passwd_change(self):
        user_passwd = input('Podaj hasło: ')
        self.cursor.execute('SELECT email from logowanie WHERE haslo =\''+user_passwd+'\';') 
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
    
    
#     def rezerwacja(self):
#         imie = input('Podaj imie: ')
#         nazwisko = input('Podaj nazwisko: ')
#         pozycja = input('Podaj pozycję: ')
#         self.cursor.execute('insert into klubowicze (imie,nazwisko,pozycja) values (%s,%s,%s);' , (imie,nazwisko,pozycja))

#---------------- FUNKCJONALNOŚĆ DLA menu_root ----------------------
    
#     zwraca listę wszystkich userów
    def select_klubowicze(self):
        self.cursor.execute('select id_user, imie, nazwisko, email FROM klubowicze;')
        results = self.cursor.fetchall()
        print("%3s | %10s | %10s | %26s |" %('Id', 'Imie', 'Nazwisko','email'))
        for row in results:
            id_user = row[0]
            imie = row[1]
            nazwisko = row[2]
            email = row[3]
            print("%3s | %10s | %10s | %26s |" % (id_user, imie, nazwisko, email))
    
    
#     kasuje usera po podaniu id_usera
    def delete_user(self):
        id_user = input('Podaj id klubowicza do usunięcia: ')
        self.cursor.execute('delete from klubowicze where id_user=%s;', (id_user))
        print('Użytkownik usunięty.') 
                  
            
#        self.cursor.execute('update user set id_user=%s, imie=%s, nazwisko=%s, email=%s where id=%s;', (id_user, imie, nazwisko, email))
#         print('%-15s| %-20s| %-12s| %-20s' %('ID','Imie', 'Nazwisko','email')) 
#         print ('%-15s| %-20s| %-12s| %-20s' % (id_user, imie, nazwisko, email))



#     -------------------- FUNKCJONALNOŚĆ DLA wspólna -------------------------------


class Rezerwacje:
    def __init__(self,user_email):
        self.user_email = user_email
        self.conn=conn
         
    def rez_menu(self):   
        while(True):
            c = input('--------------- \nCo chcesz zrobić: \n [S]Pokaż listę rezerwacji \n [I]nsert \n [U]pdate \n [D]usuń użytkownika \n [H]zmień hasło \n [Q]cofnij \n')
            if(c.upper() == 'S'):
                self.select_klubowicze()
            elif(c.upper() == 'I'):
                self.insert()
                self.conn.commit()    #z pythona musimy zacommitowaÄ‡ zmiany - potwierdziÄ‡
                self.select()
            elif(c.upper() == 'R'):
                self.rezerwacja()
            elif(c.upper() == 'U'):
                self.select()
                self.update()
                self.conn.commit()
                self.select()
            elif(c.upper() == 'D'):
                self.delete_user() 
                self.conn.commit()
            elif(c.upper() == 'H'):
                self.passwd_change() #dlaczego hasło sie zmienia bez commitów?
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                #self.conn.close()
                break
        

p1 = DBconn()
