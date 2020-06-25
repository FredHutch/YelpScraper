import sys, os
import pandas as pd

PATH = 'data/'

retire_df = pd.read_csv('{}{}'.format(PATH, 'retirement_homes_results.csv'))
assisted_df = pd.read_csv('{}{}'.format(PATH, 'assistedliving_results.csv'))
nursing_df = pd.read_csv('{}{}'.format(PATH, 'skillednursing_results.csv'))
print ('df lens retirement homes {}, assisted living {}, skilled nursing {}'\
		.format(len(retire_df), len(assisted_df), len(nursing_df)))


retire_set = set(retire_df.id)
assisted_set = set(assisted_df.id)
nursing_set = set(nursing_df.id)

print ('total retirement homes {}'.format(len(retire_set)))
print ('total assisted living {}'.format(len(assisted_set)))
print ('total skilled nursing {}'.format(len(nursing_set)))

just_retire = retire_set - assisted_set.union(nursing_set)
print ('retirement only {}'.format(len(just_retire)))

just_retire_df = retire_df.loc[retire_df['id'].isin(just_retire)].drop_duplicates(subset=['id'])
just_retire_df.to_csv('{}{}'.format(PATH, 'retirement_only_results.csv'))
print (len(just_retire_df))

just_nursing = nursing_set - assisted_set.union(retire_set)
print ('nursing only {}'.format(len(nursing_set)))

just_nursing_df = nursing_df.loc[nursing_df['id'].isin(just_nursing)].drop_duplicates(subset=['id'])
just_nursing_df.to_csv('{}{}'.format(PATH, 'skilled_nursing_only_results.csv'))
print (len(just_nursing_df))