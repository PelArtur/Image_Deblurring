"""
Image Deblurring Script

This script performs image deblurring using various parameters specified in a configuration file. It reads an 
input image, applies a specified Point Spread Function (PSF) to simulate blurring, optionally adds Gaussian noise, 
and then performs deblurring to recover the original image.

Usage:
    python image_deblurring.py config_file.cfg

Dependencies:
    - argparse
    - configparser
    - cv2 (OpenCV)
    - numpy

Functions:
    - parse_config(path: str) -> dict[str, Any]:
        Parses the configuration file and extracts parameters for image deblurring.

    - save_images(config: dict, blurred_image: np.ndarray, deblurred_image: np.ndarray) -> None:
        Saves the blurred and deblurred images to files specified in the configuration.

    - apply_psf(config: dict, image: np.ndarray, psf: np.ndarray) -> np.ndarray:
        Applies the Point Spread Function (PSF) to the input image to simulate blurring.

    - image_deblurring(config: dict) -> None:
        Performs the image deblurring process using the parameters specified in the configuration.

Usage Example:
    python image_deblurring.py config.cfg

This script can be used for various image deblurring tasks by adjusting parameters such as the PSF type, PSF parameters, noise addition, and image display.
"""
import argparse
import configparser
import cv2 as cv

import numpy as np
from typing import Any
from point_spread_functions import gaussian, defocus
from image_noise import gaussian_noise

#program data parsing
parser = argparse.ArgumentParser()
parser.add_argument('config_path', type=str)

args = parser.parse_args()

#global vars
psf_function = {0: gaussian,
                1: defocus}


def parse_config(path: str) -> dict[str, Any]:
    """
    Parses the configuration file and extracts parameters for image deblurring.

    ----------
    Parameters:
        - path (str): Path to the configuration file.
    ----------
    Returns:
        - dict[str, Any]: A dictionary containing the extracted parameters.
    """
    config = configparser.ConfigParser()
    config.read(path)
    
    config_data = dict()
    config_data["input_image"] = config.get('Params', 'input_image')  #str
    config_data["blurred_image"] = config.get('Params', 'blurred_image')
    config_data["deblurred_image"] = config.get('Params', 'deblurred_image')
    
    psf_num = config.getint('Params', 'psf')
    config_data["psf"] = psf_function[psf_num]
    config_data["n"] = config.getint('Params', 'n')
    config_data["psf_param"] = config.getint('Params', 'psf_param')
    
    config_data["add_noise"] = config.getboolean('Params', 'add_noise')
    config_data["mean"] = config.getfloat('Params', 'mean')
    config_data["var"] = config.getfloat('Params', 'var')
    
    config_data["show_images"] = config.getboolean('Params', 'show_images')
    config_data["color"] = config.getboolean('Params', 'color')
    
    return config_data
    

def save_images(config: dict, blurred_image: np.ndarray, deblurred_image: np.ndarray) -> None:
    """
    Saves the blurred and deblurred images to files specified in the configuration.

    ----------
    Parameters:
        - config (dict): Dictionary containing configuration parameters.
        - blurred_image (np.ndarray): Blurred image array.
        - deblurred_image (np.ndarray): Deblurred image array.
    ----------
    Returns:
        None
    """
    cv.imwrite(config["blurred_image"], (blurred_image * 255).astype(int)) 
    cv.imwrite(config["deblurred_image"], (deblurred_image * 255).astype(int)) 


def apply_psf(config: dict, image: np.ndarray, psf: np.ndarray) -> np.ndarray:
    """
    Applies the Point Spread Function (PSF) to the input image to simulate blurring.

    ----------
    Parameters:
        - config (dict): Dictionary containing configuration parameters.
        - image (np.ndarray): Input image array.
        - psf (np.ndarray): Point Spread Function array.
    ----------
    Returns:
        - np.ndarray: Blurred image array.
    """
    res = np.zeros_like(image)
    if config["color"]:
        for channel in range(3):
            res[:, :, channel] = np.matmul(psf, image[:, :, channel])
    else: 
        res = np.matmul(psf, image)
        
    return res


def image_deblurring(config: dict) -> None:
    """
    Performs the image deblurring process using the parameters specified in the configuration.

    ----------
    Parameters:
        - config (dict): Dictionary containing configuration parameters.
    ----------
    Returns:
        None
    """
    #convert image to matrix
    image = cv.imread(config["input_image"]).astype(float) / 255
    if not config["color"]:
        image = cv.imread(config["input_image"], cv.IMREAD_GRAYSCALE).astype(float) / 255

    #generate psf
    psf = config["psf"](config["n"], config["psf_param"], image.shape[0])
    
    #get blurred image
    blurred_image = apply_psf(config, image, psf)

    #If necessary, add noise
    if config["add_noise"]:
        mean = 0
        var = 0.1
        image_shape = (image.shape[0], image.shape[1])
        if config["color"]:
            for channel in range(3):
                blurred_image[:, :, channel] += gaussian_noise(mean, var, image_shape)
        else:
            blurred_image += gaussian_noise(mean, var, image_shape)

    #Decompose the PSF in SVD and take the inverse
    u, sig, vT = np.linalg.svd(psf)
    sig_2d = np.zeros_like(psf)

    for i in range(sig.shape[0]):
        sig_2d[i][i] = sig[i]

    psf_inverse = np.matmul(np.matmul(vT.transpose(), np.linalg.inv(sig_2d)), u.transpose())
    
    #Deblur image
    deblurred_image = apply_psf(config, blurred_image, psf_inverse)

    save_images(config, blurred_image, deblurred_image)

    if config["show_images"]:
        cv.imshow('Input Image', image)
        cv.imshow('Blurred Image', blurred_image)
        cv.imshow('deblurred Image', deblurred_image)
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == "__main__":
    # Parse configuration file and perform image deblurring
    config = parse_config(args.config_path)
    image_deblurring(config)
        