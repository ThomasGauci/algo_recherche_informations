import xml.etree.ElementTree as ET
import nltk
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
from termcolor import colored
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import re 
import math as m
#nltk.download('stopwords')
stop_words = set(stopwords.words('english'))  
lemmatizer = WordNetLemmatizer() 
# textes[texte1[token][tagged],....]
textes = []
dictionnaire = []
files = ["1.txt","2.txt","3.txt","4.txt","5.txt","6.txt","7.txt","8.txt","9.txt"]
for i in range(len(files)):
    textes.append([])
    dictionnaire.append([])
for f in range(len(files)):
    file = open(files[f],"r")
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
            if(texte[1][0][i][1][0] == "N"):
                lem.append(lemmatizer.lemmatize(texte[1][0][i][0],pos="n"))
            if(texte[1][0][i][1][0] == "J"):
                lem.append(lemmatizer.lemmatize(texte[1][0][i][0],pos="a"))
            if(texte[1][0][i][1][0] == "V"):
                lem.append(lemmatizer.lemmatize(texte[1][0][i][0],pos="v"))
            if(texte[1][0][i][1][0] == "R"):
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

def affichage(res):
    res_sorted = sorted(res, key=lambda res: res[1], reverse=True) # On tri les documents en fonction de leurs scores
    print("------CLASSEMENT PERTINENCE------")
    print("REQUETE : " + requete)
    for i in range(len(res_sorted)):
        print(str(i+1) + "- " + res_sorted[i][0] + " score : " + str(res_sorted[i][1]))

# Requête complexe
def requete_complexe(requete,print):
    # Segmentation
    tokens = nltk.word_tokenize(requete)
    string = nltk.pos_tag(tokens)
    lem = []
    # Lemmatisation + suppression mot vide
    for i in range(len(string)):
        if(string[i][0] not in stop_words):
            if(string[i][1][0] == "N"):
                lem.append(lemmatizer.lemmatize(string[i][0],pos="n"))
            if(string[i][1][0] == "J"):
                lem.append(lemmatizer.lemmatize(string[i][0],pos="a"))
            if(string[i][1][0] == "V"):
                lem.append(lemmatizer.lemmatize(string[i][0],pos="v"))
            if(string[i][1][0] == "R"):
                lem.append(lemmatizer.lemmatize(string[i][0],pos="r"))
    # On cherche le mot dans notre dictionnaire pour obtenir sa fréquence
    res = [] # score des documents
    for f in files:
        res.append([f,0])
    for word in lem:
        idf = 0
        for i in range(len(index)):
            if(index[i][0] == word):
                docT = 0
                for j in range(len(index[i])):
                    if(j != 0):
                        if(index[i][j] == 1):
                            docT += 1
                if(docT != 0):
                    idf = m.log(len(files)/docT) # The log of the number of documents divided by the number of documents that contain the word w.
        for i in range(len(dictionnaire)):
            for j in range(len(dictionnaire[i])):
                if(dictionnaire[i][j][0] == word):
                    res[i][1] += (dictionnaire[i][j][2]/len(dictionnaire[i])) * idf
    if(print):
        affichage(res)
    return res

# Requête
def requete_booleen(requete):
    mots = requete.split()
    search_AND = []
    search_OR = []
    search_NOT = []
    for x in range(len(mots)):
        if(x == 0 and mots[x] != "AND" or mots[x] != "NOT" or mots[x] != "OR"):
            search_AND.append(mots[x])
        if(mots[x] == "AND"):
            if(mots[x+1] != "AND" or mots[x+1] != "NOT" or mots[x+1] != "OR"):
                search_AND.append(mots[x+1])
        if(mots[x] == "OR"):
            if(mots[x+1] != "AND" or mots[x+1] != "NOT" or mots[x+1] != "OR"):
                search_AND.append(mots[x+1])
        if(mots[x] == "NOT"):
            if(mots[x+1] != "AND" or mots[x+1] != "NOT" or mots[x+1] != "OR"):
                search_AND.append(mots[x+1])
    str = ""
    for word in search_AND:
        str += word + " "
    res_AND = requete_complexe(str,False)
    res_OR = []
    for word in search_OR: 
        res_OR.append(requete_complexe(str,False))
    str = ""
    for word in search_NOT:
        str += word + " "
    res_NOT = requete_complexe(str,False)
    res_Total = []
    if(len(res_AND) != 0):
        res_Total = res_AND
    elif(len(res_OR) != 0):
        res_Total = res_AND
    
    for x in range(len(res_Total)):
        for y in range(len(res_NOT)):
            res_Total[x][1] = res_Total[x][1] - res_NOT[y][1]
        for y in range(len(res_OR)):
            for z in range(len(res_OR[y])):
              res_Total[x][1] = res_Total[x][1] + res_NOT[y][z][1]
    affichage(res_Total)

requetesB = ["desease AND severe AND pneumonia","antibody AND plasma AND cells OR receptors","antimalarial drugs OR antiviral agents OR immunomodulators",
"NOT plasma AND risk of infection AND restritions","older adults AND antibodies AND NOT genomes OR variant"]
for requete in requetesB:
    requete_booleen(requete)     


requetes = ["antibody treatments","efficacy and safety of the treatments","family access to hospitals","contact tracing results","genomic analysis of SARS-CoV-2 disease"]
for requete in requetes:
    requete_complexe(requete,True)                  



# TF IDF 
# TF : The number of times a word appears in a document divded by the total number of words in the document. Every document has its own term frequency.


