list1 = [['Conus', 'regius', 'abbotti', 'NULL', 'NULL']]
list2 = [['Conus', 'abbotti']]

def compareList(list1, list2):
    for name1 in list1: # Conus regius abbotti
        for name2 in list2: # Conus abbotti
            if name2[0].strip() == name1[0].strip() and name2[1].strip() == name1[4].strip():
                list2.remove(name2)
            elif name2[0].strip() == name1[0].strip() and name2[1].strip() == name1[3].strip():
                list2.remove(name2)
            elif name2[0].strip() == name1[0].strip() and name2[1].strip() == name1[2].strip():
                list2.remove(name2)
            elif name2[0].strip() == name1[0].strip() and name2[1].strip() == name1[1].strip():
                list2.remove(name2)
    
    return list2

print(compareList(list1, list2))