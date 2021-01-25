import xml.etree.ElementTree as ET
import nltk
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
from termcolor import colored
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import re 
#nltk.download('stopwords')
stop_words = set(stopwords.words('english'))  
lemmatizer = WordNetLemmatizer() 
# textes[texte1[token][tagged],....]
textes = []
dictionnaire = []
# Rajouter le 10.txt
files = ["1.txt","2.txt","3.txt","4.txt","5.txt","6.txt","7.txt","8.txt","9.txt"]
for i in range(len(files)):
    textes.append([])
    dictionnaire.append([])
for f in range(len(files)):
    file = open(files[f],"r")
    print(files[f])
    texte = [[],[],[]]
    string = ""
    for ligne in file:
        string += ligne.rstrip('\n\r')

    # Segmentation 
    tokens = nltk.word_tokenize(string)
    texte[0].append(tokens)
    tagged = nltk.pos_tag(tokens)
    texte[1].append(tagged)
    textes[f].append(texte)
    lem = []
    # Lemmatisation + suppression mot vide
    for i in range(len(texte[1][0])):
        if(texte[1][0][i][0] not in stop_words):
            if(texte[1][0][i][1] == "NN"):
                lem.append(lemmatizer.lemmatize(texte[1][0][i][0],pos="n"))
            if(texte[1][0][i][1] == "JJ"):
                lem.append(lemmatizer.lemmatize(texte[1][0][i][0],pos="a"))
            if(texte[1][0][i][1] == "VB"):
                lem.append(lemmatizer.lemmatize(texte[1][0][i][0],pos="a"))
            if(texte[1][0][i][1] == "RB"):
                lem.append(lemmatizer.lemmatize(texte[1][0][i][0],pos="r"))
    # Dictionnaire
    for word in lem:
        exist = False
        for i in range(len(dictionnaire[f])):
            if(dictionnaire[f][i][0] == word):
                dictionnaire[f][i][2] = dictionnaire[f][i][2]+1
                exist = True
        if(exist == False):
            dictionnaire[f].append([word,f+1,1])

# Matrice d'incidence
matrice = []
for i in range(len(dictionnaire)):
    for j in range(len(dictionnaire[i])):
        present = []
        # word = dictionnaire[i][j][0]
        exist = False
        for w in range(len(matrice)):
            if(dictionnaire[i][j][0] == matrice[w][0]):
                exist = True
        if(exist == False):
            present.append(dictionnaire[i][j][0])
            for a in range(len(dictionnaire)):
                p = False
                for b in range(len(dictionnaire[a])):
                    if(dictionnaire[i][j][0] == dictionnaire[a][b][0]):
                        # mot présent dans le document a
                        present.append(1)
                        p = True
                        break
                if(p == False):
                    present.append(0)
            matrice.append(present)

# Index inversé 
index = []
for i in range(len(matrice)):
    ind = []
    for j in range(len(matrice[i])):
        # mot
        if(j == 0):
            ind.append(matrice[i][j])
        else :
        # document
            if(matrice[i][j] == 1):
                ind.append(j)
    index.append(ind)

# Requête

                    

