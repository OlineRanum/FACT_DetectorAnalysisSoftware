import matplotlib.pyplot as plt 

class plot():

    def __init__(self, data):
        self.data = data


    def plot_FACT(self):      
        plt.scatter(self.data['z'], self.data['r'])
        plt.plot
        plt.show()
        