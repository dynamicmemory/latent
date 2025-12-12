import matplotlib.pyplot as plt
import numpy as np
from numpy._core.numeric import zeros_like
import pandas as pd
from collections import defaultdict

class Strategy:
    def __init__(self, df: pd.DataFrame):
        self.data = df

    def main(self):
        self.data.drop(["sma_50", "sma_100", "sma_200", "difference", "rsi", "volume"], axis=1, inplace=True)
        # print(self.data.tail(50))

        kmeans = Kmeans(self.data["volatility"].to_numpy())
        kmeans.mainloop()
        

# We build K means here
class Kmeans:
    def __init__(self, data):
        self.k = 3
        self.cluster_means = []
        self.data = data
        self.assignments = defaultdict(list) 


    def initialization(self):
        """ initializes K means of values between the low and high of a given 
            data range 
        """
        low = self.data.min()
        high = self.data.max()

        for _ in range(self.k):
            rng = np.random.default_rng().random()
            self.cluster_means.append(low + rng * (high - low))




    def assignment(self): 
        for sample in self.data:
            least_distance = float("inf")
            selected_k = None
            
            for mean in range(len(self.cluster_means)):
                temp_distance = np.sqrt((sample - self.cluster_means[mean])**2)
                if temp_distance < least_distance:
                    least_distance = temp_distance 
                    selected_k = mean 

            self.assignments[selected_k].append(sample)
                

    def update(self):
        for key, val in self.assignments.items():
            self.cluster_means[key] = np.mean(self.assignments[key])          


    def mainloop(self):
        self.initialization()

        plt.ion()
        fig, ax = plt.subplots()
        ax.scatter(self.data,np.zeros_like(self.data), c='grey', s=1)
        centroid = ax.scatter(self.cluster_means, np.zeros_like(self.cluster_means), c="red", s=200, marker="x")
        ax.set_ylim(-1, 1)

        not_finished = True
        counter = 0
        old_means = self.cluster_means.copy()
        while not_finished:
            self.assignment()
            self.update()

            new_offset = np.column_stack((self.cluster_means, np.zeros_like(self.cluster_means)))
            centroid.set_offsets(new_offset)
            plt.pause(0.5)

            for mean in range(len(self.cluster_means)):
                if (self.cluster_means[mean] - old_means[mean]) < 1e-4:
                    not_finished = False 
                else:
                    not_finished = True
                    break
            
            for mean in range(len(self.cluster_means)):
                old_means[mean] = self.cluster_means[mean]

            

            old_means = self.cluster_means.copy()
            self.assignments = defaultdict(list)
            counter += 1
            print(counter, self.cluster_means)
        plt.ioff()
        plt.show()
       

# Randomize k means 
# for each data point, assign them to the mean they are closest too 
# recalc the means using the mean of the newly assigned points 
# clear the lists and repeat till two cycles give identical mean or within epsilson



