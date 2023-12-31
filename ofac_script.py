#MADE BY RAFFAELE CRISTODARO
import pandas as pd
import csv
import requests
import json
import xmltodict
from collections import defaultdict

coins = []
myCoins = {}
sdn = defaultdict(list)
filename = 'sdn2.xml'
URL = "https://www.treasury.gov/ofac/downloads/sanctions/1.0/sdn_advanced.xml"

response = requests.get(URL)
with open(filename, 'wb') as file:
    file.write(response.content)

xml_data = open(filename, 'r').read()  # Read file
d = xmltodict.parse(xml_data)

for i in d['Sanctions']['ReferenceValueSets']['FeatureTypeValues']['FeatureType']:
    if 'Digital Currency Address' in i['#text']:
        coins.append(i['@ID'])
        myCoins[i['@ID']] =  i['#text'].replace('Digital Currency Address - ','')
     #   print(i['@ID'],'-',i['#text'])

for i in d['Sanctions']['DistinctParties']['DistinctParty']:
    if 'Feature' in i['Profile'].keys():
        for j in i['Profile']['Feature']:
            if '@FeatureTypeID' in j:
                if type(j) is not str:
                    if str(j['@FeatureTypeID']) in coins:
                     #   print(j)
                     #   print(j['FeatureVersion']['VersionDetail']['#text'])
                        sdn[myCoins[j['@FeatureTypeID']]].append(j['FeatureVersion']['VersionDetail']['#text'])            
                    #    break
    
with open('sdn.json', 'w') as fp:
    json_data = json.dump(sdn, fp)
fp.close()