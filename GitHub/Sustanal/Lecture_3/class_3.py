"""
Student pair
(add names below)
- 
- 
"""

# Mobility carbon footprint calculator


import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def distribution(kind,loc,scale,size):
    if kind == 'normal':
        return  np.random.normal(loc=loc, scale=scale, size=size)
    elif kind == 'log_normal':
        return  np.random.lognormal(mean=loc, sigma=scale, size=size)
import numpy as np

def calculate(d_car, d_train, d_air, switch='deterministic'):

    if switch == 'deterministic':
        emission_car = np.full(1000, 10 * d_car)
        emission_train = np.full(1000, 2.5 * d_train)
        emission_airplain = np.full(1000, 200 * d_air)
        data = pd.DataFrame({'Emission_car': emission_car, 'Emission_train': emission_train, 'Emission_airplain': emission_airplain})

        return data / 1000

    elif switch == 'random':
        emission_car_normal = distribution(kind='normal', loc=55/2, scale=45 / 4, size=1000) * d_car
        emission_train_normal = distribution(kind='normal', loc=11/ 2, scale=9 / 4, size=1000) * d_train
        emission_airplain_normal = distribution(kind='normal', loc=(355+199) / 2, scale=(355-199) / 4, size=1000) * d_air
        emission_car_lognormal = distribution(kind='lognormal', loc=55/2, scale=45 / 4, size=1000) * d_car
        emission_train_lognormal = distribution(kind='lognormal', loc=11/ 2, scale=9 / 4, size=1000) * d_train
        emission_airplain_lognormal = distribution(kind='lognormal', loc=(355+199) / 2, scale=(355-199) / 4, size=1000) * d_air
        data = pd.DataFrame({'Emission_car_normal': emission_car_normal, 'Emission_train_normal': emission_train_normal, 'Emission_airplain_normal': emission_airplain_normal, 'Emission_car_lognormal': emission_car_lognormal, 'Emission_train_lognormal': emission_train_lognormal, 'Emission_airplain_lognormal': emission_airplain_lognormal})

        return data / 1000
    else:

        raise ValueError('daterministic or random')



if __name__ == "__main__":

    d_car = 200
    d_train = 10000
    d_airplane = 1000

    plt.figure()
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_car', 'normal')], kde=True,
                 log_scale=False)
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_train', 'normal')], kde=True,
                 log_scale=False)
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_airplain', 'normal')], kde=True,
                 log_scale=False)
    plt.savefig('Comparison_normal_distrib.png')
    plt.show()

    plt.figure()
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_car', 'log_normal')], kde=True,
                 log_scale=True)
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_train', 'log_normal')], kde=True,
                 log_scale=True)
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_airplain', 'log_normal')], kde=True,
                 log_scale=True)
    plt.show()



