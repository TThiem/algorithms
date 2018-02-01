# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:45:25 2017

@author: tthiem1

Module for the simulation of the gradient descent method.
"""

import numpy as np
from scipy.integrate import ode

def Gradient(x0, f, df, tRange=np.linspace(0, 20)):
    """
    Computes the minimum of f by using the gradient descent method.
    
    Parameters
    ==========
    x0 : (np.ndarray) - The initial guess for the minimum.
    f : (function) - The objective function to be minimized.
    df : (function) - The derivative of the function to be minimized.
    tRange : (np.ndarray) - An array of the output times for the integration.
    
    Returns
    =======
    positions : (np.ndarray) - An array of the positions of the independent
    variable at each time point given in trange. Shape (#dimensions, #times).
    """
    def RHS(t, y):
        """
        RHS function of the gradient descent.
        
        Parameters
        ==========
        t : (float) - The integration time variable.
        y : (np.ndarray) - The independent variable of the function
        to be minimized.
        """
        return -df(y)
    
    ODE = ode(RHS)
    ODE.set_integrator('dopri5')
    ODE.set_initial_value(x0, tRange[0])
    positions = np.empty((x0.size, tRange.size))
    for idx, _t in enumerate(tRange[1:]):
        positions[:, idx] = ODE.y
        ODE.integrate(_t)
    positions[:, -1] = ODE.y
    
    return positions
