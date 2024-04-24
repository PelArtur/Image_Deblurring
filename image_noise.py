"""
Function: gaussian_noise(mean: float, var: float, image_shape: np.ndarray) -> np.ndarray

Generates Gaussian noise with the given mean, variance, and image shape.

Parameters:
    - mean (float): Mean value of the Gaussian distribution.
    - var (float): Variance of the Gaussian distribution.
    - image_shape (np.ndarray): Shape of the image to generate noise for, e.g., (height, width).

Returns:
    np.ndarray: A NumPy array containing the generated Gaussian noise with values rounded to integers.
"""
import numpy as np
 
def gaussian_noise(mean: float, var: float, image_shape: np.ndarray) -> np.ndarray:
    """
    Generates Gaussian noise with the given mean, variance, and image shape.

    ----------
    Parameters:
        - mean (float): Mean value of the Gaussian distribution.
        - var (float): Variance of the Gaussian distribution.
        - image_shape (np.ndarray): Shape of the image to generate noise for, e.g., (height, width).
    ----------
    Returns:
       - np.ndarray: A NumPy array containing the generated Gaussian noise with values rounded to integers.
    """
    sigma = var ** 0.5
    gaussian_noise = np.random.normal(mean, sigma, image_shape).astype('uint8')
    
    return gaussian_noise