#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.corpus import reuters
import sys
import re
import random
import numpy
from sklearn.feature_extraction.text import CountVectorizer
#Comment

max_len = 300
min_len = 100

def get_wordlist(fname):
    f = open(fname)
    word_list = []
    for line in f:
        word_list.append(line.strip().lower())
    f.close()
    return word_list

def read_freq(fname):
    f = open(fname)
    words = []
    freqs = []
    for line in f:
        w, f = line.strip().split(' ')
        words.append(w)
        freqs.append(int(f))
    return words, freqs

def process_raw(sentences, stopwords):
    revised_sents = []
    for s in sentences:
        for idx in range(len(s))[::-1]:
            s[idx] = s[idx].lower().strip()
            if s[idx] in stopwords or (not s[idx].isalpha()):
                del(s[idx])
        revised_sents.append(s)
    return revised_sents

def write_to_file(labels, articles, output_name):
    f = open(output_name, 'w')
    for label, sents in zip(labels, articles):
        article_str = label + '\t'
        for sen in sents:
            for word in sen:
                article_str += word + ' '
            if len(sen) > 0:
                article_str += '. '
        article_str = article_str.strip()
        article_str += '\n'
        # print article_str
        f.write(article_str)
    f.close()


def select_news(output_name, categories, cat_num, min_len, max_len, stopwords):
    selected = []
    labels = []
    selected_fids = []
    for cat in categories:
        count = 0
        fids = reuters.fileids(cat)
        print len(fids)
        for fid in fids:
            content = reuters.sents(fid)
            word_num = sum([len(sen) for sen in content])
            if word_num < min_len:
                continue
            content = process_raw(content, stopwords)
            word_num = sum([len(sen) for sen in content])
            if word_num < min_len or word_num > max_len:
                continue
            count += 1
            labels.append(cat)
            selected.append(content)
            selected_fids.append(fid)
            if count >= cat_num:
                break
        print '**', count
    write_to_file(labels, selected, output_name)
    return selected_fids

def read_raw(fname):
    f = open(fname)
    articles = []
    for line in f:
        sents = line.strip().split('.')
        for idx in range(len(sents)):
            if sents[idx] != '':
                sents[idx] = sents[idx].strip().split(' ')
        articles.append(sents)
    f.close()
    return articles


def BOW_and_freq(fname, output_name):
    articles = read_raw(fname)
    freq = {}
    for sents in articles:
        for s in sents:
            for word in s:
                if word in freq:
                    freq[word] += 1
                else:
                    freq[word] = 1
    f = open(output_name, 'w')
    print len(freq)
    for word in sorted(freq.keys()):
        f.write(word+' '+str(freq[word])+'\n')
    f.close()

if __name__ == "__main__":
    raw_fname = 'reuters_with_puc.txt'
    raw_bow_freq = 'reuters_punc_freq.txt'
    stopwords = get_wordlist('Stopwords.txt')
    # puncts = get_wordlist('punctuations.txt')
    selected_fids = select_news(raw_fname, ['earn', 'money-fx', 'trade', 'acq','crude'], 50, min_len, max_len, stopwords)
    # print len(selected_fids)
    # print selected_fids
    # BOW_and_freq(raw_fname, raw_bow_freq)
    # fuzz_articles(raw_fname, processed_fname, raw_bow_freq, proportion=[0.25, 0.5, 0.75])