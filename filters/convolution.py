import numpy as np
from scipy.ndimage import convolve

# Filtre fonksiyonları
def apply_mean_filter(image_array, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
    filtered = convolve(image_array, kernel, mode='reflect')
    return filtered.astype(np.uint8)

def apply_median_filter(image_array, kernel_size=3):
    padded = np.pad(image_array, kernel_size // 2, mode='reflect')
    output = np.zeros_like(image_array)
    h, w = image_array.shape

    for i in range(h):
        for j in range(w):
            region = padded[i:i+kernel_size, j:j+kernel_size]
            output[i, j] = np.median(region)

    return output

def apply_edge_filter(image_array):
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    filtered = convolve(image_array, kernel, mode='reflect')
    return np.clip(filtered, 0, 255).astype(np.uint8)
