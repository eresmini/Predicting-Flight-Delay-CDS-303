#%%

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

#%%

df_concat = pd.concat(map(pd.read_csv, ['2014.csv', '2015.csv', '2016.csv',
                                        '2017.csv', '2018.csv']))

df = df_concat[pd.notnull(df_concat['OP_CARRIER'])]
df = df.drop(['Unnamed: 27'], axis=1)

#%%

# shows the amount and percentage of missing values - labelled 'missing_df1'
# we will have a few of these checks!

missing_df1 = df.isnull().sum(axis=0).reset_index()
missing_df1.columns = ['variable', 'missing values']
missing_df1['filling factor (%)']=(df.shape[0]-missing_df1['missing values'])/df.shape[0]*100
missing_df1.sort_values('filling factor (%)').reset_index(drop = True)

#%%

# SIMPLE IMPUTER - scikit learn https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html

# IMPUTATION PART 1
# For the delay type columns, replace NaN values with zero
# will make a separate numpy array with new values - 'delay_filled'
X1 = df[['CARRIER_DELAY','WEATHER_DELAY','NAS_DELAY','SECURITY_DELAY','LATE_AIRCRAFT_DELAY']]
imp_mean = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=None)
imp_mean.fit(X1)
delay_filled = imp_mean.transform(X1)

#%%

# IMPUTATION PART 2
# For the columns below, replace NaN values with mean imputed value
# will make a separate numpy array with new values - 'time_stats_filled'
X2 = df[['DEP_TIME','DEP_DELAY','TAXI_OUT','WHEELS_OFF','WHEELS_ON','TAXI_IN','AIR_TIME','ARR_DELAY']]
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
imp_mean.fit(X2)
time_stats_filled = imp_mean.transform(X2)

#%%

### REPLACE columns in main dataframe with the imputed arrays

values = delay_filled[:,0]
df['CARRIER_DELAY'] = values

values = delay_filled[:,1]
df['WEATHER_DELAY'] = values

values = delay_filled[:,2]
df['NAS_DELAY'] = values

values = delay_filled[:,3]
df['SECURITY_DELAY'] = values

values = delay_filled[:,4]
df['LATE_AIRCRAFT_DELAY'] = values

#-------------

values = time_stats_filled[:,0]
df['DEP_DELAY'] = values

values = time_stats_filled[:,1]
df['TAXI_OUT'] = values

values = time_stats_filled[:,2]
df['WHEELS_OFF'] = values

values = time_stats_filled[:,3]
df['WHEELS_ON'] = values

values = time_stats_filled[:,4]
df['TAXI_IN'] = values

values = time_stats_filled[:,5]
df['AIR_TIME'] = values

values = time_stats_filled[:,6]
df['ARR_DELAY'] = values

#%%

# shows the amount and percentage of missing values after imputation and replacement
# labelled 'missing_df2'

missing_df2 = df.isnull().sum(axis=0).reset_index()
missing_df2.columns = ['variable', 'missing values']
missing_df2['filling factor (%)']=(df.shape[0]-missing_df2['missing values'])/df.shape[0]*100
missing_df2.sort_values('filling factor (%)').reset_index(drop = True)

#%%
### DROPPING ROWS

# Remove entries (rows) for flights with delays caused by NAS or security
### REMOVE WEATHER LATER
columns = ['NAS_DELAY', 'SECURITY_DELAY']
for i in columns:
    indexNames = df[df[i] > 0].index
    df.drop(indexNames, inplace=True)

# Remove entries for cancelled flights
indexNames = df[df['CANCELLATION_CODE'].notnull()].index
df.drop(indexNames, inplace=True)

# Remove entries for null departure time and arrival time
df.dropna(subset=['DEP_TIME', 'ARR_TIME'])

# Remove entries for diverted flights
indexNames = df[df['DIVERTED'] == 1].index
df.drop(indexNames, inplace=True)

#%%
# shows the amount and percentage of missing values after imputation and replacement
# labelled 'missing_df3'

missing_df3 = df.isnull().sum(axis=0).reset_index()
missing_df3.columns = ['variable', 'missing values']
missing_df3['filling factor (%)']=(df.shape[0]-missing_df3['missing values'])/df.shape[0]*100
missing_df3.sort_values('filling factor (%)').reset_index(drop = True)


#%%

###### IATA CODE

# XE - ExpressJet Airlines
# YV - Mesa Airlines
# NW - Northwest Airlines
# OH - PSA Airlines
# OO - SkyWest Airlines
# UA - United Airlines
# US - US Airways
# WN - Southwest Airlines
# EV - Atlantic Southeast Airlines
# F9 - Frontier Airlines
# FL - AirTran Airways
# HA - Hawaiian Airlines
# MQ - Envoy Air
# 9E - Endeavor Air
# AA - American Airlines
# AS - Alaska Airlines
# B6 - JetBlue Airways
# CO - Continental Airlines
# DL - Delta Air Lines
# VX - Virgin America
# NK - Spirit Airlines
# G4 - Allegiant Air
# YX - Republic Airways

######

decoded = df.replace({'OP_CARRIER' : {'XE' : 'ExpressJet Airlines',
                                      'YV' : 'Mesa Airlines',
                                      'NW' : 'Northwest Airlines',
                                      'OH' : 'PSA Airlines',
                                      'OO' : 'SkyWest Airlines',
                                      'UA' : 'United Airlines',
                                      'US' : 'US Airways',
                                      'WN' : 'Southwest Airlines',
                                      'EV' : 'Atlantic Southeast Airlines',
                                      'F9' : 'Frontier Airlines',
                                      'FL' : 'AirTran Airways',
                                      'HA' : 'Hawaiian Airlines',
                                      'MQ' : 'Envoy Air',
                                      '9E' : 'Endeavor Air',
                                      'AA' : 'American Airlines',
                                      'AS' : 'Alaska Airlines',
                                      'B6' : 'JetBlue Airways',
                                      'CO' : 'Continental Airlines',
                                      'DL' : 'Delta Air Lines',
                                      'VX' : 'Virgin America',
                                      'NK' : 'Spirit Airlines',
                                      'G4' : 'Allegiant Air',
                                      'YX' : 'Republic Airways'}})

decoded = decoded['OP_CARRIER']
df['CARRIER_NAME'] = decoded

#%%

#### AIRLINES TO REMOVE:
# Atlantic Southeast Airlines - Merged into ExpressJet in 2011
# Airtran Airways - merged into Southwest in 2014
# Continental Airlines - merged into United Airlines in 2012
# ExpressJet - currently defunct (trying to come back)
# Northwest Airlines - acquired by Delta in 2008(?)
# US Airways - merged with American Airlines in 2013
# Virgin America - acquired by Alaska Airlines in 2018

flights_to_remove = ['Atlantic Southeast Airlines',
                     'AirTran Airways'
                     'Continental Airways',
                     'ExpressJet Airlines',
                     'Northwest Airlines'
                     'US Airways',
                     'Virgin America']

for carrier in flights_to_remove:
    indexNames = df[df['CARRIER_NAME'] == carrier].index
    df.drop(indexNames, inplace=True)

#%%
variables_to_remove = ['TAXI_OUT', 'TAXI_IN', 'WHEELS_ON', 'WHEELS_OFF', 'NAS_DELAY',
                       'SECURITY_DELAY', 'WEATHER_DELAY', 'DIVERTED', 'CANCELLED',
                       'CANCELLATION_CODE', 'OP_CARRIER_FL_NUM', 'DISTANCE']

df.drop(variables_to_remove, axis = 1, inplace = True)

df.rename(columns={"FL_DATE" : "DATE",
                   "OP_CARRIER": "IATA_CODE",
                   "CRS_DEP_TIME" : "SCHEDULED_DEP",
                   "CRS_ARR_TIME" : "SCHEDULED_ARR",
                   "CRS_ELAPSED_TIME" : "SCHEDULED_ELAPSED_TIME"},
          errors="raise")

#%%
# split date (currently in YYYY-MM-DD format) into separate Year, Month, and Day columns
df[['Year','Month','Day']] = df.FL_DATE.str.split("-",expand=True,)

#%%

# last check of amount and percentage of missing values - should be all 0/100%
# labelled 'missing_df3'

missing_df4 = df.isnull().sum(axis=0).reset_index()
missing_df4.columns = ['variable', 'missing values']
missing_df4['filling factor (%)']=(df.shape[0]-missing_df4['missing values'])/df.shape[0]*100
missing_df4.sort_values('filling factor (%)').reset_index(drop = True)


#%%
abbr_companies = {'XE' : 'ExpressJet Airlines',
                  'YV' : 'Mesa Airlines',
                  'NW' : 'Northwest Airlines',
                  'OH' : 'PSA Airlines',
                  'OO' : 'SkyWest Airlines',
                  'UA' : 'United Airlines',
                  'US' : 'US Airways',
                  'WN' : 'Southwest Airlines',
                  'EV' : 'Atlantic Southeast Airlines',
                  'F9' : 'Frontier Airlines',
                  'FL' : 'AirTran Airways',
                  'HA' : 'Hawaiian Airlines',
                  'MQ' : 'Envoy Air',
                  '9E' : 'Endeavor Air',
                  'AA' : 'American Airlines',
                  'AS' : 'Alaska Airlines',
                  'B6' : 'JetBlue Airways',
                  'CO' : 'Continental Airlines',
                  'DL' : 'Delta Air Lines',
                  'VX' : 'Virgin America',
                  'NK' : 'Spirit Airlines',
                  'G4' : 'Allegiant Air',
                  'YX' : 'Republic Airways'}

#%%
"""
Summary Statistics
"""
def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}

## DELAY STATS
global_stats = df['DEP_DELAY'].groupby(df['CARRIER_NAME']).apply(get_stats).unstack()
global_stats = global_stats.sort_values('count')
global_stats

#%%
"""
Visualizations
"""

##### DEPARTURE DELAYS VS. ARRIVAL DELAYS (BAR CHART)

mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams['hatch.linewidth'] = 2.0  

fig = plt.figure(1, figsize=(11,6))
ax = sns.barplot(x="DEP_DELAY", y="CARRIER_NAME", data=df, color="lightskyblue", ci=None)
ax = sns.barplot(x="ARR_DELAY", y="CARRIER_NAME", data=df, color="r", hatch = '///',
                 alpha = 0.0, ci=None)
labels = list(abbr_companies.values())
ax.set_yticklabels(labels)
ax.yaxis.label.set_visible(False)
plt.xlabel('Mean delay [min] (@departure: blue, @arrival: hatch lines)',
           fontsize=14, weight = 'bold', labelpad=10);
plt.show()

#%%
##### DELAYS BAR CHART

# Function that define how delays are grouped
delay_type = lambda x:((0,1)[x > 15],2)[x > 45]
df['DELAY_LEVEL'] = df['DEP_DELAY'].apply(delay_type)


fig = plt.figure(1, figsize=(10,7))
ax = sns.countplot(y="CARRIER_NAME", hue='DELAY_LEVEL', data=df)

ax.set_yticklabels(labels)
plt.setp(ax.get_xticklabels(), fontsize=12, weight = 'normal', rotation = 0);
plt.setp(ax.get_yticklabels(), fontsize=12, weight = 'bold', rotation = 0);
ax.yaxis.label.set_visible(False)
plt.xlabel('Flight count', fontsize=16, weight = 'bold', labelpad=10)

# Set the legend
L = plt.legend()
L.get_texts()[0].set_text('on time (t < 15 min)')
L.get_texts()[1].set_text('small delay (15 < t < 45 min)')
L.get_texts()[2].set_text('large delay (t > 45 min)')
plt.show()

#%%
# striplot for delay lengths

df2 = df.loc[:, ['CARRIER_NAME', 'DEP_DELAY']]
df2['CARRIER_NAME'] = df2['CARRIER_NAME'].replace(abbr_companies)
fig = plt.figure(1, figsize=(16,15))

# 18 colors for 18 airlines !
colors = ['firebrick', 'gold', 'lightcoral', 'aquamarine', 'c', 'yellowgreen', 'grey',
          'seagreen', 'tomato', 'violet', 'wheat', 'chartreuse', 'lightskyblue', 'royalblue',
          'thistle', 'slategrey', 'darkorange', 'ghostwhite']
#___________________________________________________________________
ax3 = sns.stripplot(y="CARRIER_NAME", x="DEP_DELAY", size = 4, palette = colors,
                    data=df2, linewidth = 0.5,  jitter=True)
plt.setp(ax3.get_xticklabels(), fontsize=14)
plt.setp(ax3.get_yticklabels(), fontsize=14)
ax3.set_xticklabels(['{:2.0f}h{:2.0f}m'.format(*[int(y) for y in divmod(x,60)])
                         for x in ax3.get_xticks()])
plt.xlabel('Departure delay', fontsize=18, bbox={'facecolor':'midnightblue', 'pad':5},
           color='w', labelpad=20)
ax3.yaxis.label.set_visible(False)

plt.show()

#%%

# Heatmap showing departure delays at origin, using random sample from dataset

subset = df[['ORIGIN', 'CARRIER_NAME', 'DEP_DELAY']]
flights = subset.pivot_table('DEP_DELAY', index=["ORIGIN"], columns=["CARRIER_NAME"], aggfunc='mean')
flights_rand = flights.sample(n=100, axis=0)

fig = plt.figure(1, figsize=(8,8))
sns.set(context="paper")
fig.text(0.5, 1.02, "Delays: impact of the origin airport", ha='center', fontsize = 18)
mask = flights_rand.isnull()
sns.heatmap(flights_rand, linewidths=.01, cmap="Accent", mask=mask)
plt.setp(ax.get_xticklabels(), fontsize=10, rotation = 85);
ax.yaxis.label.set_visible(False)

plt.show()

#%%

### MODELING HERE WE GOOOOO
# Datacamp logistic regression: https://www.datacamp.com/community/tutorials/understanding-logistic-regression-python

## MODEL 1 - classification - on time or delayed
# By DoT definition, any flight is delayed if it departs more than 15 minutes past schedule

# make a subset of the data with carrier and arrival delay
# convert the arrival delay values to two values: on_time if <= 15, delay if >15

classification = df[['ARR_DELAY']]

classification['ARR_DELAY'] = classification['ARR_DELAY'].where(classification['ARR_DELAY'] > 15,other='on_time')
classification['ARR_DELAY'] = classification['ARR_DELAY'].where(classification['ARR_DELAY'] == 'on_time',other='delay')

df['classifier_1'] = classification

#%%

feature_cols = ['Day','Month','Year','CRS_ELAPSED_TIME','AIR_TIME', 'DEP_DELAY','ARR_DELAY']
df.dropna()
X = df[feature_cols]
y = df.classifier_1

#%%

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

#%%

# instantiate the model (using the default parameters)
logreg = LogisticRegression()

# fit the model with data
logreg.fit(X_train,y_train)

#
y_pred=logreg.predict(X_test)

#%%


cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

print(cnf_matrix)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))