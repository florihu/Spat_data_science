

import numpy as np
import scipy.stats
from scipy.stats import norm, rv_histogram
import seaborn as sns
import matplotlib.pyplot as plt

data = np.array([
0.041610738,
0.027074236,
0.018507463,
0.018343195,
0.017699115

])

x = np.linspace(min(data), max(data),100)

hist = np.histogram(data)

y = rv_histogram(hist,density=False)


mu, std = norm.fit(data)
mu, std = norm.fit(data)


sns.histplot(data,kde=True)
plt.show()

