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
def calculate(d_car, d_train, d_air, switch='deterministic'):

   if switch == 'deterministic':
       data = pd.DataFrame()
       data['Emission_car'] = 10 * d_car
       data['Emission_train'] = 2.5 * d_train
       data['Emission_airplain'] = 200 * d_air

       return data /1000

   elif switch == 'random':
        data = pd.DataFrame()
        for type in ['normal', 'log_normal']:
            data[('Emission_car', type)] = distribution(kind=type, loc=55/2, scale=45 / 4, size=1000) * d_car
            data[('Emission_train', type)] = distribution(kind =type, loc=11/ 2, scale=9 / 4, size=1000) * d_train
            data[('Emission_airplain', type)] = distribution(kind=type, loc=(355+199) / 2, scale=(355-199) / 4, size=1000) * d_air

        return data /1000


   else:
        raise ValueError('daterministic or random')


if __name__ == "__main__":
    d_car = 200
    d_train = 10000
    d_airplane = 1000

    plt.figure()
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_car', 'normal')], kde=True, log_scale=False)
    sns.histplot(calculate(d_car, d_train, d_airplane, switch='random')[('Emission_train', 'normal')], kde=True, log_scale=False)
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

