from ReadFiles import ReadFiles
from Setup import Setup
from AnalysisToolBox import AnalysisToolBox
from plot import plot
from LoadData import LoadData
from FileConverter import FileConverter
from test_Setup import TestSetup
import time
from RunAnalysis import RunAnalysis

start = time.time()


PathData = '/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/'
PathSettings_csv = 'settings/settings.csv'
PathSettings_txt = 'settings/settings.txt'
folder   = 'Data/'

FC = FileConverter(PathSettings_csv, PathSettings_txt)
FC.Txt2CSV()

param = LoadData(PathSettings_csv)
param.Initiate() 


RA = RunAnalysis(param, PathData, folder)
#df_z = RA.RunSingleFileAnalysis('169627_11.txt')
df_z = RA.RunMultiFileAnalysis()
P = plot(None, param, None)
#P.plot_FACT_live()
P.hist(df_z)

end = time.time()
print('Full Run: %.5f' % (end - start), 's')


