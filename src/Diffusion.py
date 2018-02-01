# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:18:52 2017

@author: tthiem1

Module for simulating the 1d diffusion equation.
"""

import numpy as np
from scipy.integrate import simps

class Diffusion():
    """
    Class for simulating one-dimensional diffusion with zero Dirichlet boundary conditions.
    """
    
    def __init__(self, tRange, xRange, diffusionCoefficient, InitialConditions, tPoints=300, xPoints=101):
        """
        Initialze a diffusion object to solve the one-dimensional
        diffusion equation subject to zero Dirchlet boundary conditions.
        
        Parameters
        ==========
        tRange : (np.array) - An array containing the start time and end time
        for the diffusion simulation.
        xRange : (np.array) - An array containing the limits of the spatial
        variable x.
        diffusionCoefficient : (float) - The diffusion coefficient.
        InitialConditions: (function) - A function giving the initial conditions
        when evaluated at the x values of the grid.
        tPoints : (int) - The number of time points to use to span the interval provided
        in tRange.
        xPoints : (int) - The number of space points to use to span the space interval
        provided in xRange.
        """
        
        self.tRange = tRange
        self.diffusionCoefficient = diffusionCoefficient
        self.positions = np.linspace(xRange[0], xRange[1], xPoints)
        self.deltaX = (xRange[1] - xRange[0]) / (xPoints - 1)                
        self.deltaT = (tRange[1] - tRange[0]) / (tPoints - 1)
        self.F = self.diffusionCoefficient * self.deltaT / self.deltaX ** 2
        self.tPoints = tPoints
        self.xPoints= xPoints

        if self.F > 0.5:
            print('Warning solution unstable, F=%s, choose a smaller delta t.' % self.F)

        # Add two additional spatial ghost points for the symmetric difference method.
        # These points will satisfy the zero bondary conditions.
        self._solution = np.zeros((tPoints, xPoints + 2))
        
        # Set the interior points equal to the initial conditions.
        self._solution[0, 1:-1] = InitialConditions(self.positions)
        
        # Set the initial ghost points equal to zero for the zero Dirichlet condition.
        self._solution[0, 0], self._solution[0, -1] = 0, 0
        
    @property
    def solution(self):
        return self._solution[:, 1:-1]
        
    def simulate(self, method='forward'):
        """
        Simulate the diffusion dynamics using the given simulation method.
        
        Parameters
        ==========
        method : (string) - The numerical simulation method used to simulate
        the diffusion dynamics. Allowable values: 'forward', the forward Euler
        scheme.
        
        Returns
        =======
        solution : (np.array) - The solution at each position and time.
        positions : (np.array) - The spatial positions of the grid.
        """
        
        if method == 'forward':
            for time in range(0, self.tPoints - 1):
                # Update the ghost points.
                self._solution[time + 1, 0], self._solution[time + 1, -1] = self._solution[time, 0], self._solution[time, -1]
                # Update the interior points.
                for pos in range(1, self.xPoints + 1):
                    self._solution[time + 1, pos] = self._solution[time, pos] + self.F * (self._solution[time, pos + 1] - 2 * self._solution[time, pos] + self._solution[time, pos - 1])
        
        return (self.solution, self.positions)
    
    def selfSimilaritySolver(self):
        """
        Simulate the diffusion dynamics with rescaling after each time stepto highlight
        the self-similar behavior of the dynamics for specific initial conditions.
        The number of time points for this method refers to the number of times that
        the density is rescaled after a diffusion step.
        """
        def rescale(y):
            """
            Rescaling the diffusion solution. Currently hard coded for the default
            number of xPoints.
            """
            newVal = np.zeros(y.shape)
            newVal[45:56] = y[0::10]
            newVal /= simps(newVal, self.positions)
            
            return newVal
        
        self._solution[0, 1:-1] = rescale(self.solution[-1, :])

        return Diffusion.simulate(self)
    
def plug(x):
    """
    Plug initial conditions for diffusion.
    """
    output = np.zeros((x.shape[0]))
    output[np.logical_and(x < 1, x > -1)] = 0.5
    return output

if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    Simulation = Diffusion([0, 5], [-10, 10], 1, plug)
    solution, positions = Simulation.simulate()
    fig, ax = plt.subplots(nrows=1, ncols=5, figsize=(10, 6))
    for i in range(solution.shape[0]):
        ax[0].plot(positions, solution[i, :])
    for times in range(4):
        newsolution, positions = Simulation.selfSimilaritySolver()
        for i in range(newsolution.shape[0]):
            ax[times + 1].plot(positions, newsolution[i, :])
