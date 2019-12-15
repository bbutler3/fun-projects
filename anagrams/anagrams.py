import numpy as np

primes = {'a':2, 'b':3, 'c':5, 'd':7, 'e':11, 'f':13, 'g':17, 'h':19, 'i':23,
          'j':29, 'k':31, 'l':37, 'm':41, 'n':43, 'o':47, 'p':53, 'q':59,
          'r':61, 's':67, 't':71, 'u':73, 'v':79, 'w':83, 'x':89, 'y':97,
          'z':101}

word1orig = input('first word: ')
word2orig = input('second word: ')

word1 = "".join([char for char in word1orig if char.isalpha()])
word2 = "".join([char for char in word2orig if char.isalpha()])

word1 = word1.lower()
word2 = word2.lower()

word1total = 1
for letter in word1:
    word1total *= primes[letter]

word2total = 1
for letter in word2:
    word2total *= primes[letter]

print()
    
if word1total == word2total:
    print(f'"{word1orig}"','and',f'"{word2orig}"','are anagrams!')
else:
    print(f'"{word1orig}"','and',f'"{word2orig}"','are NOT anagrams.')

