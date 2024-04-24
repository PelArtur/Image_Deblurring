"""
Module: point_spread_functions.py

This module provides functions for generating Point Spread Functions (PSFs) commonly used in image processing applications.

Functions:
    - reshape_psf(psf: np.array, image_size: int) -> np.ndarray:
        Reshapes the given PSF (Point Spread Function) to matrix that match the desired image size.

    - gaussian(n: int, sigma: float, image_size: int) -> np.ndarray:
        Generates a Gaussian PSF with the specified parameters.

    - defocus(n: int, r: int, image_size: int) -> np.ndarray:
        Generates a PSF simulating defocused image with the specified radius.

Dependencies:
    - math
    - numpy as np
"""

import math
import numpy as np

def reshape_psf(psf: np.array, image_size: int) -> np.ndarray:
    """
    Reshapes the given PSF (Point Spread Function) to match the desired image size.

    ----------
    Parameters:
        - psf (np.array): The input PSF array.
        - image_size (int): The size of the desired image.
    ----------
    Returns:
        - np.array: The reshaped PSF array.
    """
    a = np.zeros((image_size, image_size)).astype(float)
    mid = psf.shape[0] // 2
    
    for i in range(image_size):
        for j in range(psf.shape[0]):
            if i + j - mid in range(image_size):
                a[i][i+j - mid] = psf[j]
                
    return a


def gaussian(n: int, sigma: float, image_size: int) -> np.ndarray:
    """
    Generates a Gaussian PSF with the specified parameters.

    ----------
    Parameters:
        - n (int): The size of the PSF array.
        - sigma (float): The standard deviation of the Gaussian distribution.
        - image_size (int): The size of the desired image.
    ----------
    Returns:
        np.array: The Gaussian PSF matrix.
    """
    res = np.zeros(n)
    
    a = 1 / (2 * math.pi * pow(sigma, 2))
    b = 2 * pow(sigma, 2)
    x_0 = n // 2
    
    matr_sum = 0
    for x in range(n):
        point_powers = pow(x - x_0, 2)
        res[x] = a * math.exp(- point_powers / b)
        matr_sum += res[x]
    
    normalize = 1 / matr_sum
    res *= normalize
    return reshape_psf(res, image_size)


def defocus(n: int, r: int, image_size: int) -> np.ndarray:
    """
    Generates a PSF simulating defocused image with the specified radius.

    ----------
    Parameters:
        - n (int): The size of the PSF array.
        - r (int): The radius parameter for the defocus.
        - image_size (int): The size of the desired image.
    ----------
    Returns:
        - np.ndarray: The defocused PSF matrix.
    """
    res = np.zeros(n)
    
    elem = 1 / (math.pi * pow(r, 2))
    
    mid = n // 2
    
    matr_sum = 0
    for i in range(res.shape[0]):
        if pow(i - mid, 2) <= pow(r, 2):
            res[i] = elem 
            matr_sum += res[i]
                
    normalize = 1 / matr_sum
    res *= normalize  
    
    return reshape_psf(res, image_size)
