#-*- coding: utf-8 -*-

class Logoawnie_DB:
    def __init__(self,uprawnienia):
        self.uprawnienia = uprawnienia
#       print(str(self.imie) + ' Witaj w module!')
        uprawnienia = ''

    def loged_as_user(self, uprawnienia ):
        if self.uprawnienia == '1':
            print('użytkownik')
        elif self.uprawnienia == '2':
            print('sprzetowiec')
        else:
            print('Brak nadanych uprawnień \n Skontaktuj się z administratorem!')
        



# wersja do szybkiego uruchamiania samej funkcji
# uprawnienia = ''
# 
# def loged_as_user(self, uprawnienia ):
#     if self.uprawnienia == '1':
#         print('użytkownik')
#     elif self.uprawnienia == '2':
#         print('sprzetowiec')
#     else:
#         print('Brak nadanych uprawnień \n Skontaktuj się z administratorem!')