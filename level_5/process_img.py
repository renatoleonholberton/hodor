"""This module contains a function to process an image
to be used for an OCR """
import cv2
import numpy as np

def blur(img_path):
    """Processes an image to make it readable for an
    Object Character Recognition (OCR) library"""
    img = cv2.imread(img_path)
    _, th = cv2.threshold(img, 128, 255, cv2.THRESH_TOZERO)
    gauss = cv2.GaussianBlur(th, (3, 3), 1)
    blur = cv2.blur(gauss, (3, 3))
    _, result = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    return result


def morphology(img_path):
    """Processes an image to be read by an OCR"""
    img = cv2.imread(img_path)
    _, img = cv2.threshold(img, 128, 255, cv2.THRESH_TOZERO)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2, 2), np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    erosion = cv2.erode(closing, kernel=kernel, iterations=1)
    return erosion