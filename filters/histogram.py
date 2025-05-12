import numpy as np
import matplotlib.pyplot as plt

def calculate_histogram(image_array):
    histogram = np.zeros(256, dtype=int)
    for value in image_array.flatten():
        histogram[value] += 1
    return histogram

def plot_histogram(histogram):
    plt.figure(figsize=(6, 4))
    plt.title("Görüntü Histogramı")
    plt.xlabel("Piksel Değeri (0–255)")
    plt.ylabel("Frekans")
    plt.bar(range(256), histogram, color='gray')
    plt.tight_layout()
    plt.show()

def histogram_equalization(image_array):
    hist = calculate_histogram(image_array)
    cdf = np.cumsum(hist)

    if cdf.max() == cdf.min():
        return image_array.copy()

    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    cdf_normalized = cdf_normalized.astype(np.uint8)
    equalized = cdf_normalized[image_array]
    return equalized

def contrast_stretching(image_array):
    p1, p99 = np.percentile(image_array, (1, 99))

    if p1 == p99:
        return image_array.copy()

    stretched = (image_array - p1) * 255 / (p99 - p1)
    return np.clip(stretched, 0, 255).astype(np.uint8)



