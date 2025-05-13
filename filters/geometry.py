import numpy as np
from skimage.morphology import skeletonize as ski_skeletonize
from PIL import Image
from scipy.ndimage import affine_transform

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

def rotate_image(pil_image, angle_deg=90):
    img_array = np.array(pil_image)

    if len(img_array.shape) == 2:
        rotated = rotate_image_array(img_array, angle_deg)
        return Image.fromarray(rotated.astype(np.uint8))

    channels = []
    for i in range(3):
        rotated_channel = rotate_image_array(img_array[:, :, i], angle_deg)
        channels.append(rotated_channel.astype(np.uint8))

    rotated_rgb = np.stack(channels, axis=2)
    return Image.fromarray(rotated_rgb)


def rotate_image_array(image_array, angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)

    transform_matrix = np.array([
        [cos_a, -sin_a],
        [sin_a,  cos_a]
    ])

    h, w = image_array.shape

    new_w = int(abs(h * sin_a) + abs(w * cos_a))
    new_h = int(abs(h * cos_a) + abs(w * sin_a))
    output_shape = (new_h, new_w)

    old_center = np.array([h / 2, w / 2])
    new_center = np.array([new_h / 2, new_w / 2])
    offset = old_center - transform_matrix @ new_center

    rotated = affine_transform(
        image_array,
        transform_matrix,
        offset=offset,
        output_shape=output_shape,
        order=1,
        mode='constant',
        cval=255 
    )

    return rotated


def shear_image(pil_image, shear_x=0.2, shear_y=0.0):
    width, height = pil_image.size

    matrix = (
        1, shear_x, 0,
        shear_y, 1, 0
    )

    return pil_image.transform(
        (int(width * 1.5), int(height * 1.5)),  # Kırpma olmasın diye
        Image.AFFINE,
        matrix,
        resample=Image.BICUBIC
    )

def flip_horizontal(pil_image):
    arr = np.array(pil_image)
    flipped = arr[:, ::-1]
    return Image.fromarray(flipped)

def flip_vertical(pil_image):
    arr = np.array(pil_image)
    flipped = arr[::-1, :]
    return Image.fromarray(flipped)
