'''
By Somil Singhai
Created on 21/07/2018 for ZS data science challenge

This script contains functions to combine the given
train or test dataset with the Expense and Holidays datasets

'''

##################################################################

import numpy as np 
import pandas as pd 

##################################################################


def pred_exp(year, month, coun):
	pred = 0
	return pred



def comb_with_exp(df1):
	
	exp = pd.read_csv("exp.csv")
	exp = exp.rename(index = str, columns = {'Product_Type': 'Product_ID', 'Expense_Price': 'Expense'})

	df = pd.DataFrame(columns = exp.columns)

	# Adding an expense change column

	for coun in exp.Country.unique():
		expz = exp
		expz = expz[expz['Country'] == coun]
		for pro in expz.Product_ID.unique():
			expc = expz
			expc = expc[expc.Product_ID == pro]
			expc['Exp_change'] = expc.Expense - expc.Expense.shift(1)
			df = df.append(expc)
	df = df.fillna(0).reset_index().drop('index', axis = 1)
	exp = df
	df =  df[['Year', 'Month', 'Country','Product_ID','Expense','Exp_change']]
	n = df.shape[0]

	for y in df1.Year.unique():
		for coun in ['Argentina', 'Columbia']:
			for mon in range(1,13):
				#pred = pred_exp(y, mon, coun)
				df.loc[n] = [y, mon, coun, 3, 4000,0]
				n = n+1
	df1 = df1.merge(df, on = ['Year', 'Month','Product_ID','Country'])  #merge the expense with train
	return df1

###################################################################


def comb_with_holi(df1):
	dfs = pd.read_excel('holidays.xlsx')
	dfs['Date'] = pd.to_datetime(dfs['Date'])

	dfs['Year'] = dfs['Date'].dt.year
	dfs['Month'] = dfs['Date'].dt.month
	dfs['Week'] = dfs['Date'].dt.week
	dfs.drop('Date', axis = 1, inplace =True)

	cols = ['Year', 'Month', 'Week', 'Country', 'Holiday']
	dfs = dfs[cols]
	dfs['Holiday'] = dfs['Holiday'].apply(lambda x : 1)
	dfs = dfs.groupby(['Year', 'Month', 'Week', 'Country'])['Holiday'].apply(sum).reset_index()

	if ('Merchant_ID' in df1.columns):
		dff = df1.merge(dfs, on = ['Year', 'Month','Week','Country'], how = 'left')  #merge the holiday with train
		dff = dff.fillna(0)
	else:
		dfs.drop('Week', axis = 1)
		dfs = dfs.groupby(['Year','Month', 'Country'])['Holiday'].apply(sum).reset_index()
		dff = df1.merge(dfs, on = ['Year', 'Month','Country'], how = 'left')
		dff = dff.fillna(0)
	return dff