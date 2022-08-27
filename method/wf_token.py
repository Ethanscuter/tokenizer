"""
This project used for Chinese word frequency collect.
"""

import collections
import pandas as pd
import jieba


def read_wordlist(word_list):
    with open(word_list, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    return [line.split(';')[0] for line in lines]


def read_corpus(corpus):
    with open(corpus, 'r') as f:
        lines = f.readlines()
    lines_tokenization = []
    for line in lines:
        line = "" + "/".join(jieba.cut(line, cut_all=True))
        lines_tokenization.append(line)
    return [line.strip().split('/')[:-1] for line in lines_tokenization]


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
    # corpus and wordlist direction
    corpus = '../data/weibo.csv'
    word_list = '../data/wordlist.csv'

    wordlist = read_wordlist(word_list)
    tokens = read_corpus(corpus)

    counter = count_corpus(tokens)
    token_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    # statistics based on the corpus
    # words = [candidate[0] for candidate in token_freqs]
    # number = [candidate[1] for candidate in token_freqs]
    #
    # all_result = pd.DataFrame(list(zip(words, number)), columns=['word', 'frequencies'])
    # all_result.to_csv('../result/final_wiki_all.csv', index=False)

    # tatistics based on the wordlist
    wordlist, statistics = stat(counter)

    result = pd.DataFrame(list(zip(wordlist, statistics)), columns=['word', 'frequencies'])
    result.to_csv('../result/weibo_token.csv', index=False)
