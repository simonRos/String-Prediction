#!/usr/bin/python
from SearchDataWeb import *
import json
import csv

#DEBUG
debug = True

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

#output unoptimized data structure
if debug == True:
    with open("phrase_debug.txt", 'w') as debugFile:
        for k,v in ww.nodes.items():
            debugFile.write(str(k))
            debugFile.write('\t'+str(len(v.followers))+'\n')
            for f in v.followers:
                debugFile.write('\t'+f.word)
                debugFile.write('\n\t\t'+str(v.followers[f])+'\n')

#output sudo json
if debug == True:
    ww.optimize()
    with open("json.txt", 'w') as debugFile:
        debugFile.write('{')
        debugFile.write('{')
        debugFile.write('\n\t"letterweb": {')
        for k,v in ww.letters.nodes.items():
            debugFile.write('\n\t\t{')
            debugFile.write('\n\t\t\t"word": "'+str(k)+'"')
            debugFile.write('\n\t\t\t"followers": {')
            for f in v.followers:
                debugFile.write('\n\t\t\t\t{')
                debugFile.write('\n\t\t\t\t\t"follower": '+f.letter)
                debugFile.write('\n\t\t\t\t\t"weight": '+str(v.followers[f]))
                debugFile.write('\n\t\t\t\t}')
            debugFile.write('\n\t\t\t}')
            debugFile.write('\n\t\t}')
        debugFile.write('\n\t}')
        debugFile.write('\n}')
        debugFile.write('\n{')
        debugFile.write('\n\t"wordweb": {')
        for k,v in ww.nodes.items():
            debugFile.write('\n\t\t{')
            debugFile.write('\n\t\t\t"word": "'+str(k)+'"')
            debugFile.write('\n\t\t\t"followers": {')
            for f in v.followers:
                debugFile.write('\n\t\t\t\t{')
                debugFile.write('\n\t\t\t\t\t"follower": '+f.word)
                debugFile.write('\n\t\t\t\t\t"weight": '+str(v.followers[f]))
                debugFile.write('\n\t\t\t\t}')
            debugFile.write('\n\t\t\t}')
            debugFile.write('\n\t\t}')
        debugFile.write('\n\t}')
        debugFile.write('\n}')
        debugFile.write('\n}')

#output optimized data structure
if debug == True:
    with open("optimize_debug.txt", 'w') as debugFile:
        for k,v in ww.nodes.items():
            debugFile.write(str(k))
            debugFile.write('\t'+str(len(v.followers))+'\n')
            for f in v.followers:
                debugFile.write('\t'+f.word)
                debugFile.write('\n\t\t'+str(v.followers[f])+'\n')

#output data structure for individual word prediction (True trie tree)
if debug == True:
    with open("word_debug.txt", 'w') as debugFile:
        for k,v in ww.letters.nodes.items():
            debugFile.write(str(k))
            debugFile.write('\t'+str(len(v.followers))+'\n')
            for f in v.followers:
                debugFile.write('\t'+f.letter)
                debugFile.write('\n\t\t'+str(v.followers[f])+'\n')
