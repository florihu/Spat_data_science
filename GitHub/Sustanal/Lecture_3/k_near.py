import random

import numpy as np
from sklearn.model_selection import KFold

X = np.array([[random.random(), random.random()] for i in range(100)])

kf = KFold(n_splits=10)


for i, (train_index, test_index) in enumerate(kf.split(X)):
    print(f"Fold {i}:")
    print(f"  Train: index={train_index}")
    print(f"  Test:  index={test_index}")


print(X)