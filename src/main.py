from ReadFiles import ReadFiles
from Setup import Setup
from AnalysisToolBox import AnalysisToolBox
from plot import plot
from LoadData import LoadData
from FileConverter import FileConverter
from UnitTesting import UnitTesting
import time

start = time.time()


PathData = '/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/'
PathSettings_csv = 'settings/settings.csv'
PathSettings_txt = 'settings/settings.txt'
folder   = 'Data/'

FC = FileConverter(PathSettings_csv, PathSettings_txt)
FC.Txt2CSV()

param = LoadData(PathSettings_csv)
param.Initiate() 

RF = ReadFiles(PathData, folder)
data = RF.GetCSV()

UT = UnitTesting()
UT.SetupTestingEnvironment()


"""
build = Setup(data, param)
data  = build.Initiate() 

ATB = AnalysisToolBox(data, param, build)
ATB.Initiate_Standard_Analysis()

#P = plot(data, param, build)
#P.plot_FACT_live()
"""
end = time.time()
print('Full Run: %.5f' % (end - start), 's')


