import numpy as np

def manual_threshold(image_array, threshold):
    binary = np.where(image_array > threshold, 255, 0)
    return binary.astype(np.uint8)
