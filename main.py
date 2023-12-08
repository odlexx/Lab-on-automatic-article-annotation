import re
import heapq
import NLPmodule 
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

POS_to_exclude = ['INTJ', 'PRCL', 'CONJ', 'NPRO', 'PREP']

with open("articles/article3.txt", "r", encoding="UTF8") as f:
    text = f.read()

#разделение текста на предложения с помощью встроенной библиотеки
split_regex = re.compile(r'[.|!|?|…]')
#список документов (каждый документ - отдельное предложение)
documents = [t.strip() for t in split_regex.split(text)]

#список документов после обработки слов морфологическим анализатором, разделение по словам
list_of_docs = [[ morph.parse(NLPmodule.punctuation_marks_split(word))[0].normal_form  for word in doc.lower().split()] for doc in documents]

#удаляются служебные части речи
new_list_of_docs = list()
for i,doc in enumerate(list_of_docs):
    new_doc = list()
    for j,word in enumerate(doc):
        if not(morph.parse(word)[0].tag.POS in POS_to_exclude): new_doc.append(word)
    new_list_of_docs.append(new_doc)

#создается словарь слово -- tf
tf_dict = dict()
for doc in new_list_of_docs:
    for word in doc:
        tf_dict[word] = tf_dict.get(word,0) + 1

summed_tf = list()
averraged_tf = list()
for doc in new_list_of_docs:
    buff = 0
    for word in doc:
        buff += tf_dict[word]
    summed_tf.append(buff)
    averraged_tf.append(buff/len(doc))


summed_tf_max_ind = [summed_tf.index(val) for val in heapq.nlargest(6, summed_tf)]
averraged_tf_max_ind = [averraged_tf.index(val) for val in heapq.nlargest(9, averraged_tf)]

print('\n----------------------\n')
for x in summed_tf_max_ind:
    print(documents[x])

print('\n----------------------\n')
for x in averraged_tf_max_ind:
    print(documents[x])