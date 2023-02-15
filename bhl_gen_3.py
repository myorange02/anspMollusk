from bhl_gen_2 import *

if __name__ == '__main__':
    initialNameList = []
    fileLoc = r'D:\coding\Sample_names.xlsx'
    sheetName = 'Sheet1'
    initialNameList = getExcel(initialNameList, fileLoc, sheetName)
    
    genusName = ''  
    subGenusName = ''
    speciesName = ''
    subSpeciesName = ''
    data2 = {'Name': [], 'PageLink': [], 'Source': [], 'Year': []}

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

        appendNum, pageLinkList, sourceNameList = surfAPI(genusName, subGenusName, speciesName, subSpeciesName, appendNum, pageLinkList, sourceNameList)
        if appendNum == 0:
            appendNum, pageLinkList, sourceNameList = surfWithQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum)

        if appendNum == 0:
            appendNum, pageLinkList, sourceNameList = surfWithPartialQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum)
        
        if appendNum == 0:
            appendNum, pageLinkList, sourceNameList = surfWithOutQuotation(genusName, subGenusName, speciesName, subSpeciesName, pageLinkList, sourceNameList, appendNum)
        
        data2 = listExtender(data2, 'PageLink', pageLinkList)
        data2 = listExtender(data2, 'Source', sourceNameList)
        data2 = fillTheSpace(data2, pageLinkList)

    exportLoc = r'D:\coding\test_database.xlsx'
    exportExcel(exportLoc, data2)