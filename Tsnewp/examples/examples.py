from Tsnewp import Tsnewp
import numpy as np

data = np.random.random((1000,100))
tsne = Tsnewp()
new_data = tsne.transform(data)

