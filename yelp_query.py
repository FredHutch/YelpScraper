# -*- coding: utf-8 -*-
"""
query business types for covid map overlay - washington state
"""
import sys
import json
import requests

import numpy as np
import pandas as pd
 
SET_NUM = '1'
CATEGORY = 'bars'

def get_config():
	config = json.load(open('config.json','r'))
	key = config['API_KEY']
	return key


def query_businesses(key, id, loc):
	# https://www.yelp.com/developers/documentation/v3/business
	headers = {'Authorization': 'Bearer %s' % key}
	params = {'location': loc, 'categories': CATEGORY, \
				'limit': 50, 'offset': offset}
	url = 'https://api.yelp.com/v3/businesses/search'
	req = requests.get(url, params=params, headers=headers)
	return req


def output_results(result_list):
	df = pd.DataFrame(result_list)
	df[['address1','address2','address3','city','zip_code','country','state','display_address']]\
															 = df['location'].apply(pd.Series)
	df[['latitude','longitude']] = df['coordinates'].apply(pd.Series)
	df['alias'] = df['categories'].apply(lambda x: ';'.join([x[i]['alias'] for i in range(len(x))]))
	print (df.columns)
	df = df.drop(columns=['image_url','url','review_count','rating','coordinates', 'categories', \
						'transactions','location','display_phone','distance','price'])
	df.to_csv('data/{}_results{}.csv'.format(CATEGORY, SET_NUM))
	print ('{} total distinct results'.format(len(df)))
	


if __name__ == '__main__':
	key = get_config()
	# break up town list in case of daily request max
	towns = [x.split()[0] for x in open('refs/wa_town_set{}_.txt'.format(SET_NUM))]
	results_list = []
	total_pull = 0
	for t in towns:
		max_query_results = np.inf
		offset = 0			
		while offset < max_query_results and offset < 1000:
			#print ('querying starting at offset {}'.format(offset))
			req = query_businesses(key, offset, '{}, WA'.format(t)) #, alias)
			#print('The status code is {}'.format(req.status_code))
			if req.ok:
				results = json.loads(req.text)
				max_query_results = results['total']
				results_list += results['businesses']
				num_results = len(results['businesses'])
				offset += num_results
				#print ('resetting offset at {}'.format(offset))
				if max_query_results > 1000:
					print ('MAXING OUT QUERY RESULTS AT {} for {}'.\
							format(max_query_results, t))
				
			else:		
				print('ERROR  {}  - {} '.format(req.status_code, req.reason))
				continue
		total_pull += max_query_results	
		print ('{} - {}'.format(t, max_query_results))
	print ('{} total results pulled'.format(total_pull))
	output_results(results_list)