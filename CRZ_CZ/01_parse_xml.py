# Matej Badin | UHP | 2019                                              |
# --------------------------------------------------------------------  |
# Packages needed :  numpy, xml.etree.ElementTree, os                   |
# --------------------------------------------------------------------  |
# Parsing downloaded data from CRZ GOV obtained by download_dump script |

import os
import xml.etree.cElementTree as ET
import pandas as pd

def find(item,keyword):
	res = item.find(keyword)
	if res: return res.text
	return ''

prefix = '{http://portal.gov.cz/rejstriky/ISRS/1.2/}'

working_dir   = os.getcwd()+'\\DB_dump\\'
corrupted_dir = os.getcwd()+'\\Corrupted_XML_files\\'
files = [f for f in os.listdir(working_dir) if os.path.isfile(os.path.join(working_dir, f))]

header = ['Nazov','ID','Inner-ID','Verzia','Objednavatel_ICO','Objednavatel','Objednavatel_adresa',
		'Dodavatel_ICO','Dodavatel','Dodavatel_adresa','Dalsie_zmluvne_strany','Datum_zverejnenia','Datum_podpisu',
		'Cena_bez_DPH','Cena_s_DPH','Prilohy','Link']
row_list = []

for i, f in enumerate(files):
	file = ET.parse(working_dir+f)
	root = file.getroot()
	contracts = [root[i] for i in range(5,len(root))]

	for contract in contracts:
		contract = contracts[0]

		# Basic information
		contract_ID      = contract[0][0].text
		contract_version = contract[0][1].text

		# Link and date of publication
		contract_link             = contract[1].text
		contract_date_publication = contract[2].text

		# Main contract meta-data area
		contract_info_area = contract[3]

		# Contract
		contract_subject = contract_info_area.find(prefix+'subjekt')
		contract_subject_name = contract_subject[1].text
		contract_subject_ICO  = contract_subject[2].text
		contract_subject_address = contract_subject[3].text

		contract_sides = contract_info_area.findall(prefix+'smluvniStrana')
		contract_name        = contract_info_area.find(prefix+'predmet').text

		try:
			contract_side_name = contract_sides[0][1].text
			contract_side_ICO = contract_sides[0][2].text
			contract_side_address = contract_sides[0][3].text
		except:
			contract_side_name = 'neuvedeno'
			contract_side_ICO = ''
			contract_side_address = ''

		contract_another_sides = [[contract_side[1].text,contract_side[2].text,contract_side[3].text] for contract_side in contract_sides[1:]]

		contract_date_signed = contract_info_area.find(prefix+'datumUzavreni').text
		contract_inner_ID    = find(contract_info_area,prefix+'cisloSmlouvy')
		contract_price_without_DPH = find(contract_info_area,prefix+'hodnotaBezDph')
		contract_price_with_DPH    = find(contract_info_area,prefix+'hodnotaVcetneDph')

		# Contract attachments
		contract_attachments = contract[4].findall(prefix+'priloha')
		contract_attachments = [attachment[2].text for attachment in contract_attachments]

		data   = [contract_name, contract_ID, contract_inner_ID, contract_version, contract_subject_ICO, contract_subject_name, contract_subject_address,
				contract_side_ICO, contract_side_name, contract_side_address, contract_another_sides, contract_date_publication, contract_date_signed,
				contract_price_without_DPH, contract_price_with_DPH, contract_attachments, contract_link]

		row_list.append(dict((label,data[i]) for i, label in enumerate(header)))

	print('Parsed',i+1,'files out of',len(files))
	DB = pd.DataFrame(row_list, columns = header)
	DB.to_csv('CRZ_CZ_DB.csv', header = header, sep = '|')
