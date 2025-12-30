from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

class Kmeans:
    def __init__(self, data, k:int=1) -> None:
        self.k = k
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


    def mainloop(self, plot:bool=False):
        """Currently uses the Kmeans algo to figure out k clusters in the data
            returns a list containing all the clusters"""
        self.initialization()

        if plot:
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

            if plot:
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
            # print(counter, self.cluster_means)
        if plot:
            plt.ioff()
            plt.show()
        return self.cluster_means
       
       
       
       
