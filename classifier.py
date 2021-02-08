from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from nltk.corpus import stopwords
import csv
import numpy as np
import io

stemmer = SnowballStemmer("portuguese")
with open('output.csv', newline='\n',encoding="utf-8") as csvfile:
    data = list(csv.reader(csvfile,delimiter=';'))

#Tira cabeçalho
data = data[1:]
# Data é um array de arrays, [classificacao,comentario]

data2 = list()
'''
Faz o 'stem' da palavra, ou seja,
salva apenas o radical
'''
rating = list()
review = list()
toPredict = list()
originalToPredict = list()
for row in data:
    # Apenas classificações 1,2 ou 5
    if int(row[0])!=-1:
        row2 = ''
        for word in row[1].split():
            row2 += stemmer.stem(word) + ' '
        data2.append([row2,row[0]])
        rating.append(int(row[0]))
        review.append(row2)
    else:
        row2 = ''
        for word in row[1].split():
            row2 += stemmer.stem(word) + ' '
        originalToPredict.append(row[1])
        toPredict.append(row2)
'''
Divide em dados de treino e teste
'''
features_train, features_test, labels_train, labels_test = train_test_split(review, rating, test_size=0.1, random_state=42)
# '''
# Aplica o algoritmo TFIDF para calcular
# a importância de um termo na frase
# '''
# vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
#                              stop_words=stopwords.words('portuguese'))
# features_train = vectorizer.fit_transform(features_train)
# features_test = vectorizer.transform(features_test).toarray()
#
# '''
# classificação
# '''
#
# clf = DecisionTreeClassifier()
# clf.fit(features_train, labels_train)
# print(clf.score(features_test, labels_test))
#
# '''
# Teste de predição
# '''
#
# test = 'essa upa é horrível nunca mais volto'
# rowTest = ''
# for word in test.split():
#     rowTest += stemmer.stem(test) + ' '
# rowTest = vectorizer.transform([rowTest])
#
# print(clf.predict(rowTest))

'''
Teste usando CountVectorizer (Parece ser melhor)
'''

count_vect = CountVectorizer(stop_words=stopwords.words('portuguese'))
features_train, features_test, labels_train, labels_test = train_test_split(review, rating, test_size=0.1, random_state=42)
features_train = count_vect.fit_transform(features_train)
features_test = count_vect.transform(features_test).toarray()

clf = DecisionTreeClassifier()
clf.fit(features_train, labels_train)
print(clf.score(features_test, labels_test))

'''test = 'essa upa é horrível nunca mais volto'
rowTest = ''
for word in test.split():
    rowTest += stemmer.stem(test) + ' '
rowTest = count_vect.transform([rowTest])

print(clf.predict(rowTest))'''

transformedToPredict = count_vect.transform(toPredict).toarray()

predictions = clf.predict(transformedToPredict)

strOutput = ''
for i in range(0, len(predictions)):
    strOutput+='>classe: ' + str(predictions[i]) + '\n' + originalToPredict[i] + '\n\n'

with open("output.txt", "w", encoding='utf-8') as txtFile:
    txtFile.write(strOutput)