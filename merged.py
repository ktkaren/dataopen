import pandas as pd 
import numpy as np
import datetime as dt 
import matplotlib.pyplot as plt



if __name__ == '__main__':
	df = pd.read_csv('dw_merged.csv')
	data = df.copy()
	data['valid_start'] = pd.to_datetime(data['valid_start'])
	data['valid_end'] = pd.to_datetime(data['valid_end'])
	data['use_per_person'] = data['d_totaluse']/data['population']
	temp_num = []
	temp_diff = []
	fips = data.fips.unique()
	for x in fips:
		cdata = data[data['fips'] == x]
		temp_diff.extend(cdata['valid_end'].diff())

	data['continuous'] = [(x == dt.timedelta(days = 7)) for x in temp_diff]

	data['cont'] = [(x == dt.timedelta(days = 7)) for x in temp_diff]
	for y in fips:
		cdata = data[data['fips'] == y]
		#count nums of droughts
		temp_num.extend([list(cdata['continuous']).count(False)] * len(cdata))
	data['num_of_droughts'] = temp_num
	data['use_vs_droughts'] = list(zip(data['num_of_droughts'],data['use_per_person']))
	unique_state = data['state'].unique()
	for s in unique_state:
		sdata = data[data['state'] == s]
		plt.scatter(sdata['use_per_person'],sdata['num_of_droughts'], label = s, marker = '.')
	plt.legend( borderaxespad=0.)
	plt.title('Water use per person vs Number of Groughts')
	plt.xlabel('Usage per person')
	plt.ylabel('Number of Droughts')
	plt.show()
	data.to_csv('temp.csv', index = False)