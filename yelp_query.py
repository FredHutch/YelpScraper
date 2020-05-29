# -*- coding: utf-8 -*-
"""
query business types for covid map overlay - washington state
"""
import json
import requests
 

def get_config():
	config = json.load(open('config.json','r'))
	key = config['API_KEY']
	return key


def query_businesses(key, location, term, categories):
	# https://www.yelp.com/developers/documentation/v3/business
	headers = {'Authorization': 'Bearer %s' % key}
	params = {'location': location, 'categories': categories, 'limit': 50}
	url = 'https://api.yelp.com/v3/businesses/search'
	req = requests.get(url, params=params, headers=headers)
	return req


def query_categories(key, category_alias):
	# https://www.yelp.com/developers/documentation/v3/category
	headers = {'Authorization': 'Bearer %s' % key}
	url ='https://api.yelp.com/v3/categories/{}'.format(category_alias)
	req=requests.get(url, params=params, headers=headers)
	
	#results = json.loads(req.text)
	return req


def output_results(req):
	results = json.loads(req.text)
	print (results)
	print ('{} returned points of interest'.format(len(results['businesses'])))
	print (results['total'])
	print (results['region'])


if __name__ == '__main__':
	key = get_config()
	# still playing around with the two different endpoints for POI data
	# results = query_categories(key, 'homeandgarden')
	req = query_businesses(key, 'Seattle', 'Home Depot','homeandgarden')
	print('The status code is {}'.format(req.status_code))
	if req.ok:
		output_results(req)
	else:		
		print(req.raise_for_status())