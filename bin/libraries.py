import numpy as np


def load_MNIST_images(filename):
  """
  returns a 28x28x[number of MNIST images] matrix containing
  the raw MNIST images
  :param filename: input data file
  """
  with open(filename, "r") as f:
    magic = np.fromfile(f, dtype=np.dtype('>i4'), count=1)

    num_images = int(np.fromfile(f, dtype=np.dtype('>i4'), count=1))
    num_rows = int(np.fromfile(f, dtype=np.dtype('>i4'), count=1))
    num_cols = int(np.fromfile(f, dtype=np.dtype('>i4'), count=1))

    images = np.fromfile(f, dtype=np.ubyte)
    images = images.reshape((num_images, num_rows * num_cols)).transpose()
    images = images.astype(np.float64) / 255

    f.close()

    return images 



def open_binary(filename, FileType=np.int8):
	f = open(filename, 'r')
	magic = np.fromfile(f, dtype=FileType)
	return magic
