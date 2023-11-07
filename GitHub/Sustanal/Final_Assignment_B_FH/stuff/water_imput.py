import wbgapi as wb
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
import numpy as np
import matplotlib.pyplot as plt
from .util import *


data = wb.data.DataFrame(['ER.H2O.FWIN.ZS','NV.IND.TOTL.ZS'], time=[2020])


class Process_data():
    def __init__(self):
        self.data = data
        self.thres1 = None
        self.thres2 = None


    def imput_calc(self):

        data = region_cleaner(self.data)

        y = data['ER.H2O.FWIN.ZS']
        X = data['NV.IND.TOTL.ZS']

        imputer = SimpleImputer(strategy='mean')

        data['H20_imputed_simple'] = imputer.fit_transform(y.values.reshape(-1, 1))

        knn_imputer_uniform = KNNImputer(n_neighbors=10, weights='uniform')

        data['H20_imp_k_uni'] = knn_imputer_uniform.fit_transform(
            np.column_stack((X, y)))[:, 1]

        knn_imputer_dist = KNNImputer(n_neighbors=10, weights='distance')

        data['H20_imp_k_dist'] = knn_imputer_dist.fit_transform(
            np.column_stack((X, y)))[:, 1]

        return data

    def plot_output(self, value1, value2):
        result_df = self.clustering(value1,value2)  # Fixed method call
        result_df_percentage = result_df.div(result_df.sum(axis=0), axis=1) * 100
        return result_df_percentage.T.plot(kind='bar', stacked=True)
        #plt.ylabel('Percentage (%)' + f" {self.thres1, self.thres2}")  # Fixed syntax
        #plt.savefig('Graphs\porportion_classes_UI.jpeg')
        #plt.show()

    def clustering(self, value1, value2):

        self.thres1 = value1
        self.thres2 = value2
        data = self.imput_calc()

        # cat 1: < median -> high sust
        # threshold 2: median =< VALUE =< average -> medium sust
        # threshold 3: value >average -> high sust
        #
        ser = data['ER.H2O.FWIN.ZS']
        ser = ser[~ser.isna()]

        thres1 = np.percentile(ser, self.thres1)
        thres2 = np.percentile(ser, self.thres2)

        #print('Threshold1:'+f"{self.thres1}"+' Threshold2:'+f"{self.thres2}")

        dict_ = {key for key in data.columns}

        dict_bar = {}

        for column in data.columns:
            dict_bar[column] = []
            mask_high = data[column] < thres1
            mask_medium = (data[column] >= thres1) & (data[column] <= thres2)
            mask_low = data[column] > thres2
            dict_bar[column].append(data[column][mask_high].describe()['count'])
            dict_bar[column].append(data[column][mask_medium].describe()['count'])
            dict_bar[column].append(data[column][mask_low].describe()['count'])

        df = pd.DataFrame.from_dict(dict_bar)
        df.index = ['high', 'medium', 'low']

        #result_df_percentage = df.div(df.sum(axis=0), axis=1) * 100

        #result_df_percentage.T.plot(kind='bar', stacked=True)
        #plt.ylabel('Percentage (%)' + f" {self.thres1, self.thres2}")  # Fixed syntax
        #folder_checker('Graphs')
        #plt.savefig('Graphs\porportion_classes_UI.jpeg')
        #plt.show()

        return df


iteration = Process_data()



