# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:30:25 2017

@author: tthiem1

A module for running various optimization algorithms on a given objective function.
"""

import numpy as np
from sklearn.neighbors import KernelDensity
from scipy.spatial.distance import pdist
from itertools import product
from Gradient import Gradient
from Davidenko import Davidenko
from Nesterov import cNesterov

class OptimizationSolver():
    """
    A class for exploring self-similarities in optimization dynamical system solutions.
    """    
    def __init__(self, InitialConditions, TimeRange, TimeOut, ObjFunc=None, DObjFunc=None, DDObjFunc=None, Algorithm='Gradient'):
        """
        Initialize the self-similarity object with the data, the objective
        function and the evolution algorithm.
        
        Parameters
        ----------
        InitialConditions : (np.array) - An array of the initial conditions to use in the dynamical
        system simulation. Shape (#points, #dimensions).
        TimeRange : (np.array) - An array containing the start time and end time for the simulation.
        TimeOut : (int) - The number of points in time to output the results of the optimization.
        Positions : (np.array) - An array of the positions of the points after each optimization algorithm time step.
            Shape (#points, #dimensions, #times).
        ObjFunc : (function) - The objective function.
        DObjFunc : (function) - The derivative or Jacobian of the objective function.
        DDObjFunc : (function) - The second derivative or Hessian of the objective function.
        Algorithm : (string) - The evolution algorithm to use for the dynamical system. Possible values:
            'Newton' : the Newton method, 'Davidenko' : a continuous version of the Newton method,
            'Nesterov' : an accelerated gradient based optimization algorithm, 'Gradient' : the gradient descent method.
        """

        self.Times = np.linspace(TimeRange[0], TimeRange[1], TimeOut)
        self.Algorithm = Algorithm
        self.Positions = np.zeros((InitialConditions.shape[0], InitialConditions.shape[1], TimeOut))
        self.Positions[:, :, 0] = InitialConditions
        self.ObjFunc = ObjFunc
        self.DObjFunc = DObjFunc
        self.DDObjFunc = DDObjFunc
        
    def Simulate(self):
        """
        Simulate the dynamics of various optimization algorithms.
        
        Parameters
        ----------
        Algorithm : (string) - The evolution algorithm to use for the dynamical system. Possible values:
            'Newton' : the Newton method, 'Davidenko' : a continuous version of the Newton method,
            'Nesterov' : an accelerated gradient based optimization algorithm, 'Gradient' : the gradient descent method.
        
        Returns
        -------
        Positions : (np.array) - An array of the positions of the points after each optimization algorithm time step.
            Shape (#times, #points).
        Velocities : (np.array, Nesterov method only) - An array of the velocities of the points after each Nesterov time step.
            Shape (#times, #points).
        """
        if self.Algorithm == 'Gradient':
            for i in range(self.Positions.shape[0]):
                self.Positions[i, :, :] = Gradient(self.Positions[i, :, 0], self.ObjFunc, self.DObjFunc, self.Times)
        elif self.Algorithm == 'Davidenko':
            for i in range(self.Positions.shape[0]):
                self.Positions[i, :, :] = Davidenko(self.Positions[i, :, 0], self.DObjFunc, self.DDObjFunc, self.Times)
        elif self.Algorithm == 'Nesterov':
            self.Velocities = np.zeros((self.Positions.shape))
            for i in range(self.Positions.shape[0]):
                self.Positions[i, :, :], self.Velocities[i, :, :] = cNesterov(self.Positions[i, :, 0], self.ObjFunc, self.DObjFunc, self.Times)

    def GetDensity(self, action='generate', samples=100, draws=None):
        """
        TODO: Check density calculations for multiple dimensions.
        Generate a density estimation of the positions at each time or sample positions
        from the generated density at a specified time.
        
        Parameters
        ----------
        action : (string) - Options: 'generate', 'sample'.
            'generate' : Generate a density estimation using kernel density estimation and save it.
            'sample' : Generate a density estimation at the final time and both draw and return samples
                from it equal to the number of points in position.
        samples : (int) - The number of sample points in each dimension at which to measure the density.
            Total number of points is samples ** dimensions.
        draws : (int) - The number of points to draw from the density distribution, if None,
            draw a number of points equal to the number of points in Positions.
            
        Returns
        -------
        'generate'        
            DensitySamples : (np.array) - An array of the positions of the points used to sample the density.
            Density : (np.array) - The value of the density evaluated at each points in DensitySamples.
        'sample'
            samples : (np.array) - An array of the samples drawn from the density generated from the positions
                at the final time.
        """
        if action == 'generate':
#           A list of sample arrays ranging from the min value to the max value in each dimension.
            minmax = [np.linspace(np.amin(self.Positions[:, i, :]), np.amax(self.Positions[:, i, :]), samples) for i in range(self.Positions.shape[1])]
            self.DensitySamples = np.array(list(product(*minmax)))
            self.Density = np.zeros((self.DensitySamples.shape[0], self.Times.shape[0]))
            
            for i in range(self.Positions.shape[2]):
                bandwidth = 0.2 * np.mean(pdist(self.Positions[:, :, i]))
                KDE = KernelDensity(bandwidth=bandwidth, kernel='gaussian', metric='euclidean')
                KDE.fit(self.Positions[:, :, i])
                self.Density[:, i] = np.exp(KDE.score_samples(self.DensitySamples))
        
        elif action == 'sample':
            bandwidth = min(pdist(self.Positions[-1, :][:, np.newaxis]))
            KDE = KernelDensity(bandwidth=bandwidth, kernel='gaussian', metric='euclidean')
            KDE.fit(self.Positions[-1, :][:, np.newaxis])
            if draws is None:
                draws = self.Positions.shape[1]
            return KDE.sample(draws)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
#    InitialConditions = np.array([(x, y) for x in range(-2, 3) for y in range(-2, 3)])
    InitialConditions = np.array([(np.sin(x), np.cos(x)) for x in 2 * np.pi * np.linspace(0, 0.99, 100)])
    TimeRange = [0, 5]
    TimeOut = 100
    ObjFunc = lambda x: x[0] ** 2 + x[1] ** 2
    DObjFunc = lambda x: np.array((2 * x[0], 2 * x[1]))
    DDObjFunc = lambda x: np.array([[2, 0], [0, 2]])
    methods = ['Gradient', 'Davidenko', 'Nesterov']
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    for i in range(3):
        optimization = OptimizationSolver(InitialConditions, TimeRange, TimeOut, ObjFunc, DObjFunc, DDObjFunc, Algorithm=methods[i])
        optimization.Simulate()
        for j in range(InitialConditions.shape[0]):
            ax[i].scatter(optimization.Positions[j, :, :][0, :], optimization.Positions[j, :, :][1, :])
        ax[i].set_title(methods[i])
        ax[i].set_xlabel('Time')
        ax[i].set_xlabel('Position')
    plt.tight_layout()
