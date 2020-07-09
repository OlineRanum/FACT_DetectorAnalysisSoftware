import pandas as pd
import os
import time
import numpy as np


class ReadFiles():
    def __init__(self, path, folder, filename):
        self.path = path
        self.folder = folder
        self.filename = filename

    def GetCSV(self):  
        read_file = pd.read_table(self.path + self.folder + self.filename, header=None)
        read_file.to_csv (self.path+'Data.csv', index=None, header = None)
        df = pd.read_csv(self.path+'Data.csv', sep=",", names = ["N","t","tot"])
        df['t'] -= df['t'].loc[0]

        return df