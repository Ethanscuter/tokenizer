"""
This project used for Chinese word frequency collect.
"""

import collections
import pandas as pd
import jieba
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


def tokenizer(line):
    line = "" + "/".join(jieba.cut(line, cut_all=True))
    return line.strip().split('/')[:-1]


def check_token(max_line, token_line):
    after_check_token = []
    for word in max_line:
        if len(word) <= 2:
            if word in token_line:
                after_check_token.append(word)
        else:
            after_check_token.append(word)
    return after_check_token


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
        tokenizer_tokens = tokenizer(line)
        after_check_token = check_token(line_tokens, tokenizer_tokens)
        tokens.append(after_check_token)
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
    args = parser.parse_args()
    # corpus and wordlist direction
    # corpus = '../data/Wiki/wiki.csv'
    wordlist = read_wordlist(args.wordlist_dir)

    corpus = args.data_dir
    tokens = read_corpus(corpus, wordlist, FMM_func)

    counter = count_corpus(tokens)
    token_freqs = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    # statistics based on the wordlist
    wordlist, statistics = stat(counter)

    result = pd.DataFrame(list(zip(wordlist, statistics)), columns=['word', 'frequencies'])

    file_path = '../result/weibo_hybrid_split_' + '_' + corpus.split('/')[-1]
    result.to_csv(file_path, index=False)


