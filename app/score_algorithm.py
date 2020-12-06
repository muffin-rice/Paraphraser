import spacy;
import re;
from collections import defaultdict
import en_core_web_sm

# Text Preprocessing Pkg
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
punc = list(punctuation)
nlp = en_core_web_sm.load()
#nlp = spacy.load('en_core_web_sm')

# Build a List of Stopwords
stopwords = list(STOP_WORDS)
whitelist = {};

INTERNAL_SCALE_FACTOR = 1;
EXTERNAL_SCALE_FACTOR = 2;

def cleanStringPunc(string):
    for i in punc:
        string=string.replace(i,'')
    return string;

def scale(d, proportion):
    maximum_frequency = max(d.values())
    d = {word : freq/maximum_frequency * proportion for word, freq in d.items()}

#Merge dict2 into dict1
def mergeDict(dict1, dict2):
    for i in dict2.keys():
        word = i.lower();
        if word not in dict1.keys():
            dict1[word] = dict2[i]
        else:
            dict1[word] += dict2[i]

def summarize(document : str, keywords : [str] = []):
    # Build an NLP Object
    docx = nlp(document)
    stripdoc = nlp(cleanStringPunc(document).lower());

    # Build Word Frequency
    # word.text is tokenization in spacy
    word_frequencies = {}
    for word in stripdoc:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    # Maximum Word Frequency
    scale(word_frequencies, INTERNAL_SCALE_FACTOR)
    keywords = {k : EXTERNAL_SCALE_FACTOR for k in keywords}
    #scale(keywords,EXTERNAL_SCALE_FACTOR)
    mergeDict(word_frequencies,keywords)
    # Frequency Table

    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Sentence Score via comparing each word with sentence
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Import Heapq
    from heapq import nlargest
    summarized_sentences = nlargest(10, sentence_scores, key=sentence_scores.get)
    #print(summarized_sentences)
    final_sentences = [ w.text for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    return summary;