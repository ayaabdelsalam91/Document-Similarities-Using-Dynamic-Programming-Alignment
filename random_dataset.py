#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.corpus import reuters
import sys
import re
import random
import numpy
from sklearn.feature_extraction.text import CountVectorizer
#Comment

max_len = 200
min_len = 80

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

def write_to_file(articles, output_name):
    f = open(output_name, 'w')
    for sents in articles:
        article_str = ''
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


def select_news(output_name, min_len, max_len, max_article_num, stopwords):
    fids = reuters.fileids()
    selected = []
    selected_fids = []
    count = 0
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
        selected.append(content)
        selected_fids.append(fid)
        if count >= max_article_num:
            break
    write_to_file(selected, output_name)
    print count
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

def random_with_prob(freqs, num=1):
    cutoff = [freqs[0]]
    output = []
    for i in freqs[1:]:
        cutoff.append(cutoff[-1] + freqs[i])
    # print freqs
    # print cutoff
    for i in range(num):
        rand_num = random.randint(1, cutoff[-1])
        for j in range(len(cutoff)):
            if rand_num <= cutoff[j]:
                output.append(j)
                break
    if num == 1:
        return output[0]
    else:
        return output

def fuzz_articles(article_file, output_file, freq_file, proportion):
    articles = open(article_file)
    f = open(output_file, 'w')
    if type(proportion) != list:
        proportion = [proportion]
    voc, freqs = read_freq(freq_file)
    for line in articles:
        line = line.strip()
        new_articles = []
        new_articles.append(line+'\n')
        article_words = line.split(' ')
        for p in proportion:
            fuzzed = []
            for word in article_words:
                if random.random() < p:
                    behavior = random.random()
                    if behavior < 1/3:
                        pass
                    elif behavior < 2/3:
                        fuzzed.append(voc[random_with_prob(freqs)])
                    else:
                        fuzzed.append(voc[random_with_prob(freqs)])
                        fuzzed.append(word)
                else:
                    fuzzed.append(word)
            # print fuzzed
            new_articles.append(' '.join(fuzzed)+'\n')
        f.writelines(new_articles)
        f.write('\n')


if __name__ == "__main__":
    raw_fname = 'reuters_output.txt'
    raw_bow_freq = 'reuters_freq.txt'
    processed_fname = 'reuters_processed.txt'
    stopwords = get_wordlist('Stopwords.txt')
    max_article_num = 100
    puncts = get_wordlist('punctuation.txt')
    selected_fids = select_news(raw_fname, min_len, max_len, max_article_num, stopwords)
    print len(selected_fids)
    print selected_fids
    BOW_and_freq(raw_fname, raw_bow_freq)
    fuzz_articles(raw_fname, processed_fname, raw_bow_freq, proportion=[0.25, 0.5, 0.75])