import numpy as np
 
def gaussian_noise(mean, var, image_shape):
    sigma = var ** 0.5
    gaussian_noise = np.random.normal(mean, sigma, image_shape).astype('uint8')
    
    return gaussian_noise