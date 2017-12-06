# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 13:09:31 2017

@author: tthiem1

Module for the simulation of the continuous Newton's method (Davidenko method).
"""

import numpy as np
from scipy.integrate import ode

def Davidenko(x0, f, gradf, trange=np.linspace(0, 20)):
    """
    Computes the minimum of f by using the continuous Newton's method (Davidenko).
    
    Parameters
    ==========
    x0 : (np.ndarray) - The initial guess for the minimum.
    f : (function) - The function to be minimized.
    gradf : (function) - The gradient of the function to be minimized.
    trange : (np.ndarray) - An array of the output times for the integration.
    
    Returns
    =======
    positions : (np.ndarray) - An array of the positions of the independent
    variable at each time point given in trange.
    """
    def RHS(t, y):
        """
        RHS function of the Davidenko equation.
        
        Parameters
        ==========
        t : (float) - The integration time variable.
        y : (np.ndarray) - The independent variable of the function
        to be minimized.
        """
        return -f(y) / gradf(y)
    
    ODE = ode(RHS)
    ODE.set_integrator('dopri5')
    ODE.set_initial_value(x0, trange[0])
    positions = np.empty((x0.size, trange.size))
    for idx, _t in enumerate(trange[1:]):
        positions[:, idx] = ODE.y
        ODE.integrate(_t)
    positions[:, -1] = ODE.y
    
    return positions
        