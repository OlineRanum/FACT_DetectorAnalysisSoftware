import pandas as pd


class FileConverter():

    def __init__(self, path_settings_csv, path_settings_txt):
        self.path_settings_csv = path_settings_csv
        self.path_settings_txt = path_settings_txt

    def Txt2CSV(self):
        read_file = pd.read_table(self.path_settings_txt, header = 0, sep = ' ')
        read_file = read_file.T
        read_file.to_csv(self.path_settings_csv, index=None, header = None)

