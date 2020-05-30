# -*- coding: utf-8 -*-
"""
query business types by specific category alias where max query results were reached
for covid map overlay - washington state
"""
import sys
import json
import requests

import numpy as np
import pandas as pd
 

def get_config():
    config = json.load(open('config.json','r'))
    key = config['API_KEY']
    return key


def query_businesses(key, id, loc, alias):
    # https://www.yelp.com/developers/documentation/v3/business
    headers = {'Authorization': 'Bearer %s' % key}
    params = {'location': loc, 'categories': alias, \
                'limit': 50, 'offset': offset}
    url = 'https://api.yelp.com/v3/businesses/search'
    req = requests.get(url, params=params, headers=headers)
    return req


def output_results(result_list):
    df = pd.DataFrame(result_list)
    df[['address1','address2','address3','city','zip_code','country','state','display_address']] = df['location'].apply(pd.Series)
    df[['latitude','longitude']] = df['coordinates'].apply(pd.Series)
    df['alias'] = df['categories'].apply(lambda x: ';'.join([x[i]['alias'] for i in range(len(x))]))
    print (df.columns)
    df = df.drop(columns=['image_url','url','review_count','rating','coordinates', 'categories', \
                        'transactions','location','display_phone','distance','price'])
    df.to_csv('data/max_bar_resto_results.csv')
    print ('{} total distinct results'.format(len(df)))
    


if __name__ == '__main__':
    key = get_config()
    towns = [x.strip() for x in open('refs/query_maxes_restaurants.txt','r').readlines()[1:]]
    categories = json.load(open('refs/categories.json','r'))
    restos = [d['alias'] for d in categories if 'bars' in d['parents'] or 'restaurants' in d['parents']]
    print (len(restos))
    results_list = []
    total_pull = 0
    for t in towns:
        for alias in restos:

            max_query_results = np.inf
            offset = 0          
            while offset < max_query_results and offset < 1000:
                #print ('querying starting at offset {}'.format(offset))
                req = query_businesses(key, offset, '{}, WA'.format(t), alias)
                #print('The status code is {}'.format(req.status_code))
                if req.ok:
                    results = json.loads(req.text)
                    max_query_results = results['total']
                    results_list += results['businesses']
                    num_results = len(results['businesses'])
                    offset += num_results
                    if max_query_results > 1000:
                        print ('MAXING OUT QUERY RESULTS AT {} for {} - {}'.\
                                format(max_query_results, t, alias))
                    
                else:       
                    print('ERROR  {}  - {} '.format(req.status_code, req.reason))
                    continue
            total_pull += max_query_results 
            print ('{} - {}'.format(t, max_query_results))
    print ('{} total results pulled'.format(total_pull))
    output_results(results_list)