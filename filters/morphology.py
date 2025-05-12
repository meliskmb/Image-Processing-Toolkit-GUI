import numpy as np

# 3x3 Yapısal Eleman ile
def dilation(binary_image):
    kernel = np.ones((3, 3), dtype=np.uint8)
    padded = np.pad(binary_image, pad_width=1, mode='constant', constant_values=0)
    result = np.zeros_like(binary_image)

    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            region = padded[i:i+3, j:j+3]
            if np.any(region & kernel):
                result[i, j] = 255
    return result

def erosion(binary_image):
    kernel = np.ones((3, 3), dtype=np.uint8)
    padded = np.pad(binary_image, pad_width=1, mode='constant', constant_values=0)
    result = np.zeros_like(binary_image)

    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            region = padded[i:i+3, j:j+3]
            if np.all(region & kernel):
                result[i, j] = 255
    return result
