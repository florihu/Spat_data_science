#%% libraries and settings

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import product

# target yearly oil extraction

def logistic_function(K, r, x_peak, x):
    '''

    :param K: This is the value f(x->inf)=K
    :param r: this is the growth rate
    :param x_peak: this is the peak
    :param x: time vector
    :return: is an output vector of time dependent values
    '''
    return K / ( 1+ np.exp(r*(x_peak-x)))

def plotting_stuff(data):
    '''

    :param data:
    :return:
    '''
    return sns.lineplot(data)

def gener_par_tup(r_list, t_max_list, q_max_list):
    '''

    :param r_list: list of r values
    :param t_max_list: list of t_max values
    :param q_max_list: list of q_max values
    :return: a list of tupples.
    '''

    list_par_comb = list(product(r_list, t_max_list, q_max_list))

    return list_par_comb

def generate_data_frame(t_series, r, t_max, q_max):
    hubbert_eval = pd.DataFrame()

    hubbert_eval.index = t_series

    for combo in gener_par_tup(r, t_max, q_max):
        hubbert_eval[f"{combo}"] = logistic_function(K = combo[2], r = combo[0], x_peak = combo[1], x = t_series)

    return hubbert_eval



if __name__ == '__main__':
    r = np.arange(.5, .7, 10)
    t_max = np.array(range(30, 80, 10))
    q_max = np.array(range(150, 250, 10))
    t_series = np.array(range(141))

    data = generate_data_frame(t_series, r, t_max, q_max)

    plotting_stuff(data)
    plt.show()






