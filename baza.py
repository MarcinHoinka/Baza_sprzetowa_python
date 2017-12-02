#-*- coding: utf-8 -*-
import pymysql
# import getpass
from Conn_Package.connection import conn
from aifc import data

class DBconn:
    def __init__(self):
#         self.user_email=''
        self.conn=conn
        self.cursor = self.conn.cursor()
        print('''
    __________                                                       
    \______   \_____  _____________                                  
     |    |  _/\__  \ \___   /\__  \                                 
     |    |   \ / __ \_/    /  / __ \_                               
     |______  /(____  /_____ \(____  /                               
            \/      \/      \/     \/                                
      _________                           __                         
     /   _____/____________________ _____/  |_  ______  _  _______   
     \_____  \\____ \_  __ \___   // __ \    __\/  _ \ \/ \/ /\__  \  
     /        \  |_> >  | \//    /\  ___/|  | (  <_> )     /  / __ \_
    /_______  /   __/|__|  /_____ \\____  >__|  \____/ \/\_/  (____  /
            \/|__|               \/     \/                        \/ 

    Połączenie ustanowione.\n''')
    
#         print(""" print bloku """) 
        
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
            c = input('--------------- \nCo chcesz zrobić: \n [S]Pokaż listę użytkowników \n [I]insert \n [R]rezerwacje\n [U]update \n [D]usuń użytkownika \n [H]zmień hasło \n [Q]Wyloguj \n')
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
                r1 = Rezerwacje(self.user_email)
                r1.rez_menu()
            elif(c.upper() == 'Z'):
                self.user_update()
            elif(c.upper() == 'H'):
                self.passwd_change()
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                #self.conn.close()
                break
    

#     -------------------- Funkcjonalność (METODY) do menu_root i menu_user -------------------------------
    
    def user_update(self):
        self.cursor.execute('SELECT * FROM klubowicze WHERE email =\''+self.user_email+'\';')
        results = self.cursor.fetchall()
#         print(results)
        for row in results:
            id_user = str(row[0])
            imie = row[1]
            nazwisko = row[2]
            ksywa = row[3]
            plec = row[4]
            data_ur = row[5]
            waga = row[6]
            email = row[7]
            telefon = row[8]
#             testowe printy sprawdzające działanie - do usuniecia
#             print ('%8s| %-15s| %-20s| %-10s| %-5s| %-14s| %-5s| %-20s| %-10s|' % ('User ID','imie', 'nazwisko', 'ksywa', 'płeć', 'Data urodzenia', 'waga', 'email', 'telefon'))
#             print ('%8i| %-15s| %-20s| %-10s| %-5s| %-14s| %-5s| %-20s| %-10s|' % (id_user, imie, nazwisko, ksywa, plec, data_ur, waga, email, telefon))
        
#         print('-------------\nPodaj dane do edycji. \nUwaga! Puste pola nadpiszą stare wartości!')
        print('---------------\nEDYCJA DANYCH')
        while(True):
#             print('Zmiania imienia ([D]-przejdz dalej): ')
            c = input('Zmiana imienia.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            else:
                imie = input('Podaj imie: ')
                self.cursor.execute('UPDATE klubowicze SET imie = \''+imie+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
        
        while(True):
            c = input('Zmiana nazwiska.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            else:
                nazwisko = input('Podaj nazwisko: ')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+nazwisko+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            
        while(True):
            c = input('Zmiana ksywki.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            else:
                ksywa = input('Podaj swoją ksywkę: ')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+ksywa+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break       
            
        while(True):
            c = input('Zmiana płci ;) \n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            else:
                ksywa = input('Podaj płeć: ')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+plec+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            
        while(True):
            c = input('Zmiana ksywki.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            else:
                ksywa = input('Podaj swoją datę urodzenia w formacie \'YYYY-MM-RR\':')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+data_ur+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            
        while(True):
            c = input('Zmiana wagi\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            else:
                ksywa = input('Podaj wagę: ')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+waga+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            
        while(True):
            c = input('Zmiana numeru telefonu \n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            else:
                ksywa = input('Podaj nr. telefonu (bez spacji): ')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+telefon+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            
#         email = input('Podaj email: ')     email w oddzielnym menu!!!!
      
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

# klasa do submenu obsługi rezerwacji

class Rezerwacje:
    def __init__(self,user_email):
        self.user_email = user_email
        self.conn=conn

         
    def rez_menu(self): 
        self.cursor = self.conn.cursor()  
        while(True):
            c = input('--------------- \nCo chcesz zrobić: \n [S]Pokaż listę rezerwacji \n [I]nsert \n [U]pdate \n [D]usuń użytkownika \n [H]zmień hasło \n [Q]cofnij \n')
            if(c.upper() == 'S'):
                self.rez_list()
            elif(c.upper() == 'I'):
                self.insert()
                self.conn.commit()    #z pythona musimy zacommitować zmiany - potwierdziÄ‡
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
        
    def rez_list(self):
        print(self.user_email)
#         self.cursor.execute('SELECT imie, nazwisko, ksywka, plec, data_ur, waga, email, telefon FROM klubowicze WHERE email =\''+
#                             self.user_email+'\';')
        self.cursor.execute('SELECT * FROM baza_sprzetowa.historia_rez2;')
        results = self.cursor.fetchall()
        print ('%-15s| %-15s| %-10s| %-20s| %-10s| %-10s| %-13s| %-9s| %-12s| %-10s|' % ('Rezerwacja od', 'Rezerwacja od','imie', 'nazwisko','ID kajaka','ID wiosla','ID kamizelki','ID kasku','ID fartucha','ID rzutki'))
        for row in results:
            data_rez_start = row[0]
            data_rez_end = row[1]
            imie = row[2]
            nazwisko = row[3]
            id_kajaka = row[4]
            id_wiosla = row[5]
            id_kamizelki = row[6]
            id_kasku= row[7]
            id_fartucha = row[8]
            id_rzutki = row[9]
            print('%-15s| %-15s| %-10s| %-20s| %-10s| %-10s| %-13s| %-9s| %-12s| %-10s|' % (data_rez_start, data_rez_end, imie, nazwisko, id_kajaka, id_wiosla, id_kamizelki, id_kasku, id_fartucha, id_rzutki))
        
#         'data_rez_start', 'data_rez_end','imie;nazwisko','id_kajaka','id_wiosla','id_kamizelki','id_kasku','id_fartucha','id_rzutki
                

p1 = DBconn()
