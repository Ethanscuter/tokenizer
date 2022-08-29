import glob
import numpy as np
import pandas as pd

file_list = glob.glob('./result/*.csv')  # need to be specified as the results folder

cur = 1

for file in file_list:
    if cur == 1:  # init
        init_df = pd.read_csv(file)
        cur += 1
    else:
        update_df = pd.read_csv(file)
        init_df['frequencies'] = init_df['frequencies'] + update_df['frequencies']

file_to_save = './result/corpus_method.csv' # need to be changed where you want to save it
init_df.to_csv(file_to_save, index=False)
