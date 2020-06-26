import pandas as pd
import os
import time
import numpy as np


class ReadFiles():
    def __init__(self, path, folder):
        self.path = path
        self.folder = folder

    def ToCSV(self):  
        start = time.time()
        for filename in os.listdir(self.path + self.folder):
            read_file = pd.read_table(self.path + self.folder+filename, header=None)
            read_file.to_csv (self.path+'Data.csv', index=None, header = None)
        end = time.time()
        df = pd.read_csv(self.path+'Data.csv', sep=",", names = ["N","t","tot"])
        df['t'] -= df['t'].loc[0]
        print('Reading all files: %.2f' % (end - start), 's')
        return df