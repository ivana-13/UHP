# Matej Badin | UHP | 2019                                             |
# -------------------------------------------------------------------- |
# Packages needed :  numpy, xml.etree.ElementTree, os                  |
# -------------------------------------------------------------------- |

import requests
import urllib.request
import datetime
import re
import os

now = datetime.datetime.now()

if not os.path.exists('DB_dump'):
	os.makedirs('DB_dump')

DB_dir   = os.getcwd()+'\\DB_dump\\'

url  = 'https://data.smlouvy.gov.cz/'
years = [str(year) for year in range(2016,now.year+1)]
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

for year in years:
	for month in months:
		print('Downloading DB dump from '+month+'/'+year)
		try:
			urllib.request.urlretrieve('https://data.smlouvy.gov.cz/dump_'+year+'_'+month+'.xml', os.path.join(DB_dir,year+'_'+month+'.xml'))
		except:
			pass
