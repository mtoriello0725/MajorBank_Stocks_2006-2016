# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 13:44:46 2018

@author: mtoriello0725
"""

"""

Python for Data Science Finance Project

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt     # plt.show() to display plot
import seaborn as sns
sns.set_style('darkgrid')

### Load Bank Data
bank_stocks = pd.read_pickle('all_banks')
tickers = 'BAC C GS JPM MS WFC'
tickers = tickers.split()
bank_stocks.columns.names = ['Bank Tickers', 'Stock Info']


### Find the Maximum Closing Price for Each Bank
bank_max_close = bank_stocks.xs('Close', axis=1, level='Stock Info').max()		# dataframe of closing values for each bank, max claculated using cross-section
print("The Maximum closing price for each bank is as folows: \n",bank_max_close, '\n\n')


### Create Returns Dataframe
Returns = pd.DataFrame()		# Create empty dataframe for Returns values
for tick in tickers:															# For each ticker values in the tickers string
	Returns[tick+' Returns'] = bank_stocks[tick]['Close'].pct_change()			# Fill Returns column with percentage changes from bank_stocks close
# print(Returns.head())


### Plot Returns in Seaborn as a Pairplot
pairPlotFig = sns.pairplot(Returns.drop(Returns.index[0]),\
	diag_kind='hist', plot_kws={"s": 8})											# Seaborn Plot to showcase Returns as a relationship to other returns.

pairPlotFig.fig.set_size_inches(15,8)									# Pairplot is meant to compare how each bank's daily returns compare to each other. 
plt.subplots_adjust(top=0.9, bottom=.1, left=.1, right=.9)				# Adjust the size of plot to add title
pairPlotFig.fig.suptitle('RETURNS')


### Print the date of the Maximum and Minimum Return for each bank, as well as standard deviation of returns in 2015
Returns = Returns.drop(Returns.index[0])		# drop the first index as it is N/A
print('Date of Maximum Return Value for each Bank\n', Returns.idxmax(),'\n\n Date of Minimum Return Value for each Bank \n',Returns.idxmin())
print('\n\nStandard Deviation for each Bank over 10 year Span\n',Returns.std(),'\n\nStandard Deviation for each bank in 2015 \n',Returns.loc[Returns.index >= '2015-01-01'].std())

'''
		4 of the banks experienced their worst drop on the same day. This is ignauration day 01-20-2009. 
		JPM recovered and had its best day after inaguration

		Looking at the standard deviations for each bank, Citi Group proves to be the riskiest over the 10 year span.
'''


### Plotting 2015 Returns for Morgan Stanely
fig_dist = plt.figure(figsize=(15,5))												# make new figure to customize fig size
ax_dist = fig_dist.add_axes([.1,.1,.8,.8])											# define axes of figure
distPlotFig = sns.distplot(\
	Returns.loc[Returns.index >= '2015-01-01']['MS Returns'],\
	color='green', bins=100)														# distribution plot for MS in 2015
ax_dist.set_title('Distribution Plot for Morgan Stanely 2015', fontsize=14)			# set custom title , xlabel, and ylabel
ax_dist.set_xlabel('Distance from Mean Return')												
ax_dist.set_ylabel('Frequency of Returns')													


### Plotting 2008 Returns for CitiGroup
fig_dist2 = plt.figure(figsize=(15,5))												# make new figure to customize fig size
ax_dist2 = fig_dist2.add_axes([.1,.1,.8,.8])										# define axes of figure
sns.distplot(Returns.loc[(Returns.index >= '2008-01-01') & \
	(Returns.index < '2009-01-01')]['C Returns'],\
	color='red', bins=100)															# distribution plot for Citi in 2009
ax_dist2.set_title('Distribution Plot for Citi Group 2008', fontsize=14)			# set custom title , xlabel, and ylabel
ax_dist2.set_xlabel('Distance from Mean Return')															
ax_dist2.set_ylabel('Frequency of Returns')																	


### Stock grid for entire time index for all Banks
CloseValues = pd.DataFrame()													# Empty DataFrame for Close Values

for tick in tickers:																# for each bank
	CloseValues[tick+' Close'] = bank_stocks[tick]['Close']							# place closing values in new dataframe

fig4 = plt.figure(figsize=(15,5))													# Define new figure													# Define figure title			
ax = fig4.add_axes([.1,.15,.8,.75])													# Define Axes parameters						
ax.grid(True, linestyle='-.')														# Define Grid					
ax.set_title('2006-2016 Bank Stock Prices', fontweight='bold', fontsize=16)			# set the title xlabels and ylabels																
ax.set_xlabel('Year', fontsize=14)																			
ax.set_ylabel('Closing Price', fontsize=14)																			
ax.plot(CloseValues)																# plot the closing values on a line graph			
fig4.legend(tickers, loc='upper right', bbox_to_anchor=(0.75,0.8))					# add a legend														
plt.xticks(rotation=30)																# rotate the year on the graph																					


### Plot a 30 day moving averages for Bank of America in 2008

fig5 = plt.figure(figsize=(12,6))													
ax = fig5.add_axes([.1,.1,.8,.8])													# Define new figure and add axes
CloseValues['BAC Close'][(CloseValues.index >= '2008-01-01') & \
	(CloseValues.index < '2009-01-01')].plot(label='BAC Close')						# Extract closing values for Bank of America in 2008
CloseValues['BAC Close'].ix['2008-01-01':'2009-01-01'].rolling(window=30).\
	mean().plot(label='30 Day Moving Avg')											# Calculate moving average for 2008 BAC closing values. 
ax.set_title('BAC 2008: 30 Day Moving Average', fontweight='bold', fontsize=16)		# Set title xlabels and ylabels
ax.set_xlabel('Month', fontsize=12)													
ax.set_ylabel('Closing Price', fontsize=12)											
plt.legend()																		# plot legend



### Plot a heatmap of the coorelation between each stocks closing price

fig_heat = plt.figure(figsize=(12,6))												# make new figure to customize fig size
ax_heat = fig_heat.add_axes([.1,.1,.8,.8])											# define axes of figure
sns.heatmap(CloseValues.corr(),annot=True,cmap='RdBu_r', linewidth=.2)				# Heatmap of coorelations between each banks closing price
ax_heat.set_title('Coorelation HeatMap', fontweight='bold', fontsize=16)			# Set title xlabels and ylabels
# ax.set_xlabel('Month', fontsize=12)													
# ax.set_ylabel('Closing Price', fontsize=12)											


cluster = sns.clustermap(CloseValues.corr(),annot=True,cmap='RdBu_r', linewidth=.2).\
	fig.suptitle('Coorelation Cluster Map',fontweight='bold',fontsize=16)			# Heatmap which clusters the coorelated values together.


'''
	We can infer here there are coorelations among a few of the banks. For example
	Bank of America, Citi, and Morgan Stanely generally share the same trends. 
	JP Morgan and Wells Fargo also share common trends, but all other combinations
	show weak coorelation. 

'''

plt.show()