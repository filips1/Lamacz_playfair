import string
import random
ALPHABET = string.ascii_uppercase #angielski alfabet dużych liter

def readfile(file):
    f=open(file, mode='r') # otwieranie pliku w trybie read
    message=''
    for ch in f.read():
        if 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122: # sprawdzanie czy dany znak jest literą za pomocą numeru ASCII
            message+=ch.upper() #Zmiana liter na duże
    f.close()
    return message # przerobiona wiadomość

class Playfair:
    @staticmethod
    def buildtable(key): # tworzenie tablicy znaków (klucza) 5x5
        table = sorted(set(key), key = lambda x: key.index(x)) # wprowadzenie podanego klucza do tablicy w postaci setu w kolejności
        for ch in ALPHABET:
            if not (ch in key) and ch!= 'J': 
                table += ch # dodannie alfabetycnie pozostałych znaków nie będących już podanych w kluczu poza j żeby mógł powstać kwadrat 5x5
        return table

    @staticmethod
    def padding(message):  # wpisywanie znkaku jeśli obok siebie są 2 takie same litery lub gdy liczba liter jest nieparzysta :D
        list_message=list(message)
        i = 1
        while i < len(list_message):            #sprawdzanie czy 2 litery obok siebie są równe
            if list_message[i]==list_message[i-1]:
                list_message.insert(i, 'X')
            i += 2
        if len(list_message)%2!=0:  #sprawdzanie parzystości liter
            list_message.append('X')
        padded_message = []
        for a in range(0, len(list_message), 2):
            padded_message.append(''.join(list_message[a:a+2])) #dzielenie szyfru w pary liter
        return padded_message

    @staticmethod
    def substitution(message, table, *, mode):

        if mode == 1:
            message=message.replace('J', 'I') # usuwanie dodatkowej litery żeby liczba liter była równa kwadratowi 5x5
        list_message=Playfair.padding(message)
        list_pos = []
        for elem in list_message:
            first_letter = [table.index(elem[0])//5, table.index(elem[0])%5] #przypisanie pozycji danej litery w kwadracie playfair
            second_letter = [table.index(elem[1])//5, table.index(elem[1])%5] #przypisanie pozycji następne litery w kwadracie playfair
            list_pos.append([first_letter, second_letter ]) #ustalanie pozycji par liter w kwadracie 5x5 poprzez podstaiwienie ich do klucza i dzielenie przez 5 bez reszty oraz 5 modulo.
        list_pos2=[]
        for elem in list_pos:

            if elem[0][0]==elem[1][0]: #jeśli są w tej samej kolumnie
                list_pos2.append([[elem[0][0], (elem[0][1]+mode)%5], [elem[1][0], (elem[1][1]+mode)%5]]) #przesuń o jedno w dół
            elif elem[0][1]==elem[1][1]: # jeśli są w tym samym rzędzie
                list_pos2.append([[(elem[0][0]+mode)%5, elem[0][1]], [(elem[1][0]+mode)%5, elem[1][1]]]) # przesuń o jedno w bok
            else:
                list_pos2.append([[elem[0][0], elem[1][1]], [elem[1][0], elem[0][1]]]) # jeśli ani jedno ani drugie zamień rogami tak żeby tworzyły kwadrat
        c=''.join([table[e[0][0]*5+e[0][1]]+table[e[1][0]*5+e[1][1]] for e in list_pos2])
        return c

    @staticmethod
    def encrypt(message, key):
        return Playfair.substitution(message, key, mode=1)

    @staticmethod
    def decrypt(message, key):
        return Playfair.substitution(message, key, mode=-1)

key=Playfair.buildtable('monarchy'.upper())
c = Playfair.encrypt('wearediscoveredsaveyourselfx'.upper(), key)
print(c)
d = Playfair.decrypt(c, key)
print(d)

