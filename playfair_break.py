import playfair
import datetime
import random
import math
import json
from math import log10
import math


class ngram_score(object):
    def __init__(self,ngramfile,sep=' '):
        # wczytaj plik i zapisz jego wartości
        self.ngrams = {}
        for line in open(ngramfile):
            key,count = line.split(sep) 
            self.ngrams[key] = int(count)
        self.L = len(key)

        self.N = sum(self.ngrams.values())
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N) #wylicz prawdopodobieństwo logarytmiczne
        self.floor = log10(0.01/self.N)

    def score(self,text):
        score = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text)-self.L+1):
            if text[i:i+self.L] in self.ngrams: score += ngrams(text[i:i+self.L]) # przebadaj punktację tekstu
            else: score += self.floor          
        return score


def playfairkeytransformation(childkey): # modyfikowanie klucza playfair
    rand = random.randint(0, 50) # za pomocą losowania
    if rand == 1: # 2% szans na zamianę wiersza
        i = random.randrange(5)
        j = random.randrange(5)
        childkey[i*5:i*5+5], childkey[j*5:j*5+5] = childkey[j*5:j*5+5], childkey[i*5:i*5+5]
    elif rand == 2: # 2% szans na zamianę kolumny
        i = random.randrange(5)
        j = random.randrange(5)
        childkey[0*5+i], childkey[1*5+i], childkey[2*5+i], childkey[3*5+i], childkey[4*5+i], childkey[0*5+j], childkey[1*5+j], childkey[2*5+j], childkey[3*5+j], childkey[4*5+j] = childkey[0*5+j], childkey[1*5+j], childkey[2*5+j], childkey[3*5+j], childkey[4*5+j], childkey[0*5+i], childkey[1*5+i], childkey[2*5+i], childkey[3*5+i], childkey[4*5+i]
    elif rand == 3: # 2% szans na odwrócenie klucza
        childkey.reverse()
    elif rand == 4: # 2% na odwrócenie wierszy z góry na dół
        for i in range(3):
            childkey[i*5:i*5+5], childkey[(4-i)*5:(4-i)*5+5] = childkey[(4-i)*5:(4-i)*5+5], childkey[i*5:i*5+5]
    elif rand == 5: #2% na zamianę kolumn prawo-lewo
        for i in range(3):
            childkey[0*5+i], childkey[1*5+i], childkey[2*5+i], childkey[3*5+i], childkey[4*5+i], childkey[0*5+(4-i)], childkey[1*5+(4-i)], childkey[2*5+(4-i)], childkey[3*5+(4-i)], childkey[4*5+(4-i)] = childkey[0*5+(4-i)], childkey[1*5+(4-i)], childkey[2*5+(4-i)], childkey[3*5+(4-i)], childkey[4*5+(4-i)], childkey[0*5+i], childkey[1*5+i], childkey[2*5+i], childkey[3*5+i], childkey[4*5+i]
    else: # 90% na zamianę 2 liter
        i = random.randrange(25)
        j = random.randrange(25)
        childkey[i], childkey[j] = childkey[j], childkey[i]
    return childkey


def breakplayfair(ciphertext): #Simulated annealing algorithm
    fitness = ngram_score('english_quadgrams.txt') #ustalenie słownika wykorzystywanego przez ngramy
    result = [] 
    parentkey = list(playfair.ALPHABET.replace('J', '')) #usinięcie J z klucza
    d = playfair.Playfair.decrypt(ciphertext, ''.join(parentkey)) # dekodowanie szyfru za pomocą klucza
    oldfitness = fitness.score(d) # wynik puntkowy ustawienia
    maxscore = fitness.score(d) # obecny maksymalny wynik
    maxkey = parentkey[:] # ustawienie obecnego klucza jako najlepszy wynik
    T = 10.0 
    count = 0 
    while T > 0:
        while count < 5001:
            childkey = parentkey[:]
            childkey = playfairkeytransformation(childkey) #zamiana znaku w kluczu
            d = playfair.Playfair.decrypt(ciphertext, ''.join(childkey)) #dekrypcja szyfru przy użyciu nowego klucza
            newfitness = fitness.score(d) #zapisanie nowego wyniku
            if newfitness > maxscore: # jeśli nowy wynik jest lepszy od poprzedniego
                maxkey = childkey #nowy najlepszy klucz jest zapisany
                maxscore = newfitness # i nowy najlepszy wynik
                print(maxscore)
                print("Klucz to:",maxkey)
            if newfitness >= oldfitness: # jeśli jest lepszy bądź równy od poprzedniego wyniku
                parentkey = childkey # wtedy klucz rodzica zostaje zamieniony
                oldfitness = newfitness # wynik zostaje zastąpiony
            else:
                if T > 0:
                    prob = math.exp((newfitness - oldfitness)/T)
                    if prob > random.uniform(0.0, 1.0)/10000:
                        oldfitness = newfitness
                        parentkey = childkey
            count += 1
            if count % 5000 == 0:
                result.append(playfair.Playfair.decrypt(ciphertext, ''.join(maxkey))) # jeślli zostało wykonane 10000 działań zapisz najlepszy wynik
        T = T - 0.2
        count = 0
        print(T)
        print("Obecny max to: ",  max(result, key=fitness.score))
    print(maxscore)
    return max(result, key=fitness.score) # wypisanie najlepszego wyniku



print(datetime.datetime.now())
message = playfair.readfile(r'hobbit.txt')
fitness = ngram_score('english_quadgrams.txt')
print("Oryginalna punktacja", fitness.score(message))
key=playfair.Playfair.buildtable('BELIAR'.upper())
print("klucz:", key)
ciphertext = playfair.Playfair.encrypt(message, key)
print(ciphertext)
print(breakplayfair(ciphertext))

print(datetime.datetime.now()) #oczekwiany czas pracy 5-10 minut

