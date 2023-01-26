# Program: mollusk data web scrapper
# Purpose: to scratch data from BHL with API - getting basis of record
# Author: Juwhan Isaac Jung
# Date: 10/31/22

# importing necessary modules
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
from urllib3 import request
import urllib3
import certifi
import json

initialNameList = []

def getExcel():
    df = pd.read_excel(r'D:\coding\test_file.xlsx', sheet_name = 'Sheet1')

    for i in range(0, len(df.index)): 
        name = [df['Genus'][i], df['Species'][i]] #columns name first, then rows number will be iterated.
        initialNameList.append(name)  # This will append names that has been read from excel to the list

    return 0

def getMolluskInfo():
    genusName = ''
    speciesName = ''

    data2 = {'Name': [], 'PageLink': []}  # This dictionary will store the result data from this program

    for name in initialNameList:
        genusName = name[0].strip() #Genus Name
        speciesName = name[1].strip() #Species Name

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        url = f'https://www.biodiversitylibrary.org/api3?op=GetNameMetadata&name={genusName}+{speciesName}&format=json&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
        r = http.request('GET', url)
        r.status

        data = json.loads(r.data.decode('utf-8'))
        if data['Result'][0] == None:
            continue
        
        data2['Name'].append(str([data['Result'][0]['NameConfirmed']])[2:-2])

        baseFormat = data['Result'][0]['Titles']
        pageLinkList = []

        i = 0
        appendNum = 0

        for i in range(0, len(baseFormat)):
            j = 0
            if appendNum == 10:
                break
            item = baseFormat[i]['Items']
            for j in range(0, len(item)):
                page = item[j]['Pages']
                k = 0
                if appendNum == 10:
                    break
                for k in range(0, len(page)):
                    l = 0
                    n = 0
                    if appendNum == 10:
                        break
                    pageID = page[k]['PageID']
                    pageURL = page[k]['PageUrl']
                    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED' ,ca_certs=certifi.where())
                    url = f'https://www.biodiversitylibrary.org/api3?op=GetPageMetadata&pageid={pageID}&ocr=t&names=t&format=json&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
                    r = http.request('GET', url)
                    r.status

                    data = json.loads(r.data.decode('utf-8'))    
                    text = data['Result'][0]['OcrText'].replace('\n', '')

                    for l in range(0, len(text)):
                        wholeName = genusName + " " + speciesName
                        nameOnText = text[l:l+len(wholeName)]
                        count = 0

                        for m in range(len(wholeName)):
                            if nameOnText[m] != wholeName[m]:
                                count += 1

                        if count <= 1:
                            pageLinkList.append(pageURL)
                            appendNum += 1
                            break
                        elif l == len(text) - len(wholeName):
                            break
                    
                    for n in range(0, len(text)):
                        abbrName = genusName[0] + ". " + speciesName
                        if abbrName == text[n:n+len(abbrName)]:
                            pageLinkList.append(pageURL)
                            appendNum += 1
                            break
                        elif n == len(text) - len(abbrName):
                            break
        count = 0
        if appendNum == 0:
            response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+{speciesName}"&stype=F')
            if response.status_code != 200:
                print('Error has happened')
            else:
                soup = bs(response.text, "html.parser")
                pubs = soup.find_all('div', class_="pubResult")
                for pub in pubs:
                    if count == 10:
                        break
                    anchor = pub.find_all('a') # this creates a list
                    link = anchor[0]['href'] # since anchor is a list, we need to tag it as a list first, and then call dictionary keyword 'dict'
                    if link[0:5] != 'https':
                        link = f'https://www.biodiversitylibrary.org{link}'
                    pageLinkList.append(link)
                    count += 1
        
        if appendNum == 0:
            response = get(f'https://www.biodiversitylibrary.org/search?searchTerm={genusName}+{speciesName}&stype=F')
            if response.status_code != 200:
                print('Error has happened')
            else:
                soup = bs(response.text, "html.parser")
                pubs = soup.find_all('div', class_="pubResult")
                for pub in pubs:
                    if count == 10:
                        break
                    anchor = pub.find_all('a') # this creates a list
                    link = anchor[0]['href'] # since anchor is a list, we need to tag it as a list first, and then call dictionary keyword 'dict'
                    if link[0:5] != 'https':
                        link = f'https://www.biodiversitylibrary.org{link}'
                    pageLinkList.append(link)
                    count += 1
        
        data2['PageLink'].extend(pageLinkList)

        for i in range(0, len(pageLinkList) - 1):
            data2['Name'].append('')

        if len(pageLinkList) == 0:
            data2['PageLink'].append('')
    
    def make_hyperlink(value):
        return '=HYPERLINK("%s", "%s")' % (value, value)

    df2 = pd.DataFrame(data2, columns = ['Name', 'PageLink'])
    df2['PageLink'] = df2['PageLink'].apply(lambda x: make_hyperlink(x))
    
    df2.to_excel(r'D:\\coding\\test_database.xlsx', index = False)

    return 0

getExcel()
getMolluskInfo()