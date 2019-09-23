# Matej Badin | UHP | 2019                                             |
# -------------------------------------------------------------------- |
# Packages needed :  numpy, xml.etree.ElementTree, os                  |
# -------------------------------------------------------------------- |

import requests
import lxml.html as lh
import pandas as pd
import re

find_ID = re.compile(r'\d+')

# Find last starting ID --> 1 000 000 000 is just sufficiently large number
url  = 'https://www.crp.gov.sk/5-sk/register-projektov/?page=1000000000'

page = requests.get(url)
doc  = lh.fromstring(page.content)

last_ID = int(doc.find_class('pagelist')[0][-1].text_content())

print('Up to this date there are ',last_ID*20,'donations ...')
print('Going to crawl CRP GOV and build CRP_DB.')

donations_links = []
start_page = 1
for page_ID in range(start_page,last_ID):
	print('\tProcessing page',page_ID,'out of',last_ID)
	url  = 'https://www.crp.gov.sk/5-sk/register-projektov/?page='+str(page_ID)

	page = requests.get(url)
	doc  = lh.fromstring(page.content)

	tr_elements = doc.xpath('//tr')
	donations = [donation for donation in tr_elements if len(donation) == 5]
	links = [donation[1][0].attrib['href'] for donation in donations[1:]]

	donations_links = donations_links + links

	f = open('links.txt', 'a', encoding = 'utf-8')
	for link in links:
		f.write(link+'\n')
	f.close()
