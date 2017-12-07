#-*- coding: UTF-8 -*-

class UserData:
    def __init__(self,user_email,id_user_login,conn,cursor):
        self.user_email = user_email
        self.id_user_login = id_user_login
        self.conn=conn
        self.cursor=cursor
    
#     DODAĆ weryfikację czy podanego maila już niema w bazie!
        
    def user_add(self,):
        print('---------------\nDODAWANIE NOWEGO UŻYTKOWNIKA')
        imie = input('Podaj imie (wymagane): ')
        plec = input('Podaj płeć (K/M) (wymagane): ')
        plec = plec.upper()
            
        while(True):
#             print('Zmiania imienia ([D]-przejdz dalej): ')
            c = input('[P] podaj nazwisko\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                nazwisko = None
                print('Dalej')
                break
            elif (c.upper() == 'P'):
                nazwisko = input('Podaj nazwisko: ')
                break
            else:
                print('Zła komenda!')
                
        while(True):
            c = input('[P] podaj ksywkę\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                ksywka = None
                print('Dalej')
                break
            elif (c.upper() == 'P'):
                ksywka = input('Podaj ksywkę: ')
                break
            else:
                print('Zła komenda!')      
    
        
        while(True):
            c = input('[P] podaj datę urodzenia\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                data_ur = None
                print('Dalej')
                break
            elif (c.upper() == 'P'):
                data_ur = input('Podaj datę urodzenia YYYY-MM-DD: ')
                break
            else:
                print('Zła komenda!') 
                
        while(True):
            c = input('[P] podaj wagę\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                waga = None
                print('Dalej')
                break
            elif (c.upper() == 'P'):
                waga = input('Podaj wagę: ')
                break
            else:
                print('Zła komenda!')   
        
                
        while(True):
            c = input('[P] podaj numer telefonu\n[D] przejdz dalej ')
            if (c.upper() == 'D'):
                telefon = None
                print('Dalej')
                break
            elif (c.upper() == 'P'):
                telefon = input('Podaj numer telefonu: ')
                break
            else:
                print('Zła komenda!') 
                
        while(True):
            print('\nUprawnienia użytkownika')
            c = input('[K] Klubowicz \n[S] Sprzętowiec')
            if (c.upper() == 'K'):
                uprawnienia = '1'
                print('Uprawnienia nadane')
                break
            elif (c.upper() == 'K'):
                uprawnienia = '1'
                print('Uprawnienia nadane')
                break
            else:
                print('Zła komenda!') 
                
                
        while(True):
            print('\nDane logowania')
            email = input('Podaj adres mailowy: ')
            dl_passwd1 = input('Podaj hasło: ')
            dl_passwd2 = input('Powtórz hasło: ')
            
            if (dl_passwd1 != dl_passwd2):
                print('Podaj jednakowe hasła!')
                continue
            else:
                print('Dane logowania wpisane poprawnie.')
                break
                   
        self.cursor.execute('INSERT INTO klubowicze (imie, nazwisko, ksywka, plec, data_ur, waga, email, telefon, uprawnienia) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);', (imie, nazwisko, ksywka, plec, data_ur, waga, email, telefon, uprawnienia))
        self.cursor.execute('INSERT INTO logowanie (haslo, email) values (%s,%s);', (dl_passwd1, email))
        self.conn.commit()     
        print("Użytkownik dodany.\n")
        
