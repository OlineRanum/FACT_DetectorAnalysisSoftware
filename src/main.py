from ReadFiles import ReadFiles
from DataManager import DataManager
from DataAnalyzer import DataAnalyzer
from plot import plot




PathData = '/home/oline/Documents/CERN/CHub/AEgIS/OnlineTools/LivePlotting/'
folder   = 'Data/'
RF = ReadFiles(PathData, folder)
data = RF.ToCSV()


DA = DataAnalyzer(data)
DA.Count_ActiveFibers()
t0, tmax, time, count = DA.FindRisingEdge()

DM = DataManager(data)
DM.SetTime(t0, tmax)
data = DM.FindCoordinates()

print(data.head())
print(data.tail())

P = plot(data)
P.plot_FACT()



