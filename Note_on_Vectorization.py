import numpy as np
import time

# initialize two vectors
sizeofvec = 1000000
a = np.random.rand(sizeofvec)
b = np.random.rand(sizeofvec)
print("array properties of a and b:\n\tdimensions = {},\n\tshape = {},\n\tsize = {}".format(a.ndim, a.shape, a.size))

tic = time.time()
# c = a.dot(b) is the same syntax
c = np.dot(a,b)
toc = time.time()
print("Vectorized product = {}, in {} ms".format(c, 1000 * (toc - tic)))

c = 0
tic = time.time()
for i in range(sizeofvec):
    c += a[i] * b[i]
toc = time.time()
print("For loop product = {}, in {} ms".format(c, 1000 * (toc - tic)))

