import binascii

import numpy as np
import scipy
import scipy.cluster
import scipy.misc
from PIL import Image
from numpy import random


def search_most_common_color(image: Image.Image) -> str:
    """
    Ищет самый частый цвет в картинке

    Ставит сид, чтобы одинаковые результаты были
    Вырезает серединку, чтобы игнорить фон и бошку
    Затем по алгоритму:
    https://stackoverflow.com/a/3244061
    """
    random.seed((1000, 2000))

    cropped = image.crop((
        image.width / 3,
        image.height / 3,
        image.width * 2 / 3,
        image.height * 2 / 3
    ))

    ar = np.asarray(cropped)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
    codes, dist = scipy.cluster.vq.kmeans(ar, 5, )
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    return color