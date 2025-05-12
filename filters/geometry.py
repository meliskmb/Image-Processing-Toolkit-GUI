import numpy as np
from skimage.morphology import skeletonize as ski_skeletonize

def compute_centroid(binary_image):
    indices = np.argwhere(binary_image == 255)

    if len(indices) == 0:
        return None

    centroid = indices.mean(axis=0)
    return int(centroid[1]), int(centroid[0])  # (x, y)

def skeletonize(binary_image):
    binary = (binary_image == 255).astype(np.uint8)
    skeleton = ski_skeletonize(binary)
    return (skeleton * 255).astype(np.uint8)