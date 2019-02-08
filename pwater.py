import pandas as pd 
import numpy as np
from pandas._libs.tslib import Timestamp



if __name__ == '__main__':
	df1 = pd.read_csv('pdroughts.csv')
	ddata = df1.copy()
	ddata['valid_start'] = pd.to_datetime(ddata['valid_start'])
	ddata['valid_end'] = pd.to_datetime(ddata['valid_end'])

	#select 2010 droughts data
	ddata = ddata[((ddata['valid_start'] >= Timestamp('2010-01-01 00:00:00')) \
		& (ddata['valid_start'] < Timestamp('2011-01-01 00:00:00'))) \
	& ((ddata['valid_end'] >= Timestamp('2010-01-01 00:00:00')) \
		& (ddata['valid_end'] < Timestamp('2011-01-01 00:00:00')))]
	#only select the droughts(d2-4) that affect at least 50% of the population
	ddata = ddata[ddata['d2'] + ddata['d3'] + ddata['d4'] >= 50]
	ddata = ddata.sort_values(['fips','valid_start'])
	fips = ddata.fips.unique()
	print(len(fips))
	ddata = ddata.reset_index(drop = True)
	# #clean water_usage and merge (2010 only)
	df2 = pd.read_csv('water_usage.csv')
	wdata = df2.copy()[['fips','state_fips','county_fips','population','d_totaluse']]
	mapping = []
	for i in range(len(wdata)):
		if wdata.iloc[i]['fips'] in fips:
			mapping.append((wdata.iloc[i]['fips'], wdata.iloc[i]['d_totaluse'], wdata.iloc[i]['population']))
	print(len(mapping))
	temp_use = []
	temp_pop = []
	for i in range(len(ddata)):
		print(i)
		for x in mapping:
			if ddata.iloc[i]['fips'] == x[0]:
				temp_use.append(x[1])
				temp_pop.append(x[2])
	ddata['population'] = temp_pop
	ddata['d_totaluse'] = temp_use

	ddata.to_csv('dw_merged.csv',index = False)

