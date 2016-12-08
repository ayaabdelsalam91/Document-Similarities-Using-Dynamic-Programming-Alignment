#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import random
import copy

def get_similar_pairs(text_files, score_files, output_path):
    foutput = open(output_path, 'w')
    for text_path, score_path in zip(text_files, score_files):
        start = text_path.find('STS.input.') + len('STS.input.')
        end = text_path.find('.txt')
        label = text_path[start:end]
        ftext = open(text_path)
        fscore = open(score_path)
        for text, score in zip(ftext, fscore):
            if float(score) > 4:
                foutput.write(label + '\t' + text.strip() + '\t' + score)

def read_file(fpath):
    f = open(fpath)
    labels = []
    texts1 = []
    texts2 = []
    # texts = []
    scores = []
    for line in f:
        label, t1, t2, score = line.strip().split('\t')
        labels.append(label.strip())
        texts1.append(t1.strip())
        texts2.append(t2.strip())
        # texts.append(t1.strip())
        # texts.append(t2.strip())
        # scores.append(float(score))
    return labels, texts1, texts2

def split_data(labels):
    all_labels = list(set(labels))
    label_idxs = []
    for i in range(len(all_labels)):
        label_idxs.append([])
    for idx, label in enumerate(labels):
        label_idxs[all_labels.index(label)].append(idx)
    return all_labels, label_idxs

def get_dataset(fpath, output_path, len_of_doc, num_of_doc):
    labels, texts1, texts2 = read_file(fpath)
    label_tokens, label_idxs = split_data(labels)
    fout = open(output_path, 'w')
    for label, idx_list in zip(label_tokens, label_idxs):
        pair_num = len(idx_list)
        possible_doc_num = int(pair_num/len_of_doc)
        if possible_doc_num < num_of_doc/2:
            print "We don't have enough similar pairs for label:", label
            print pair_num
            exit(0)
        for i in range(num_of_doc):
            doc_str1 = ''
            doc_str2 = ''
            selected_idxs1 = random.sample(idx_list, len_of_doc)
            selected_idxs2 = copy.copy(selected_idxs1)
            random.shuffle(selected_idxs1)
            for j, k in zip(selected_idxs1, selected_idxs2):
                doc_str1 += texts1[j].strip()
                doc_str1 += '\t'
                doc_str2 += texts2[k].strip()
                doc_str2 += '\t'
            doc_str1 = doc_str1.strip() + '\n'
            doc_str2 = doc_str2.strip() + '\n\n'
            fout.write(doc_str1+doc_str2)

if __name__ == '__main__':
    prefix = '/Users/Dantong_Ji/Desktop/STS/datasets+scoring_script/train'
    output_path = 'sen_concatenate_corpus.txt'
    similar_pair_path = 'similar_pairs.txt'
    text_files = [prefix+'/STS2012-en-test/STS.input.surprise.SMTnews.txt', prefix+'/STS2012-en-test/STS.input.MSRpar.txt', prefix+'/STS2012-en-train/STS.input.SMTeuroparl.txt']
    score_files = [fname.replace('input', 'gs') for fname in text_files]
    get_similar_pairs(text_files, score_files, similar_pair_path)
    get_dataset(similar_pair_path, output_path, 5, 50)