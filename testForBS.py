from requests import get
from urllib3 import request
import urllib3
import certifi
import json

initialNameList = []

def getMolluskInfo():
    genusName = 'diplodocus'
    speciesName = 'longus'

    data2 = {'Name': [], 'PageLink': [], 'Source': [], 'Year': []}

    data2['Name'].append(f'{genusName} {speciesName}')
    yearList = []
    appendNum = 0

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    url = f'https://www.biodiversitylibrary.org/api3?op=GetNameMetadata&name={genusName}+{speciesName}&format=json&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
    r = http.request('GET', url)
    r.status

    data = json.loads(r.data.decode('utf-8'))
    
    if data['Result'][0] != None:
        baseFormat = data['Result'][0]['Titles']
        i = 0
        for i in range(0, len(baseFormat)):
            j = 0
            if appendNum == 10:
                break
            item = baseFormat[i]['Items']
            for j in range(0, len(item)):
                itemID = item[j]['ItemID']
                url2 = f'https://www.biodiversitylibrary.org/api3?op=GetItemMetadata&id={itemID}&idtype=bhl&pages=t&ocr=t&parts=t&format=xml&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
                r2 = get(url2)

                decoded_d = r2.content.decode('utf-8-sig')
                r2.raise_for_status()
                if r2.status_code == 204:
                    print("This is empty")
                    year = ''
                    yearList.append(year)
                    if appendNum == 10:
                        break
                else:
                    data = json.loads(decoded_d)
                    year = int(data['Result'][0]['Year'])
                    yearList.append(year)
                    if appendNum == 10:
                        break

    return 0

getMolluskInfo()