"""
This project used for Chinese word frequency collect.
"""

import collections
import pandas as pd
import jieba
from tqdm import tqdm
import os
import glob
import argparse


def FMM_func(user_dict, sentence):
    """
    Forward maximum matching（FMM）
    :param user_dict
    :param sentence
    """
    # the longest token in the dict.
    max_len = max([len(item) for item in user_dict])
    start = 0
    tokens = []
    while start != len(sentence):
        index = start+max_len
        if index > len(sentence):
            index = len(sentence)
        for i in range(max_len):
            if (sentence[start:index] in user_dict) or (len(sentence[start:index]) == 1):
                tokens.append(sentence[start:index])
                start = index
                break
            index += -1
    return tokens


def BMM_func(user_dict, sentence):
    """
    Backward maximum matching（BMM）
    :param user_dict
    :param sentence
    """
    # the longest token in the dict.
    max_len = max([len(item) for item in user_dict])
    result = []
    start = len(sentence)
    while start != 0:
        index = start - max_len
        if index < 0:
            index = 0
        for i in range(max_len):
            if (sentence[index:start] in user_dict) or (len(sentence[start:index])==1):
                result.append(sentence[index:start])
                start = index
                break
            index += 1
    return result


def read_wordlist(word_list):
    with open(word_list, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    return [line.split(';')[0] for line in lines]


def read_corpus(corpus, wordlist, method):
    with open(corpus, 'r') as f:
        lines = f.readlines()
    tokens = []
    for line in lines:
        line_tokens = method(wordlist, line)
        tokens.append(line_tokens)
    return tokens


def count_corpus(tokens):
    if len(tokens) == 0 or isinstance(tokens[0], list):
        tokens = [token for line in tokens for token in line]
    return collections.Counter(tokens)


def stat(counter):
    statistics = []
    for word in wordlist:
        statistics.append(counter[word])
    return wordlist, statistics


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--data_dir", default=None, type=str, required=True,
                        help="The input data dir.")
    parser.add_argument("--wordlist_dir", default='../data/wordlist.csv', type=str, required=False,
                        help="The wordlist dir.")
    parser.add_argument("--method", default='Maximum', type=str, required=False,
                        help="The method.")
    args = parser.parse_args()
    # corpus and wordlist direction
    # corpus = '../data/Wiki/wiki.csv'
    wordlist = read_wordlist(args.wordlist_dir)

    corpus = args.data_dir
    method_name = args.method

    if method_name == 'Maximum':
        print("Maximum matching is running: >>>")
        tokens = read_corpus(corpus, wordlist, FMM_func)
    elif method_name == 'Minimum':
        print("Minimum matching is running: >>>")
        tokens = read_corpus(corpus, wordlist, BMM_func)

    counter = count_corpus(tokens)
    token_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    # statistics based on the wordlist
    wordlist, statistics = stat(counter)

    result = pd.DataFrame(list(zip(wordlist, statistics)), columns=['word', 'frequencies'])

    # file_path = '../result/corpus_' + method_name + '.csv'
    file_path = '../result/weibo_max_' + method_name + '_' + corpus.split('/')[-1]
    result.to_csv(file_path, index=False)

    if method_name == 'Maximum':
        print("<<< Maximum matching result saved. " + "File name: " + corpus.split('/')[-1])
    elif method_name == 'Minimum':
        print("<<< Minimum matching result saved. " + "File name: " + corpus.split('/')[-1])
