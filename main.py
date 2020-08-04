import heapq,math,json,re,unicodedata,numpy as np,pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from nltk.stem import PorterStemmer


with open(r'C:\Users\Gabriele\Desktop\vocabulary.json', 'r') as fp:
    data = json.load(fp) # this is the vocabulary, a dict with this shape --> key: 'word', value: 'index of the word'
with open(r'C:\Users\Gabriele\Desktop\doc_ids.json', 'r') as fp:
    doc_ids = json.load(fp) # this is the doc_ids, a dict with this shape --> key: 'title of the doc', value: 'index of the doc'
with open(r'C:\Users\Gabriele\Desktop\index1.json', 'r') as fp:
    index = json.load(fp) # index is the inverted index for the search engine 1,3: key: 'index of the word',
                          # value: 'list of doc that cointain that word'
with open(r'C:\Users\Gabriele\Desktop\json.json', 'r') as fp:
    url_title = json.load(fp) # this is a dict with this shape --> key: 'index of one doc',
                              # value: list of info of that doc (like: url, title, intro...)
with open(r'C:\Users\Gabriele\Desktop\index2.json', 'r') as fp:
    index2 = json.load(fp) # index2 is the inverted index for the search engine 2: key: 'index of the word',
                           # value: 'list of [doc that cointains that word, tfidf of doc and word]'

# input --> query
def preprocessor_query(query):
    stop_words = set(stopwords.words('english'))
    line = query.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    ps = PorterStemmer()

    word = line.split()
    # removing stop words
    words = [w for w in word if not w in stop_words]
    # removing Punctuation from each word
    punct_remove = [" ".join(tokenizer.tokenize(w)) for w in words]
    # removing stem
    stemmed = [ps.stem(w) for w in punct_remove]
    # removing Accent
    accents = [unicodedata.normalize(u'NFKD', w).encode('ascii', 'ignore').decode('utf8') for w in stemmed]
    line = " ".join(accents)

    string = ""
    string += line + "    "

    return string.strip().split()
# list of preprocessed words of the query

# search engine with only the conjunctive query
def search_engine_1():
    my_query = input('Search Engine 1: Please enter your query:  ')
    pre_query = preprocessor_query(my_query)

    set_docs = []

    for word in pre_query:
        if word in data.keys():
            id_term = str(data[word])

        if id_term in index.keys():
            set_docs.append(index[id_term])  ## index = inverted index

# these 2 for evauate the intersection between all the list of doc that contain one single word of the query
    for i in range(len(set_docs)):
        if i == 0:
            AND = set(set_docs[i])
        elif i == 1:
            second = set(set_docs[i])
            AND = AND.intersection(second)
        else:
            th = set(set_docs[i])
            AND = AND.intersection(th)

# this part is the creation of the dataframe to show the outputs
    titles = []
    intros = []
    urls = []

    for i in AND:
        titles.append(url_title[str(i)]['Title'])
        intros.append(url_title[str(i)]['Intro'])
        urls.append(url_title[str(i)]['Url'])

    df = pd.DataFrame(columns=['Title', 'Intro', 'Wikipedia Url'])
    df['Title'] = titles
    df['Intro'] = intros
    df['Wikipedia Url'] = urls

    return print(df)

# search engine with conjunctive query and ranking based one cosine similarity
def search_engine_2():

# this function takes the query and then calculates the tfidf of each word of the query,
# then it puts them inside a vector(the vector of tfidf of the query)
    def query_tfidf():  # it gets the query and returns a list ex. ["film","film"]
        my_query = input('Search Engine 2: Please enter your query:  ')
        query_list = []
        query = preprocessor_query(my_query)
        length = len(query)
        for _ in list(dict.fromkeys(query)):
            number = query.count(_)  # number is the size of the query
            tf = number / length  # calculating tf
            index_word = data[_]  # get the index of the word
            idf = math.log(30000 / len(index[str(index_word)]))
            tf_idf = tf * idf
            query_list.append(tf_idf)

        return query_list, query  # return tf_idf for the query.

    vec, pre_query = query_tfidf()


    set_docs = []

# these 2 for evauate the intersection between all the list of doc that contain one single word of the query
    for word in pre_query:
        if word in data.keys():
            id_term = str(data[word])

        if id_term in index.keys():
            set_docs.append(index[id_term])  ## index = inverted index

    for i in range(len(set_docs)):
        if i == 0:
            AND = set(set_docs[i])
        elif i == 1:
            second = set(set_docs[i])
            AND = AND.intersection(second)
        else:
            th = set(set_docs[i])
            AND = AND.intersection(th)

# this function gets from the inverted index the tfidf between the documents and the words of the query
# the it puts them in a dict with this shape --> key: 'doc id', value: list of tfidf
    def tfidf_docs():
        query = pre_query
        query = list(dict.fromkeys(query))
        dic_tfidf = {}
        for _ in range(len(query)):
            q_index = str(data[query[_]])
            tfidf_list = index2[q_index]  # it is a list
            for i in tfidf_list:
                tf_idf = i[1]
                doc_id = i[0]
                if doc_id not in dic_tfidf.keys():
                    dic_tfidf[doc_id] = [tf_idf]
                else:
                    dic_tfidf[doc_id].append(tf_idf)

        return dic_tfidf, query


    dict_tfidf_1 = {} # now we take only the documents that cointains all the words of the query togheter
    dict_tfidf, query = tfidf_docs()
    for k, v in dict_tfidf.items():
        if k in AND:
            dict_tfidf_1[k] = v

# we compute the cosine similarity for each doc and store them in a list --> (cosine similarity, doc_id)
    def cosine_similarity():
        similarity = []

        for k, v in dict_tfidf_1.items():
            cosine_sim = (np.dot(vec, v) / (np.linalg.norm(vec) * np.linalg.norm(v))) # we rank them by the cosine similarity
            similarity.append((cosine_sim, k))
        return similarity

# this part is  just for showing the outputs in a datafram(pandas)
    def dataframe_output():
        similarity = cosine_similarity()
        sort_docs = heapq.nlargest(len(similarity), similarity)
        titles = []
        intros = []
        urls = []
        scores = []

        for i in sort_docs:
            titles.append(url_title[str(i[1])]['Title'])
            intros.append(url_title[str(i[1])]['Intro'])
            urls.append(url_title[str(i[1])]['Url'])
            scores.append(i[0])

        df = pd.DataFrame(columns=['Title', 'Intro', 'Wikipedia Url', 'Cosine Similarity'])
        df['Title'] = titles
        df['Intro'] = intros
        df['Wikipedia Url'] = urls
        df['Cosine Similarity'] = scores

        return df

    return print(dataframe_output())

# this is a search engine with conjunctive query and a score
# the score is based on the absolute difference between the preferred duration time,
# chosen by the user and the real duration time of the found movies from the conjunctive query.
def search_engine_3():

    def conjunctive_query():
        my_query = input('Search Engine 3: Please enter your query:  ') # here we get the query and preprocess the query typed.
                                                                        # these 2 for evauate the intersection between all the list
                                                                        # of doc that contain one single word of the query
        pre_query = preprocessor_query(my_query)

        set_docs = []

        for word in pre_query:
            if word in data.keys():
                id_term = str(data[word])

            if id_term in index.keys():
                set_docs.append(index[id_term])    ## index = inverted index

        for i in range(len(set_docs)):
            if i == 0:
                AND = set(set_docs[i])
            elif i == 1:
                second = set(set_docs[i])
                AND = AND.intersection(second)
            else:
                th = set(set_docs[i])
                AND = AND.intersection(th)

        return AND, url_title

    def score(): # definition of the score based on the absolute difference of the duration time of the movies.
        AND, url_title = conjunctive_query()
        second_query = int(input('choose your preferred duration time: '))

        duration = {}
        minutes = []

        for i in AND:
            fi = open(r'C:\Users\Gabriele\Desktop\tsv\article-' + str(i) + '.tsv', encoding = 'utf8' )
            text = fi.read()
            fi.close()
            mins = []

            for j in range(13):
                mins.append(text[:text.find("\t")].strip())
                text = text[text.find("\t") + 1:]

            l = re.findall('\d+', mins[-3]) # here we have written a regex only on the number in the duration time field
            if len(l) >= 1:
                score = abs(second_query - int(l[0]))
                minutes.append((score, i))
            else:
                minutes.append((500, i))
            if len(l) >= 1:
                duration[str(i)] = int(l[0])
            else:
                duration[str(i)] = 'NA'   # if there is no info in the tsv file we set the value to NA
        # k = 15
        if len(AND) >= 15:
            sort_list = heapq.nsmallest(15, minutes)
        else:
            sort_list = heapq.nsmallest(len(AND), minutes) # here we sort the returned values based on the smallest
                                                           # difference between duration time and the input from the user.
                                                           # finally, we print 15 movies that fit the request.

        return sort_list, url_title, duration

    def dataframe_output(): # this part is for showing th output, using pandas dataframe.
        sort_list, url_title, duration = score()
        titles = []
        intros = []
        urls = []
        scores = []
        duration_time = []

        for i in sort_list:
            titles.append(url_title[str(i[1])]['Title'])
            intros.append(url_title[str(i[1])]['Intro'])
            urls.append(url_title[str(i[1])]['Url'])
            scores.append(i[0])
            duration_time.append(duration[str(i[1])])

        df = pd.DataFrame(columns = ['Title', 'Intro', 'Wikipedia Url', 'Duration time', 'Difference'])
        df['Title'] = titles
        df['Intro'] = intros
        df['Wikipedia Url'] = urls
        df['Duration time'] = duration_time
        df['Difference'] = scores


        return df

    return print(dataframe_output())

def wrapper_engines(): # this is the function that wraps all the search engines
                       # and here we get the input from the user, compare the user input and then
                       # execute the requested search engine.
    while(True):
        answer = int(input('Please Choose Your Desired Search Engine...You can choose 1,2 or 3  '))
        if answer in [1,2,3]:
            break
        else:
            print('Please Enter the correct engine number!!!! ')
    if answer == 1:
        search_engine_1()
    elif answer == 2:
        search_engine_2()
    elif answer == 3:
        search_engine_3()

wrapper_engines() # finally we execute wrapper function.