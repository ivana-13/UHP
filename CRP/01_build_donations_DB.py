# Matej Badin | UHP | 2019                                             |
# -------------------------------------------------------------------- |
# Packages needed :  numpy, xml.etree.ElementTree, os                  |
# -------------------------------------------------------------------- |
# Crawl tables with supplemental agreements on CRZ GOV                 |
# Include them inside DB get by 01_parse_xml.py                        |
# -------------------------------------------------------------------- |

import requests
import lxml.html as lh
import pandas as pd
import re
import sys

find_ID = re.compile(r'\d+')
header  = ['Nazov','ID_CRP','Prijmatel_ICO','Prijmatel','Prijmatel_adresa','Miesto_realizacie',
			'Poskytovatel_ICO','Poskytovatel', 'Typ_dotacie', 'Datum_podpisu', 'Datum_ucinnosti',
			'Datum_platnosti','Celkova_cena','Nazov_zmluvy','Prilohy','Link_dotacia']

fo  = open('links.txt','r', encoding = 'utf-8')
links = fo.readlines()
fo.close()

row_list = []
print('Going to build donations DB of',len(links))

for i, link in enumerate(links):
	# Unfortunately some donation may be missing or corrupted
	print('Processing link:',i+1,'out of',len(links))
	sys.stdout.flush()
	url_donation = 'https://www.crp.gov.sk/'+link

	page = requests.get(url_donation)
	doc  = lh.fromstring(page.content)

	# Name
	name = doc[0][7].text_content().replace(' | Register projektov','')

	# Metadata about dates
	dates_area = doc.find_class('area area1')[0][1]
	date_signed     = dates_area[0][1].text_content()
	date_efficiency = dates_area[1][1].text_content()
	date_validity   = dates_area[2][1].text_content()

	# Metadata about name, number, supplier and purchaser
	text_area  = doc.find_class('b_right area area3')[0][1]
	donation_acceptor     = text_area[0][1].text_content()
	donation_acceptor_ICO = text_area[1][1].text_content()
	donation_place        = text_area[2][1].text_content()
	donation_provider     = text_area[3][1].text_content()
	donation_type         = text_area[4][1].text_content()
	if len(text_area) == 6:
		donation_ID = find_ID.findall(text_area[5][1].text_content())[0]
	else:
		donation_ID = find_ID.findall(text_area[6][1].text_content())[0]

	# Metadata about whole price
	price_area = doc.find_class('area area4')[0][2]
	donation_whole_price  = float(price_area[1].text_content().replace(' €','').replace(' ','').replace(',','.'))

	# Metadata about contracts
	if (len(doc.find_class('area area7'))>0):
		contracts_area = doc.find_class('area area7')[0][1]

		for contract in contracts_area[1:]:
			contract_link = contract[1][0].attrib['href']
			contract_name = contract[1][0].text_content()

			url = 'https://www.crp.gov.sk/'+contract_link
			page_contract = requests.get(url)
			doc_contract  = lh.fromstring(page_contract.content)

			table = doc_contract.find_class('table_detail')[0]
			donation_provider_ICO     = table[2][1].text_content()
			donation_acceptor_address = table[6][1].text_content()

			attachments = table[15][1]
			attachments_link = ['https://www.crp.gov.sk'+attachment_link.attrib['href'] for attachment_link in attachments]

			data    = [name, donation_ID, donation_acceptor_ICO, donation_acceptor, donation_acceptor_address, donation_place,
						donation_provider_ICO, donation_provider, donation_type, date_signed, date_efficiency, date_validity, donation_whole_price, contract_name, attachments_link, url_donation]

			row_list.append(dict((label,data[i]) for i, label in enumerate(header)))

	else:
		contract_link = ''
		contract_name = ''
		donation_provider_ICO = ''
		donation_acceptor_address = ''
		attachments_link = ''

		data    = [name, donation_ID, donation_acceptor_ICO, donation_acceptor, donation_acceptor_address, donation_place,
						donation_provider_ICO, donation_provider, donation_type, date_signed, date_efficiency, date_validity, donation_whole_price, contract_name, attachments_link, url_donation]

		row_list.append(dict((label,data[i]) for i, label in enumerate(header)))


	if (i % 50 == 0):
		DB = pd.DataFrame(row_list, columns = header)
		DB.to_csv('CRP_DB_supplements.csv', header = header, sep = '|')
