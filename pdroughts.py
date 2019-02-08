import pandas as pd 
import numpy as np 



if __name__ == '__main__':
	df1 = pd.read_csv('droughts.csv')
	ddata = df1.copy()
	# ddata['valid_start'] = pd.to_datetime(ddata['valid_start'])
	# ddata['valid_end'] = pd.to_datetime(ddata['valid_end'])
	del ddata['state']
	del ddata['county']
	ddata['fips'] = [str(int(x)) for x in ddata['fips']]
	ddata['state_fips'] = [int(x[:-3]) for x in ddata['fips']]
	ddata['county_fips'] = [int(x[-3:]) for x in ddata['fips']]

	ddata['d0'] = [100 if x > 100 else x for x in ddata['d0']]
	ddata['d1'] = [100 if x > 100 else x for x in ddata['d1']]
	ddata['d2'] = [100 if x > 100 else x for x in ddata['d2']]
	ddata['d3'] = [100 if x > 100 else x for x in ddata['d3']]
	ddata['d4'] = [100 if x > 100 else x for x in ddata['d4']]
	
	#mapping state name/fips
	df2 = pd.read_csv('stateFIPS.csv')
	sdata = df2.copy()
	fips = sdata.FIPS.unique()
	state = sdata.State.unique()

	mapping = []
	for i in range(len(fips)):
		mapping.append((fips[i],state[i]))
	temp = []
	for x in ddata['state_fips']:
		for y in mapping:
			if x == y[0]:
				temp.append(y[1])
	ddata['state'] = temp

	ddata.to_csv('pdroughts.csv',index = False)

