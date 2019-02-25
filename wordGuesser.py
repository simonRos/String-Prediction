#!/usr/bin/python
from SearchDataWeb import *
import csv

product_list = []
file_name = input("File name: ")
with open(file_name, 'r') as f:
  reader = csv.reader(f)
  product_list = list(reader)


clean_list = []
for product in product_list:
    clean_list.append(product[0].replace('"', ''))

ww = WordWeb()
ww.add(clean_list)
ww.optimize()

while True:
    inString = input("[Enter]: ")
    letterG = ""
    try:
        letterG = ww.letters.nodes[inString].guessNextLetter()
    except:
        letterG = "[No Guess]"
    print("Letter?\t"+str(letterG))
    wordG = ""
    try:
        wordG = ww.letters.guessWord(inString)
    except:
        wordG = "[No Guess]"
    print("Word?\t"+str(wordG))
    nextG = ""
    try:
        nextG = ww.nodes[wordG].guessNextWord()
    except:
        nextG = "[No Guess]"
    print("Next?\t"+str(nextG))
    phraseG = ""
    try:
        phraseG = ww.guessPhrase(wordG, 6)
    except Exception as e:
        print("ERROR: "+str(e))
        phraseG = "[No Guess]"
    print("Phrase?\t"+str(phraseG))
    print('\n')
