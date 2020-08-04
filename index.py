import heapq,math,json,os,re,io,string,nltk,unicodedata,numpy as np,pandas as pd
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from nltk.stem import PorterStemmer

def preprocessor(file):
    stop_words = set(stopwords.words('english'))
    text = file.read()
    file.close()
    ############################
    line_entry = text.lower()
    # taking only intro and plot
    intro_and_plot = []
    for i in range(3):
        intro_and_plot.append(line_entry[:line_entry.find("\t")].strip())
        line_entry = line_entry[line_entry.find("\t") + 1:]
    intro_and_plot.pop(0)  # only intro and plot

    # intro_and_plot is the list of sentences
    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()
    for _ in range(len(intro_and_plot)):
        # _ is a string
        word = intro_and_plot[_].split()
        # removing stop words
        words = [w for w in word if not w in stop_words]
        # removing Punctuation from each word
        punct_remove = [" ".join(tokenizer.tokenize(w)) for w in words]
        # removing stem
        stemmed = [ps.stem(w) for w in punct_remove]
        # removing Accent
        accents = [unicodedata.normalize(u'NFKD', w).encode('ascii', 'ignore').decode('utf8') for w in stemmed]
        intro_and_plot[_] = " ".join(accents)
    string = ""
    for _ in intro_and_plot:
        string += _ + "    "
    return string.strip()

word_li = []

def vocabulary(string):
    single_words = nltk.word_tokenize(string)
    for i in single_words:
        word_li.append(i)

# list of directory in one folder
for file in os.listdir(r"C:\Users\Gabriele\Desktop\tsv"):
    if file.endswith(".tsv"):
        path_fold = r"C:\Users\Gabriele\Desktop\tsv"
        file_to = open(os.path.join(path_fold, file), encoding = "utf8")
        vocabulary(preprocessor(file_to))

buffer = set(word_li)
word_list = list(buffer)
res = dict(zip(word_list, range(1, len(word_list)+1)))

with open(r'C:\Users\Gabriele\Desktop\vocabulary.json', 'r') as fp:
    data = json.load(fp)
with open(r'C:\Users\Gabriele\Desktop\doc_ids.json', 'r') as fp:
    doc_ids = json.load(fp)

reverse_index = {}

for file in os.listdir(r"C:\Users\Gabriele\Desktop\tsv"):
    if file.endswith(".tsv"):
        path_fold = r"C:\Users\Gabriele\Desktop\tsv"
        file_to = open(os.path.join(path_fold, file), encoding="utf8")
        file_string = preprocessor(file_to).split()

        for word in file_string:
            if word in data.keys():
                if data[word] not in reverse_index.keys():
                    reverse_index[data[word]] = [doc_ids[file]]
                else:
                    if doc_ids[file] not in reverse_index[data[word]]:
                        reverse_index[data[word]].append(doc_ids[file])

with open('index1.json', 'w') as fp:
    json.dump(reverse_index, fp)

with open('index1.json', 'r') as fp:
    index = json.load(fp)


def tf_idf(word, doc):
    lenght = len(doc)
    number = doc.count(word)
    tf = number / lenght
    idf = math.log(30000 / len(index[str(data[word])]))

    return tf * idf


index2 = {}

for file in os.listdir(r"C:\Users\Gabriele\Desktop\tsv"):
    if file.endswith(".tsv"):
        path_fold = r"C:\Users\Gabriele\Desktop\tsv"
        file_to = open(os.path.join(path_fold, file), encoding="utf8")
        file_string = preprocessor(file_to).split()

        for word in file_string:
            if word in data.keys():
                if data[word] not in index2.keys():
                    tfidf = tf_idf(word, file_string)
                    index2[data[word]] = [(doc_ids[file], tfidf)]
                else:
                    tfidf = tf_idf(word, file_string)
                    if (doc_ids[file], tfidf) not in index2[data[word]]:
                        index2[data[word]].append((doc_ids[file], tfidf))

with open('index2.json', 'w') as fp:
    json.dump(index2, fp)
