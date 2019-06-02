import numpy as np


import string

exclude = set(string.punctuation)

Akbar = 'Abul-Fath Jalal-ud-din Muhammad Akbar popularly known as Akbar I, also as Akbar the Great, was the third Mughal emperor, who reigned from 1556 to 1605'
Akbar =  ''.join(ch for ch in Akbar if ch not in exclude)
print(Akbar)

Banana = 'A banana is an edible fruit Ã¢ÂÂ botanically a berry Ã¢ÂÂ produced by several kinds of large herbaceous flowering plants in the genus Musa'
Banana = ''.join(ch for ch in Banana if ch not in exclude)
print(Banana)


f = open("10kwords.txt","r")
tenwords = f.readlines()
f.close()

worddict = {}
i=0
for word in tenwords:
    worddict[word.strip().lower()] = i
    i+=1 

tensor = np.zeros(10000)

print()
for item in Akbar.split():
    if item.lower() in worddict:
        print(item)
        print(worddict[item.lower()])

        tensor[worddict[item.lower()]]+=1

print(tensor.sum())

tensor = np.zeros(10000)

print()
for item in Banana.split():
    if item.lower() in worddict:
        print(item)
        print(worddict[item.lower()])

        tensor[worddict[item.lower()]]+=1

print(tensor.sum())