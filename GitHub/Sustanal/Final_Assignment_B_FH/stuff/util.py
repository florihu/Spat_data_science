import wbgapi as wb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
import numpy as np
import os

wb_economies = wb.economy.DataFrame()


def region_cleaner(data, economies=wb_economies):
    '''

    :param data: This is the data consumed by the wb. Assumed are two indicators
    :param economies: Economics of wb.economies
    :return: DataFrame with mutliindex and removed regions.
    '''

    # Filter out non-country aggregates
    data_clean = data[data.index.isin(economies[economies['aggregate'] == False].index)]

    # Join with economy names and set a multi-index
    data_clean_name = data_clean.join(economies[['name']], on=data_clean.index, how='inner')
    data_clean_name.set_index(['name', data_clean_name.index], inplace=True)

    # Drop the unnecessary key_0 column
    data_clean_name.drop(columns='key_0', inplace=True)

    return data_clean_name



def nan_checker(data):
    '''

    :param data: wb data
    :return: Prints the sum of the NaN values per indicator
    '''
    data = region_cleaner(data)
    print('TASK 4c NaN values per indicator\n', data.isna().sum(), '\n')

def imput_countries(data):
    '''

    :param data: wb data
    :return: Prints the countries where primary indicator is NaN and secondary is NOT NaN
    '''
    data = region_cleaner(data)
    prim, sec = data.columns
    data_new = data[~data[sec].isna() & data[prim].isna()]
    print('TASK 4d: Countries where primary NaN and secondary not NaN\n',
          data_new.index.values, '\n')


def set_split(data):
    '''

    * the return of this function is a DataFrame with only non NAN values for both indicators

    :param data: wb data
    :return: Dataframe with countries where both indicators are not NaN
    '''

    data = region_cleaner(data)
    prim, sec = data.columns
    data_new = data[~data[sec].isna() & ~data[prim].isna()]
    #data_new=  data[~data['NV.IND.TOTL.ZS'].isna() & data['ER.H2O.FWIN.ZS'].isna()]

    return data_new


def plot_stuff(data):
    '''
    Generates some plots to investigate the data further
    :param data
    :return: plots
    '''
    data = set_split(data)
    prim, sec = data.columns
    industry_share = data[sec]
    water_share = data[prim]

    if not os.path.exists('Graphs'):
        os.makedirs('Graphs')

    #sns.scatterplot(x =industry_share, y = water_share)
    #plt.savefig('Graphs\Scatter_init.png')
    #plt.close()
    #sns.histplot(industry_share, kde=True)
    #plt.savefig('Graphs\Indust_distrib.png')
    #plt.close()
    sns.histplot(water_share, kde=True)
    plt.savefig('Graphs\hist_plot.png', dpi=150)
    plt.show()
    plt.close()


def imput_calc(data):
    '''
    Imputes the missing values with three different kind
    1. simple imputation
    2. k uniform  imputation
    3. k distance imputation

    :param data: wb data
    :return: DataFrame with imputet values
    '''

    data = region_cleaner(data)
    prim, sec = data.columns


    y = data[prim]
    X =  data[sec]

    imputer = SimpleImputer(strategy='mean')

    data[f"{prim}"+'_imputed_simple'] = imputer.fit_transform(y.values.reshape(-1, 1))

    knn_imputer_uniform = KNNImputer(n_neighbors=10, weights='uniform')

    data[f"{prim}"+'_imp_k_uni'] = knn_imputer_uniform.fit_transform(
    np.column_stack((X, y)))[:,1]

    knn_imputer_dist = KNNImputer(n_neighbors=10, weights='distance')

    data[f"{prim}"+'_imp_k_dist'] = knn_imputer_dist.fit_transform(
    np.column_stack((X, y)))[:,1]


    return data

def imp_valid(data, n_folds=5, print_output = False):
    '''
    Default 5-fold cross validation.
    For a given dataset three different kinds of imputations are compared
    1. simple
    2. k uniform
    3. k distance

    :param data: this is again the raw data
    :param n_folds: number of folds. The number of times the dataset is splited and testing is executed.
    :return: DataFrame with the scores for the alternatives. Evaluated scores =[R2, NMRSE, PBIAS]
    '''

    scores ={'aver':{'R2':[], 'NMRSE':[], 'PBIAS':[] },'k_uni':{'R2':[], 'NMRSE':[], 'PBIAS':[] },'k_dist':{'R2':[], 'NMRSE':[], 'PBIAS':[] }}

    data = set_split(data)
    prim, sec = data.columns

    # Perform imputations and model evaluation over multiple runs

    # Initialize a k-fold cross-validation splitter
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    data_copy = data.copy()
    y = np.array(data[prim])
    X = np.array(data[sec])

    for imp_switch in ['aver', 'k_uni', 'k_dist']:

        for train_index, test_index in kf.split(data):

            # Set NaN values in the 'ER.H2O.FWIN.ZS' column for the test index
            y_test = y.copy()
            y_test[test_index] = np.NaN

            if imp_switch == 'aver':
                imputer = SimpleImputer(strategy='mean')
                y_imp = imputer.fit_transform(y_test.reshape(-1, 1))

            elif imp_switch == 'k_uni':

                knn_imputer_uniform = KNNImputer(n_neighbors=10, weights='uniform')
                y_imp = knn_imputer_uniform.fit_transform(np.column_stack((X, y_test)))[:,1]

            elif imp_switch == 'k_dist':

                knn_imputer_dist = KNNImputer(n_neighbors=10, weights='distance')

                y_imp = knn_imputer_dist.fit_transform(np.column_stack((X, y_test)))[:,1]


            scores[imp_switch]['R2'].append(r2_score(y[test_index], y_imp[test_index]))
            scores[imp_switch]['NMRSE'].append(np.sqrt(mean_squared_error(y[test_index],
                                                                          y_imp[test_index]))/np.mean(y[test_index]))
            scores[imp_switch]['PBIAS'].append(((y_imp[test_index]-y[test_index]).sum()
                                                    /y[test_index].sum()))

        scores[imp_switch]['R2'] = np.mean(np.array(scores[imp_switch]['R2']))
        scores[imp_switch]['NMRSE'] = np.mean(np.array(scores[imp_switch]['NMRSE']))
        scores[imp_switch]['PBIAS'] = np.mean(np.array(scores[imp_switch]['PBIAS']))

    if print_output:
        print('TASK 5e: Mean of 5 fold cross validation scores\n', pd.DataFrame.from_dict(scores), '\n')

    return pd.DataFrame.from_dict(scores)


def clustering(data, fig_output = False):

    '''

    :param data: wb data
    :param fig_output: Should Graph be printed?
    :return: Clustering of distribution in sutainability categories low, medium, high.
    '''
    data = imput_calc(data)
    prim, sec = data.columns[:2]
    data.pop(sec)


    #cat 1: < median -> high sust
    #threshold 2: median =< VALUE =< average -> medium sust
    #threshold 3: value >average -> high sust
    #
    ser = data[prim]
    ser = ser[~ser.isna()]

    thres1 = np.percentile(ser, 25)
    thres2 = np.percentile(ser, 50)

    dict_ = {key for key in data.columns}

    dict_bar = {}
    for column in data.columns:
        dict_bar[column] = []
        mask_high = data[column] < thres1
        mask_medium =   (data[column] >= thres1) & (data[column] <= thres2)
        mask_low = data[column] > thres2
        dict_bar[column].append(data[column][mask_high].describe()['count'])
        dict_bar[column].append(data[column][mask_medium].describe()['count'])
        dict_bar[column].append(data[column][mask_low].describe()['count'])

        df = pd.DataFrame.from_dict(dict_bar)
        df.index = ['high', 'medium', 'low']


    if fig_output:

        df_percentage = df.div(df.sum(axis=0), axis=1) * 100

        color_palette = sns.color_palette("husl")
        plt.figure(figsize=(20, 10))
        # plt.subplots_adjust(left= .5)  # Adjust the left margin as needed
        df_percentage.T.plot(kind='barh', stacked=True, color=color_palette)
        plt.ylabel('Percentage (%)')
        folder_checker('Graphs')
        plt.savefig('Graphs\stacked_bars.png', dpi= 150)
        plt.show()

    return df


def folder_checker(Folder):
    '''

    :param Folder: Folder name
    :return: If folder does not exist a folder is initiated.
    '''
    if not os.path.exists(Folder):
        os.makedirs(Folder)

