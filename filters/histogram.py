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
