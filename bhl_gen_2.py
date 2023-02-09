# Program: mollusk data web scrapper with generalized version
# Purpose: to scratch data from BHL with API - getting basis of record
# Author: Juwhan Isaac Jung
# Date: 1/30/23

# importing necessary modules
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
from urllib3 import request
import urllib3
import certifi
import json

data2 = {'Name': [], 'PageLink': [], 'Source': [], 'Year': []}


def getExcel(listName, location, sheetName):
    df = pd.read_excel(location, sheet_name = sheetName)

    for i in range(0, len(df.index)):
        if df['Subgenus'][i] == 'x' and df['Subspecies'][i] == 'x':
            name = [df['Genus'][i], '', df['Species'][i], '']
        elif df['Subgenus'][i] != 'x' and df['Subspecies'][i] == 'x':
            name = [df['Genus'][i], df['Subgenus'][i], df['Species'][i], '']
        elif df['Subgenus'][i] == 'x' and df['Subspecies'][i] != 'x':
            name = [df['Genus'][i], '', df['Species'][i], df['Subspecies'][i]]
        else:
            name = [df['Genus'][i], df['Subgenus'][i], df['Species'][i], df['Subspecies'][i]]
        #columns name first, then rows number will be iterated.
        listName.append(name)  # This will append names that has been read from excel to the list

    return listName

def surfAPI(genusName, subGenusName, speciesName, subSpeciesName, appendNum, pageLinkList, sourceNameList):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    if subGenusName == '' and subSpeciesName == '':
        url = f'https://www.biodiversitylibrary.org/api3?op=GetNameMetadata&name={genusName}+{speciesName}&format=json&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
    elif subGenusName != '' and subSpeciesName == '':
        url = f'https://www.biodiversitylibrary.org/api3?op=GetNameMetadata&name={genusName}+{subGenusName}+{speciesName}&format=json&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
    elif subGenusName == '' and subSpeciesName != '':
        url = f'https://www.biodiversitylibrary.org/api3?op=GetNameMetadata&name={genusName}+{speciesName}+{subSpeciesName}&format=json&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
    else:
        url = f'https://www.biodiversitylibrary.org/api3?op=GetNameMetadata&name={genusName}+{subGenusName}+{speciesName}+{subSpeciesName}&format=json&apikey=63a119b4-40ed-4772-aa3d-627a9b2a828a'
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
                            sourceNameList.append('API')
                            appendNum += 1
                            break
                        elif l == len(text) - len(wholeName):
                            break
                    
                    for n in range(0, len(text)):
                        abbrName = genusName[0] + ". " + speciesName
                        if abbrName == text[n:n+len(abbrName)]:
                            pageLinkList.append(pageURL)
                            sourceNameList.append('API')
                            appendNum += 1
                            break
                        elif n == len(text) - len(abbrName):
                            break
    
    return appendNum, pageLinkList, sourceNameList

def surfWithQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum):
    if subGenusName == '' and subSpeciesName == '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+{speciesName}"&stype=F')
    elif subGenusName != '' and subSpeciesName == '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+({subGenusName})+{speciesName}"&stype=F')
    elif subGenusName == '' and subSpeciesName != '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+{speciesName}+{subSpeciesName}"&stype=F')
    else:
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+({subGenusName})+{speciesName}+{subSpeciesName}"&stype=F')

    if response.status_code != 200:
        print('Error has happened')
    else:
        soup = bs(response.text, "html.parser")
        pubs = soup.find_all('div', class_="pubResult")
        for pub in pubs:
            if appendNum == 10:
                break
            anchor = pub.find_all('a') # this creates a list
            link = anchor[0]['href'] # since anchor is a list, we need to tag it as a list first, and then call dictionary keyword 'dict'
            if link[0:5] != 'https':
                link = f'https://www.biodiversitylibrary.org{link}'
            pageLinkList.append(link)
            sourceNameList.append('search WITH quotation')
            appendNum += 1
    return appendNum, pageLinkList, sourceNameList # 임시

def surfWithPartialQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum):
    if subGenusName == '' and subSpeciesName == '':
            response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+{speciesName}"&stype=F')
    elif subGenusName != '' and subSpeciesName == '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+({subGenusName})"+{speciesName}&stype=F')
    elif subGenusName == '' and subSpeciesName != '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm={genusName}+"{speciesName}+{subSpeciesName}"&stype=F')
    else:
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm="{genusName}+({subGenusName})"+"{speciesName}+{subSpeciesName}"&stype=F')

    if response.status_code != 200:
        print('Error has happened')
        print(genusName, speciesName)
    else:
        soup = bs(response.text, "html.parser")
        pubs = soup.find_all('div', class_="pubResult")
        for pub in pubs:
            if appendNum == 10:
                break
            anchor = pub.find_all('a') # this creates a list
            link = anchor[0]['href'] # since anchor is a list, we need to tag it as a list first, and then call dictionary keyword 'dict'
            if link[0:5] != 'https':
                link = f'https://www.biodiversitylibrary.org{link}'
            pageLinkList.append(link)
            sourceNameList.append('search WITH Partial quotation')
            appendNum += 1

    return appendNum, pageLinkList, sourceNameList # 임시

def surfWithOutQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum):
    if subGenusName == '' and subSpeciesName == '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm={genusName}+{speciesName}&stype=F')
    elif subGenusName != '' and subSpeciesName == '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm={genusName}+({subGenusName})+{speciesName}&stype=F')
    elif subGenusName == '' and subSpeciesName != '':
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm={genusName}+{speciesName}+{subSpeciesName}&stype=F')
    else:
        response = get(f'https://www.biodiversitylibrary.org/search?searchTerm={genusName}+({subGenusName})+{speciesName}+{subSpeciesName}&stype=F')

    if response.status_code != 200:
        print('Error has happened')
    else:
        soup = bs(response.text, "html.parser")
        pubs = soup.find_all('div', class_="pubResult")
        for pub in pubs:
            if appendNum == 10:
                break
            anchor = pub.find_all('a') # this creates a list
            link = anchor[0]['href'] # since anchor is a list, we need to tag it as a list first, and then call dictionary keyword 'dict'
            if link[0:5] != 'https':
                link = f'https://www.biodiversitylibrary.org{link}'
            pageLinkList.append(link)
            sourceNameList.append('search WITHOUT quotation')
            appendNum += 1

    return appendNum, pageLinkList, sourceNameList # 임시

def listExtender(columnName, extendingList):
    data2[columnName].extend(extendingList)
    return 0

def fillTheSpace(dataList, pageLinkList):
    for i in range(0, len(pageLinkList) - 1):
        dataList['Name'].append('')

    if len(pageLinkList) == 0:
        dataList['PageLink'].append('')
        dataList['Source'].append('')

    return dataList
    
def make_hyperlink(value):
    return '=HYPERLINK("%s", "%s")' % (value, value)

def exportExcel(location, data2):
    df2 = pd.DataFrame(data2, columns = ['Name', 'PageLink', 'Source'])
    df2['PageLink'] = df2['PageLink'].apply(lambda x: make_hyperlink(x))
    
    df2.to_excel(location, index = False)

    return 0

if __name__ == '__main__':
    initialNameList = []
    fileLoc = r'D:\\coding\\Sample_names.xlsx'
    sheetName = 'Sheet1'
    initialNameList = getExcel(initialNameList, fileLoc, sheetName)
    
    genusName = ''
    subGenusName = ''
    speciesName = ''
    subSpeciesName = ''

    for name in initialNameList:
        genusName = str(name[0]).strip() #Genus Name
        subGenusName = str(name[1]).strip() #Subgenus Name
        speciesName = str(name[2]).strip() #Species Name
        subSpeciesName = str(name[3]).strip() #Subspecies Name
        if subGenusName == '' and subSpeciesName == '':
            data2['Name'].append(f'{genusName} {speciesName}')
        elif subGenusName != '' and subSpeciesName == '':
            data2['Name'].append(f'{genusName} ({subGenusName}) {speciesName}')
        elif subGenusName == '' and subSpeciesName != '':
            data2['Name'].append(f'{genusName} {speciesName} {subSpeciesName}')
        else:
            data2['Name'].append(f'{genusName} ({subGenusName}) {speciesName} {subSpeciesName}')

        pageLinkList = []
        sourceNameList = []
        appendNum = 0

        appendNum, pageLinkList, sourceNameList = surfAPI(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum)
        if appendNum == 0:
            appendNum, pageLinkList, sourceNameList = surfWithQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum)

        if appendNum == 0:
            appendNum, pageLinkList, sourceNameList = surfWithPartialQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum)
        
        if appendNum == 0:
            appendNum, pageLinkList, sourceNameList = surfWithOutQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum)
        
        listExtender('PageLink', pageLinkList)
        listExtender('Source', sourceNameList)
        data2 = fillTheSpace(data2, pageLinkList)

    exportLoc = r'D:\\coding\\test_database.xlsx'
    exportExcel(exportLoc, data2)