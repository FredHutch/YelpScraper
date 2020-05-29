# -*- coding: utf-8 -*-
"""
query business types for covid map overlay - washington state
"""
import sys
import json
import requests

import numpy as np
 
CATEGORY = 'homeandgarden'
LOCATION = 'King County'

def get_config():
	config = json.load(open('config.json','r'))
	key = config['API_KEY']
	return key


def query_businesses(key, offset):
	# https://www.yelp.com/developers/documentation/v3/business
	headers = {'Authorization': 'Bearer %s' % key}
	params = {'location': LOCATION, 'categories': CATEGORY, 'limit': 50, 'offset': offset}
	url = 'https://api.yelp.com/v3/businesses/search'
	req = requests.get(url, params=params, headers=headers)
	return req


def query_categories(key, category_alias):
	# https://www.yelp.com/developers/documentation/v3/category
	headers = {'Authorization': 'Bearer %s' % key}
	url ='https://api.yelp.com/v3/categories/{}'.format(category_alias)
	req = requests.get(url, params=params, headers=headers)	
	return req


def output_results(result_d):
	with open('data/result_{}_{}.json'.format(CATEGORY,LOCATION.replace(' ','')), 'w') as out:
		json.dump(result_d, out)
	


if __name__ == '__main__':
	key = get_config()
	# still playing around with the two different endpoints for POI data
	# results = query_categories(key, 'homeandgarden')
	max_query_results = np.inf
	offset = 0
	results_list = []
	while offset < max_query_results:
		print ('querying starting at offset {}'.format(offset))
		req = query_businesses(key, offset)
		print('The status code is {}'.format(req.status_code))
		if req.ok:
			results = json.loads(req.text)
			max_query_results = results['total']
			results_list.append(results['businesses'])
			num_results = len(results['businesses'])
			print ('{} returned points of interest'.format(num_results))
			print ('total response results: {}'.format(max_query_results))

			offset += num_results
			print ('resetting offset at {}'.format(offset))
			
		else:		
			print('ERROR  '.format(req.raise_for_status()))
			sys.exit()
	output_results(results_list)