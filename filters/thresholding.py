import numpy as np

def manual_threshold(image_array, threshold):
    binary = np.where(image_array > threshold, 255, 0)
    return binary.astype(np.uint8)

def otsu_threshold(image_array):
    histogram, _ = np.histogram(image_array, bins=256, range=(0, 256))
    total = image_array.size

    current_max, threshold = 0, 0
    sum_total, sum_foreground = 0, 0
    weight_background, weight_foreground = 0, 0

    for i in range(256):
        sum_total += i * histogram[i]

    for t in range(256):
        weight_background += histogram[t]
        if weight_background == 0:
            continue

        weight_foreground = total - weight_background
        if weight_foreground == 0:
            break

        sum_foreground += t * histogram[t]

        mean_b = sum_foreground / weight_background
        mean_f = (sum_total - sum_foreground) / weight_foreground

        between_var = weight_background * weight_foreground * (mean_b - mean_f) ** 2

        if between_var > current_max:
            current_max = between_var
            threshold = t

    return np.where(image_array > threshold, 255, 0).astype(np.uint8)

def kapur_threshold(image_array):
    hist, _ = np.histogram(image_array, bins=256, range=(0, 256))
    hist = hist.astype(np.float64)
    hist = hist / hist.sum()  # normalize et

    max_entropy = -np.inf
    threshold = 0

    for t in range(1, 255):
        p1 = hist[:t]
        p2 = hist[t:]

        w1 = p1.sum()
        w2 = p2.sum()

        if w1 == 0 or w2 == 0:
            continue

        H1 = -np.sum(p1 / w1 * np.log(p1 / w1 + 1e-12)) # 0'a bölmeyi engelle
        H2 = -np.sum(p2 / w2 * np.log(p2 / w2 + 1e-12))

        total_entropy = H1 + H2

        if total_entropy > max_entropy:
            max_entropy = total_entropy
            threshold = t

    return np.where(image_array > threshold, 255, 0).astype(np.uint8)
