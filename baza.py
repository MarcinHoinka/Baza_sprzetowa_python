#-*- coding: utf-8 -*-
import pymysql
# import getpass
from Conn_Package.connection import conn




class DBconn:
    def __init__(self):       
        self.conn=conn
#         self.conn.set_character_set('utf8') ????????????????????
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
    ''')
    
#         print(""" print bloku """) 
        
        while(True):
            choice = input('\nLOGOWANIE\n [Z]zaloguj\n [Q]wyjdz\n ')
            if (choice.upper() == 'Z'):
                self.log_in()
#                 break
            elif (choice.upper() == 'Q'):
                print('\nZamknięcie programu.')
                self.conn.close()
                break
            
    def log_in(self):
        self.user_email = input('Podaj email: ')
        user_passwd = input('Podaj hasło: ')
        self.cursor.execute("SELECT k.id_user, k.imie, k.nazwisko, k.uprawnienia, k.email as email FROM klubowicze as k JOIN logowanie as l where l.haslo COLLATE utf8_bin ='"
                             +user_passwd+"' and (k.email = l.email);")       
        results = self.cursor.fetchall()
# USTERKA nie przepuszcza niepoprawnego hasła (Case sensitive) ale brakuje monitu tak jak z emailem
        for row in results:
            self.id_user_login = row[0]
#             user_id_log zczytany po cichu dla tworzenia insertów rezerwacji w klasie Rezerwacje
            imie = row[1]
            nazwisko = row[2]
            uprawnienia = row[3]
            email = row[4]
            
#             print ('%-15s| %-20s| %-12s| %-20s' % (imie, nazwisko, uprawnienia, email))
            if (email == self.user_email):
                print('-----------------------------------\nWitaj '+imie+'!')
                print('%-15s| %-20s| %-12s| %-20s|' %('Imie', 'Nazwisko','uprawnienia','email')) 
                print ('%-15s| %-20s| %-12s| %-20s|' % (imie, nazwisko, uprawnienia, email))
# TODO print(uprawnienia) - podglad uprawnien w zmiennej - DO SKASOWANIA NA KONIEC
                if uprawnienia == '1':
                    print('Status: klubowicz')
                    l1 = Logowanie(self.user_email,self.id_user_login, self.conn,self.cursor)
                    l1.menu_user()
                elif uprawnienia == '2':
                    print('Status: sprzętowiec')
                    l2 = Logowanie(self.user_email,self.id_user_login,self.conn,self.cursor)
                    l2.menu_root()
                else:
                    print('Brak nadanych uprawnień \n Skontaktuj się ze sprzętowcem!')
                    break
            else: 
                print('Niepoprawny email')
#                 self.conn.close()
                break
        
class Logowanie:
    def __init__(self, user_email, id_user_login, conn, cursor):
        self.user_email = user_email
        self.id_user_login = id_user_login
        self.conn=conn
        self.cursor = cursor
        
# MENU dla uprawnień SPRZĘTOWIEC (admin)        
    def menu_root(self):

        while(True):
            c = input('--------[MENU]-------- \n\n--SPRZĘT--\n[R]rezerwacje i sprzęt \n\n--ADMINISTRACJA-- \n[S]pokaż listę użytkowników \n[D]usuń użytkownika \n\n--UŻYTKOWNIK--\n[P]wyświetl swoje dane \n[Z]zmień swoje dane \n[E]zmień email \n[H]zmień hasło \n[Q]wyloguj \n')
            if(c.upper() == 'S'):
                self.select_klubowicze()
            elif(c.upper() == 'P'):
                self.user_dane()    
            elif(c.upper() == 'Z'):
                self.user_update()
#             elif(c.upper() == 'I'):
#                 self.insert()
#                 self.conn.commit()
#                 self.select()
            elif(c.upper() == 'R'):
                r1 = Rezerwacje(self.user_email,self.id_user_login,self.conn,self.cursor)
                r1.rez_menu()
#             elif(c.upper() == 'U'):
#                 self.select()
#                 self.update()
#                 self.conn.commit()
#                 self.select()
            elif(c.upper() == 'D'):
                self.delete_user() 
                self.conn.commit()
            if(c.upper() == 'E'):
                self.user__email_update() 
            elif(c.upper() == 'H'):
                self.passwd_change() #dlaczego hasło sie zmienia bez commitów?
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                #self.conn.close()
                # self.conn.close tylko na początku!
                break

# MENU dla uprawnień KLUBOWICZ (user)  
    def menu_user(self):
        while(True):
            c = input('--------[MENU]-------- \n\n--SPRZĘT--\n[R]rezerwacje i sprzęt \n\n--UŻYTKOWNIK--\n[P]wyświetl swoje dane \n[Z]zmień swoje dane \n[E]zmień email \n[H]zmień hasło \n[Q]wyloguj \n')
            if(c.upper() == 'R'):
                r1 = Rezerwacje(self.user_email,self.id_user_login, self.conn,self.cursor)
                r1.rez_menu()
            elif(c.upper() == 'P'):
                self.user_dane()    
            elif(c.upper() == 'Z'):
                self.user_update()
            elif(c.upper() == 'E'):
                self.user__email_update()                
            elif(c.upper() == 'H'):
                self.passwd_change()
            elif(c.upper() == 'Q'):
                print('Wylogowano')
                #self.conn.close()
                break
    

#     -------------------- Funkcjonalność (METODY) do menu_root i menu_user -----------------------------


# WYŚWIETLA dane użytkownika 

    def user_dane(self):
        self.cursor.execute('SELECT * FROM klubowicze WHERE email =\''+self.user_email+'\';')
        results = self.cursor.fetchall()
        print ('%-15s| %-20s| %-10s| %-5s| %-14s| %-5s| %-20s| %-10s|' % ('imie', 'nazwisko', 'ksywa', 'płeć', 'Data urodzenia', 'waga', 'email', 'telefon'))
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
        print ('%-15s| %-20s| %-10s| %-5s| %-14s| %-5s| %-20s| %-10s|' % (imie, nazwisko, ksywa, plec, data_ur, waga, email, telefon))

    

# ZMIANA DANYCH użytkownika
    
    def user_update(self):
        self.cursor.execute('SELECT * FROM klubowicze WHERE email =\''+self.user_email+'\';')
        results = self.cursor.fetchall()
        print ('%8s| %-15s| %-20s| %-10s| %-5s| %-14s| %-5s| %-20s| %-10s|' % ('User ID','imie', 'nazwisko', 'ksywa', 'płeć', 'Data urodzenia', 'waga', 'email', 'telefon'))
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
        print ('%8s| %-15s| %-20s| %-10s| %-5s| %-14s| %-5s| %-20s| %-10s|' % (id_user, imie, nazwisko, ksywa, plec, data_ur, waga, email, telefon))

        print('---------------\nEDYCJA DANYCH')
        while(True):
#             print('Zmiania imienia ([D]-przejdz dalej): ')
            c = input('Zmiana imienia.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            elif (c.upper() == 'Z'):
                imie = input('Podaj imie: ')
                self.cursor.execute('UPDATE klubowicze SET imie = \''+imie+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
        
            else:
                print('Zła komenda!')
        
        while(True):
            c = input('Zmiana nazwiska.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            elif (c.upper() == 'Z'):
                nazwisko = input('Podaj nazwisko: ')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+nazwisko+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            else:
                print('Zła komenda!')
                break
        
        while(True):
            c = input('Zmiana ksywki.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            elif (c.upper() == 'Z'):
                ksywa = input('Podaj swoją ksywkę: ')
                self.cursor.execute('UPDATE klubowicze SET nazwisko = \''+ksywa+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            else:
                print('Zła komenda!')
                break
        
        while(True):
            c = input('Zmiana płci ;) \n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            elif (c.upper() == 'Z'):
                plec = input('Podaj płeć: ')
                self.cursor.execute('UPDATE klubowicze SET plec = \''+plec+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            else:
                print('Zła komenda!')
                break
        
        while(True):
            c = input('Zmiana daty urodzenia.\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            elif (c.upper() == 'Z'):
                data_ur = input('Podaj swoją datę urodzenia w formacie \'YYYY-MM-RR\':')
                self.cursor.execute('UPDATE klubowicze SET data_ur = \''+data_ur+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            else:
                print('Zła komenda!')
                break
        
        while(True):
            c = input('Zmiana wagi\n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            elif (c.upper() == 'Z'):
                waga = input('Podaj wagę: ')
                self.cursor.execute('UPDATE klubowicze SET waga = \''+waga+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            else:
                print('Zła komenda!')
                break
        
        while(True):
            c = input('Zmiana numeru telefonu \n[Z] zmień\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                print('Dalej')
                break
            elif (c.upper() == 'Z'):
                telefon = input('Podaj nr. telefonu (bez spacji): ')
                self.cursor.execute('UPDATE klubowicze SET telefon = \''+telefon+'\' WHERE id_user = '+id_user+';')
                self.conn.commit()
                break
            else:
                print('Zła komenda!')
                break
        
# DODAĆ - dodawnie userów na zasadzie jak edycja(JAK REZERWACJE!) Menu kaskadowe zbierajace wartosci do zmiennych które sie zaimportuje do polecania INSERT INTO           
            
#  ZMIANA adresu email
    def user__email_update(self):
        self.cursor.execute('SELECT id_user, imie, email FROM klubowicze WHERE email =\''+self.user_email+'\';')
        results = self.cursor.fetchall()
        print('---------------\nZMIANA ADRESU EMAIL')
        for row in results:
            id_user = str(row[0])
            imie = row[1]
            email = row[2]
            print ('| %-15s| %-20s|' % ('imie','email'))
            print ('| %-15s| %-20s|' % (imie, email))
            email_new = input('Wpisz nowy email: ')
            self.cursor.execute('UPDATE klubowicze SET email= \''+email_new+'\' WHERE id_user ='+id_user+';')
#             print('UPDATE klubowicze SET email= \''+email_new+'\' WHERE id_user ='+id_user+';')
            self.conn.commit()
            self.user_email = email_new
            print('Adres email zmieniony poprawnie.\n')


# ZMIANA hasła usera, Wymagane potwierdzenie aktualnym hasłem
    def passwd_change(self):
        user_passwd = input('Podaj hasło: ')
        self.cursor.execute('SELECT email from logowanie WHERE haslo =\''+user_passwd+'\';') 
        results = self.cursor.fetchall()
        for row in results:
            email = row[0]
            print('Podaj swój email:'+email+'\n') 
            passwd_new = input('Wpisz nowe hasło: ')
            passwd_new2 = input('Wpisz nowe hasło ponownie: ')
            if(passwd_new == passwd_new2):
                self.cursor.execute('UPDATE logowanie SET haslo = \''+passwd_new+'\' WHERE email = \''+email+'\';')
                self.conn.commit()
                print('Hasło zmienione poprawnie.\n')
            else:
                print('Hasła nie są jednakowe! Wpisz dwa razy to samo hasło. \n')
            break


#    ---------------- FUNKCJONALNOŚĆ DLA menu_root ----------------------
    
# zwraca listę wszystkich userów
    def select_klubowicze(self):
        self.cursor.execute('select id_user, imie, nazwisko, email FROM klubowicze;')
        results = self.cursor.fetchall()
        print("%3s| %-10s| %-10s| %-26s|" % ('Id', 'Imie', 'Nazwisko','email'))
        for row in results:
            id_user = row[0]
            imie = row[1]
            nazwisko = row[2]
            email = row[3]
            print("%-3s| %-10s| %-10s| %-26s|" % (id_user, imie, nazwisko, email))
    
    
# USUWANIE usera po podaniu jego ID (z listy klubowiczów) - kasuje też logowanie
    def delete_user(self):
        id_user = input('Podaj id klubowicza do usunięcia: ')
#         print('delete from klubowicze where id_user=%s', (id_user))
        self.cursor.execute('delete from klubowicze where id_user=%s', (id_user))
        print('Użytkownik usunięty.') 


#     -------------------- FUNKCJONALNOŚĆ wspólna -------------------------------

# klasa do submenu obsługi rezerwacji

class Rezerwacje:
    def __init__(self,user_email,id_user_login,conn,cursor):
        self.user_email = user_email
        self.id_user_login = id_user_login
        self.conn=conn
        self.cursor=cursor

# MENU obsługi rezerwacji 
         
    def rez_menu(self): 
        while(True):
            c = input('\n----[REZERWACJE]----\n[H]pokaż historię rezerwacji \n[R]zarezerwuj sprzęt \n[K]lista kajaków \n[W]lista wioseł \n[I]lista kamizelek \n[F]lista fartuchów \n[S]lista kasków \n[T]lista rzutek \n[Q]Cofnij \n')
            if(c.upper() == 'H'):
                self.rez_hist()
            elif(c.upper() == 'R'):
                self.rezerwacja()
            elif(c.upper() == 'K'):
                self.lista_kajaki()                           
            elif(c.upper() == 'W'):
                self.lista_wiosla()
            elif(c.upper() == 'I'):
                self.lista_kamizelki()
            elif(c.upper() == 'S'):
                self.lista_kaski()
            elif(c.upper() == 'F'):
                self.lista_fartuchy()
            elif(c.upper() == 'T'):
                self.lista_rzutki()
            elif(c.upper() == 'Q'):
#                 print('Wyjście ze rezerwacji...')
                break


# LISTA REZERWACJI
    def rez_hist(self):
        self.cursor.execute('SELECT * FROM baza_sprzetowa.historia_rez2;')
        results = self.cursor.fetchall()
        print ('%-15s| %-15s| %-10s| %-20s| %-10s| %-10s| %-13s| %-9s| %-12s| %-10s|' % ('Rezerwacja od', 'Rezerwacja od','Imie', 'Nazwisko','ID kajaka','ID wiosla','ID kamizelki','ID kasku','ID fartucha','ID rzutki'))
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
        
# LISTA sprzetu z tabeli kajaki
    def lista_kajaki(self):
        self.cursor.execute('SELECT id_kajaka, marka, model, typ, wypornosc, kolor FROM kajaki;')
        results = self.cursor.fetchall()
        print ('%-10s| %-18s| %-18s| %-10s| %-10s| %-20s|' % ('ID kajaka', 'marka','model', 'typ','wypornosc','kolor'))
        for row in results:
            id_kajaka = row[0]
            marka = row[1]
            model = row[2]
            typ = row[3]
            wypornosc = row[4]
            kolor = row[5]
            print ('%-10s| %-18s| %-18s| %-10s| %-10s| %-20s|' % (id_kajaka, marka, model, typ, wypornosc, kolor))

# LISTA sprzetu z tabeli wiosła
    def lista_wiosla(self):
            self.cursor.execute('SELECT id_wiosla, marka, model, typ, kat FROM wiosla;')
            results = self.cursor.fetchall()
            print ('%-10s| %-15s| %-15s| %-10s| %-5s|' % ('ID wiosła', 'marka','model', 'typ','kąt'))
            for row in results:
                id_wiosla = row[0]
                marka = row[1]
                model = row[2]
                typ = row[3]
                kat = row[4]
                print ('%-10s| %-15s| %-15s| %-10s| %-5s|' % (id_wiosla, marka, model, typ, kat))
                
    def lista_kamizelki(self):
            self.cursor.execute('SELECT id_kamizelki,marka,model,rozmiar,kolor FROM kamizelki;')
            results = self.cursor.fetchall()
            print ('%-13s| %-15s| %-15s| %-10s| %-15s|' % ('ID kamizelki', 'marka','model', 'rozmiar','kolor'))
            for row in results:
                id_kamizelki = row[0]
                marka = row[1]
                model = row[2]
                rozmiar = row[3]
                kolor = row[4]
                print ('%-13s| %-15s| %-15s| %-10s| %-15s|' % (id_kamizelki,marka,model,rozmiar,kolor))           

    def lista_fartuchy(self):
            self.cursor.execute('SELECT id_fartucha,marka,model,rozmiar,rozmiar_kokpitu FROM fartuchy;')
            results = self.cursor.fetchall()
            print ('%-13s| %-15s| %-15s| %-10s| %-16s|' % ('ID fartucha', 'marka','model', 'rozmiar','rozmiar_kokpitu'))
            for row in results:
                id_fartucha = row[0]
                marka = row[1]
                model = row[2]
                rozmiar = row[3]
                rozmiar_kokpitu = row[4]
                print ('%-13s| %-15s| %-15s| %-10s| %-16s|' % (id_fartucha,marka,model,rozmiar,rozmiar_kokpitu))
                
    def lista_kaski(self):
            self.cursor.execute('SELECT id_kasku, marka, model, rozmiar, kolor, garda FROM kaski;')
            results = self.cursor.fetchall()
            print ('%-13s| %-20s| %-15s| %-10s| %-16s| %-6s|' % ('ID kasku', 'marka','model', 'rozmiar','kolor','garda'))
            for row in results:
                id_kasku = row[0]
                marka = row[1]
                model = row[2]
                rozmiar = row[3]
                kolor = row[4]
                garda = row[5]
                print ('%-13s| %-20s| %-15s| %-10s| %-16s| %-6s|' % (id_kasku,marka,model,rozmiar,kolor,garda))        

    def lista_rzutki(self):
            self.cursor.execute('SELECT id_rzutki, marka, model, dlugosc FROM asekuracja;')
            results = self.cursor.fetchall()
            print ('%-11s| %-15s| %-15s| %-10s|' % ('ID rzutki', 'marka','model', 'długość'))
            for row in results:
                id_rzutki = row[0]
                marka = row[1]
                model = row[2]
                dlugosc = row[3]
                print ('%-11s| %-15s| %-15s| %-10s|' % (id_rzutki,marka,model,dlugosc))        


# rezerwacja - insert w tabeli rezerwacji dopisywany kaskadowo
# najpierw wprowadzamy date rezerwacji, nastepnie zamawamy kolejne elementy z dostępnych w tym okresie 

    def rezerwacja(self):
        data_rez_start = input('Podaj datę początkową rezerwacji (RRRR-MM-DD): ')
        data_rez_end = input('Podaj datę końcową rezerwacji (RRRR-MM-DD): ')
        while(data_rez_start > data_rez_end):
            print('Data końcowa jest wczesniejsza od początkowej!')
            break

# sprawdzenie dostepności kajaka w danym terminie
        print("--Dostępność kajaków--")
        self.cursor.execute('SELECT id_kajaka, CASE WHEN (data_rez_start <= \''+data_rez_end+'\' AND data_rez_end >= \''+data_rez_start+'\' AND id_kajaka is not null) OR (data_rez_start >= \''+data_rez_start+'\' AND data_rez_end <= \''+data_rez_end+'\' AND id_kajaka is not null) THEN \'Zajety\' ELSE \'Wolny\' END AS rezerwacja FROM rezerwacje group by rezerwacja having rezerwacja = \'Zajety\';')
        results = self.cursor.fetchall()
        print ('%-10s| %-11s|' % ('ID','Dostępność'))
        for row in results:
            id_kajaka = row [0]
            dostepnosc = row [1] 
            print('%-10s| %-11s|' % (id_kajaka, dostepnosc))
            
# DODANIE id kajaka do zmiennej id kajaka (na poczet inserta z rezerwacją lub przejscie dalej 
        while(True):
            c = input('\nRezerwacja kajaka.\n[R] rezerwuj\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                id_kajaka = 'null'
                print('Dalej')
                break
            elif (c.upper() == 'R'):
                id_kajaka = input('Podaj ID kajaka: ')
                id_kajaka = id_kajaka.upper()
                break 
            else:
                print('Zła komenda!')
   
# sprawdzenie dostepności WIOSŁA w danym terminie
        print("--Dostępność wioseł--")
        self.cursor.execute('SELECT id_wiosla, CASE WHEN (data_rez_start <= \''+data_rez_end+'\' AND data_rez_end >= \''+data_rez_start+'\' AND id_wiosla is not null) OR (data_rez_start >= \''+data_rez_start+'\' AND data_rez_end <= \''+data_rez_end+'\' AND id_wiosla is not null) THEN \'Zajete\' ELSE \'Wolne\' END AS rezerwacja FROM rezerwacje group by rezerwacja having rezerwacja = \'Zajete\';')
        results = self.cursor.fetchall()
        print ('%-10s| %-11s|' % ('ID','Dostępność'))
        for row in results:
            id_wiosla = row [0]
            dostepnosc = row [1] 
            print('%-10s| %-11s|' % (id_wiosla, dostepnosc))   
                
                
# DODANIE id wiosła do zmiennej (na poczet inserta z rezerwacją lub przejscie dalej 
        while(True):
            c = input('\nRezerwacja wiosła.\n[R] rezerwuj\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                id_wiosla = 'null'
                print('Dalej')
                break
            elif (c.upper() == 'R'):
                id_wiosla = input('Podaj ID wiosła: ')
                id_wiosla = id_wiosla.upper()
                break
            else:
                print('Zła komenda!')                
                
# sprawdzenie dostepności kamizelki w danym terminie
        print("--Dostępność kamizelek--")
        self.cursor.execute('SELECT id_kamizelki, CASE WHEN (data_rez_start <= \''+data_rez_end+'\' AND data_rez_end >= \''+data_rez_start+'\' AND id_kamizelki is not null) OR (data_rez_start >= \''+data_rez_start+'\' AND data_rez_end <= \''+data_rez_end+'\' AND id_kamizelki is not null) THEN \'Zajeta\' ELSE \'Wolna\' END AS rezerwacja FROM rezerwacje group by rezerwacja having rezerwacja = \'Zajeta\';')
        results = self.cursor.fetchall()
        print ('%-10s| %-11s|' % ('ID','Dostępność'))
        for row in results:
            id_kamizelki = row [0]
            dostepnosc = row [1] 
            print('%-10s| %-11s|' % (id_kamizelki, dostepnosc))
            
# dodanie id_kamizelki do zmiennej id_kamizelki (na poczet inserta z rezerwacją lub przejscie dalej 
        while(True):
            c = input('\nRezerwacja kamizelki.\n[R] rezerwuj\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                id_kamizelki = 'null'
                print('Dalej')
                break
            elif (c.upper() == 'R'):
                id_kamizelki = input('Podaj ID kamizelki: ')
                id_kamizelki = id_kamizelki.upper()
                break 
            else:
                print('Zła komenda!')

# sprawdzenie dostepności kasku w danym terminie
        print("--Dostępność kasków--")
        self.cursor.execute('SELECT id_kasku, CASE WHEN (data_rez_start <= \''+data_rez_end+'\' AND data_rez_end >= \''+data_rez_start+'\' AND id_kasku is not null) OR (data_rez_start >= \''+data_rez_start+'\' AND data_rez_end <= \''+data_rez_end+'\' AND id_kasku is not null) THEN \'Zajety\' ELSE \'Wolny\' END AS rezerwacja FROM rezerwacje group by rezerwacja having rezerwacja = \'Zajety\';')
        results = self.cursor.fetchall()
        print ('%-10s| %-11s|' % ('ID','Dostępność'))
        for row in results:
            id_kasku = row [0]
            dostepnosc = row [1] 
            print('%-10s| %-11s|' % (id_kasku, dostepnosc))
            
# DODANIE id_kasku (na poczet inserta z rezerwacją lub przejscie dalej 
        while(True):
            c = input('\nRezerwacja kasku.\n[R] rezerwuj\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                id_kasku = 'null'
                print('Dalej')
                break
            elif (c.upper() == 'R'):
                id_kasku = input('Podaj ID kasku: ')
                id_kasku = id_kasku.upper()
                break 
            else:
                print('Zła komenda!')

# sprawdzenie dostepności fartucha w danym terminie
        print("--Dostępność fartuchów--")
        self.cursor.execute('SELECT id_fartucha, CASE WHEN (data_rez_start <= \''+data_rez_end+'\' AND data_rez_end >= \''+data_rez_start+'\' AND id_fartucha is not null) OR (data_rez_start >= \''+data_rez_start+'\' AND data_rez_end <= \''+data_rez_end+'\' AND id_fartucha is not null) THEN \'Zajety\' ELSE \'Wolny\' END AS rezerwacja FROM rezerwacje group by rezerwacja having rezerwacja = \'Zajety\';')
        results = self.cursor.fetchall()
        print ('%-10s| %-11s|' % ('ID','Dostępność'))
        for row in results:
            id_fartucha = row [0]
            dostepnosc = row [1] 
            print('%-10s| %-11s|' % (id_fartucha, dostepnosc))
            
# DODANIE id_fartucha (na poczet inserta z rezerwacją lub przejscie dalej 
        while(True):
            c = input('\nRezerwacja fartucha.\n[R] rezerwuj\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                id_fartucha = 'null'
                print('Dalej')
                break
            elif (c.upper() == 'R'):
                id_fartucha = input('Podaj ID fartucha: ')
                id_fartucha = id_fartucha.upper()
                break 
            else:
                print('Zła komenda!')

# sprawdzenie dostepności rzutki w danym terminie
        print("--Dostępność rzutek--")
        self.cursor.execute('SELECT id_rzutki, CASE WHEN (data_rez_start <= \''+data_rez_end+'\' AND data_rez_end >= \''+data_rez_start+'\' AND id_rzutki is not null) OR (data_rez_start >= \''+data_rez_start+'\' AND data_rez_end <= \''+data_rez_end+'\' AND id_rzutki is not null) THEN \'Zajeta\' ELSE \'Wolna\' END AS rezerwacja FROM rezerwacje group by rezerwacja having rezerwacja = \'Zajeta\';')
        results = self.cursor.fetchall()
        print ('%-10s| %-11s|' % ('ID','Dostępność'))
        for row in results:
            id_rzutki = row [0]
            dostepnosc = row [1] 
            print('%-10s| %-11s|' % (id_rzutki, dostepnosc))
            
# DODANIE id_rzutki (na poczet inserta z rezerwacją lub przejscie dalej 
        while(True):
            c = input('\nRezerwacja rzutki.\n[R] rezerwuj\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                id_rzutki = 'null'
                print('Dalej')
                break
            elif (c.upper() == 'R'):
                id_rzutki = input('Podaj ID rzutki: ')
                id_rzutki = id_rzutki.upper()
                break 
            else:
                print('Zła komenda!')
         
        id_user_login = str(self.id_user_login)
        print('insert into rezerwacje values (null,\''+data_rez_start+'\', \''+data_rez_end+'\', \''+id_user_login+'\', \''+id_kajaka+'\', \''+id_wiosla+'\',\''+id_kamizelki+'\',\''+id_kasku+'\',\''+id_fartucha+'\',\''+id_rzutki+'\');')
        self.cursor.execute('insert into rezerwacje values (null,\''+data_rez_start+'\', \''+data_rez_end+'\', \''+id_user_login+'\', \''+id_kajaka+'\', \''+id_wiosla+'\',\''+id_kamizelki+'\',\''+id_kasku+'\',\''+id_fartucha+'\',\''+id_rzutki+'\');')
        self.conn.commit()
        
                
#         print('insert into rezerwacje values (id_rezerwacje ,data_rez_start=%s, data_rez_end=%s, id_kajaka=%s, id_wiosla=%s, id_kamizelki=%s, id_kasku=%s, id_fartucha=%s, id_rzutki=%s ;', ('null', data_rez_start, data_rez_end, id_kajaka, id_wiosla, id_kamizelki, id_kasku, id_fartucha, id_rzutki))
#         print('(insert into rezerwacje values (null, '2017-10-16' ,'2017-10-23', 13 ,'KG-007', 'WG-006', 'KaG-005', null, null , null)');
#         print('(insert into rezerwacje values (null, \''+data_rez_start+'\', \''+data_rez_end+'\', \''+id_kajaka+'\', \''+id_wiosla+'\',\''+id_kamizelki+'\',\''+id_kasku+'\',\''+id_fartucha+'\',\''+id_rzutki+'\');')


p1=DBconn()
