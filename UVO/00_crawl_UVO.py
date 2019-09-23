# Matej Badin | UHP | 2019                                             |
# -------------------------------------------------------------------- |
# Packages needed :  numpy, xml.etree.ElementTree, os                  |
# -------------------------------------------------------------------- |

import requests
import lxml.html as lh
import pandas as pd
import re

find_ID = re.compile(r'\d+')

# Find last page
url  = 'https://www.uvo.gov.sk/vyhladavanie-zakaziek-4dd.html?page=1&limit=80'

page = requests.get(url)
doc  = lh.fromstring(page.content)
last_page = int(doc.xpath("//select[@class='pag-pageNo']")[0][-1].text)

print('Up to this date there are ',int(last_page)*80,'contracts ...')
print('Going to crawl UVO and build UVO_DB.')

contracts_IDs = []
start_page = 1
for page_ID in range(start_page,last_page):
	print('\tProcessing page',page_ID,'out of',last_page)

	url  = 'https://www.uvo.gov.sk/vyhladavanie-zakaziek-4dd.html?page='+str(page_ID)+'&limit=80'
	page = requests.get(url)
	doc  = lh.fromstring(page.content)

	tr_elements = doc.xpath('//tr')
	contracts = [contract for contract in tr_elements if len(contract) == 8]
	IDs = [find_ID.findall(contract[0][0].attrib['href'])[0] for contract in contracts]
	contracts_IDs = contracts_IDs + IDs

	f = open('contract_IDs.txt', 'a', encoding = 'utf-8')
	for ID in IDs:
		f.write(ID+'\n')
	f.close()
