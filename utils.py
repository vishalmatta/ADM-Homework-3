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


