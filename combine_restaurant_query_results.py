# -*- coding: utf-8 -*-
"""
combine and deduplicate point of interest dataframes
to support washington state covid vaccine trial recruitment efforts
"""
import os

import pandas as pd

PATH = 'data/restaurants_and_bars'


def get_dfs():
	master_df = pd.DataFrame()
	all_results = 0
	for f in os.listdir(PATH):
		df = pd.read_csv('{}{}{}'.format(PATH, os.path.sep, f))
		master_df = master_df.append(df)
	print ('total reuslts returned all files {}'.format(len(master_df)))
	return master_df

def filter_df(df):
	df = df.drop_duplicates(subset=['id'])
	df = df.loc[df.state == 'WA']
	df = df.loc[df.is_closed == False]
	df = df.drop(['Unnamed: 0'], axis=1)
	return df


if __name__ == '__main__':
	df = get_dfs()
	df = filter_df(df)
	print ('filtered results {}'.format(len(df)))
	df.to_csv('data/all_washington_restaurants.csv')