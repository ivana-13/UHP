# Matej Badin | UHP | 2019                                             |
# -------------------------------------------------------------------- |
# Packages needed :  numpy, xml.etree.ElementTree, os                  |
# -------------------------------------------------------------------- |

import requests
import lxml.html as lh
import pandas as pd
import re

ID = '421540'

url  = 'https://www.uvo.gov.sk/vyhladavanie-zakaziek/detail/'+ID
page_info = requests.get(url)
doc  = lh.fromstring(page_info.content)

metadata_table = doc.xpath("//table[@class='table table-info']")

contract_name = metadata_table[0][0][0][1].text_content().strip()
contract_purchaser = metadata_table[0][0][1][1].text_content().strip()

contract_last_update =
contract_CPV		 =
contract_NUTS		 =
contract_type 		 =
contract_type_procedure =
contract_criteria 	 =
contract_EU_funds 	 =
contract_security    =
contract_deadline_explanation =
contract_deadline    =
contract_date_other  =
contract_date_criteria   =
contract_date_publicatin =
contract_electronic_auction =


#'https://www.uvo.gov.sk/vyhladavanie-zakaziek/detail/dokumenty/421540'
#'https://www.uvo.gov.sk/vyhladavanie-zakaziek/detail/oznamenia/421540'

