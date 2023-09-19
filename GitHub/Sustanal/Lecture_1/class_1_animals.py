import pandas as pd

#%% data input
shelter_count = pd.read_csv('shelter_count.csv', skiprows = 4,
                             header = [0,1], index_col = [0,1])
print(shelter_count.describe())

#%% data exploration
shelter_count.columns
shelter_count.index
shelter_count.shape
shelter_count.dtypes
shelter_count.head()
pd.set_option('display.max_columns', None)
shelter_count.head()

pd.notna(shelter_count).all().all()

#%% summary statistics
shelter_count.drop(index = 'Total', columns = ['Total', 'Grand Total'],
                    level = 1, inplace = True)

shelter_count.groupby(level = 0).sum()
shelter_count.groupby(axis = 1, level = 0).sum()
shelter_count.sum(axis = 1)

#%% subsetting and sorting
shelter_count.sum(axis = 1).loc['Gross Live Outcomes']
shelter_count.sum(axis = 1).loc['Gross Live Outcomes'].sort_values()
shelter_count.sum(axis = 1).loc['Gross Live Outcomes'].\
sort_values(ascending = False)

#%% data manipulation
shelter_count.sum(axis = 1).to_list()

net_intake = shelter_count.loc['Gross Intakes'].sum() - \
shelter_count.loc[('Gross Intakes', 'Transferred in from Agency')]
net_live_outcomes = shelter_count.loc['Gross Live Outcomes'].sum() - \
shelter_count.loc[('Gross Live Outcomes', 'Transferred to another Agency')]
net_intake.groupby(level = 0).sum()
net_live_outcomes.groupby(level = 0).sum()

# option 1
net_count = net_intake.to_frame('Net Intakes').merge(\
                               net_live_outcomes.to_frame('Net Live Outcomes'),
                               left_index = True, right_index = True)

# option 2
net_count = pd.concat([net_intake.to_frame('Net Intakes'),
                       net_live_outcomes.to_frame('Net Live Outcomes'),], axis = 1)

# option 1 (rows not aligned)
net_count = net_intake.to_frame('Net Intakes').merge(\
                               net_live_outcomes.sort_values().to_frame('Net Live Outcomes'),
                               left_index = True, right_index = True)

# option 2 (rows not aligned)
net_count = pd.concat([net_intake.to_frame('Net Intakes'),
                       net_live_outcomes.sort_values().to_frame('Net Live Outcomes'),], axis = 1)


#%% data output
net_count.to_csv('shelter_net_count.csv')
