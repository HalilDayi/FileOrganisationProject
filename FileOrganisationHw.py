import os
#A list representing an index table holds Node entities. In the primary index list, the nodes maintain a case number and a one-dimensional offset list.
#The secondary index lists hold the name of the plaintiff or defendant and the case numbers associated with those persons.
class Node:
    def __init__(self, key, listt):
        self.key = key
        self.list = listt

#We're going to use the variables here inside the loop.We will scan each line up to the marks we have determined character by character
#and get the field values. Once we have these values, we will add them to the corresponding lists. Eventually, we will add these lists to the relevant files.
plaintiffField = ""
defendantField = ""
numberField = ""
#switch is used to identify records that have two lines.
switch = False
#Let's create the lists required to create the index files. Each list consists of two fields. The first is the key and the second is the list. 
#These lists represent index files. After the loop is finished, each of them is written to separate files.
indexTableList = []
secondaryTableList_plaintiff = [] 
secondaryTableList_defendant = []
#Let's use length to find offset value.
lengthOfCursor = 0
#First, let's read the court-case file.
with open("court-cases.txt", "r") as f:
    for line in f:
        #Let's find the offset of each record.
        if not switch:
            byteOffset = lengthOfCursor
        #1 is added for \n character at the end of the each row.
        lengthOfCursor += len(line) + 1
        if not switch:
        #Combine characters until you see V./v. to get the plaintiff field.
            firstOffset = line.find(" v. ")
            if(firstOffset == -1):
                firstOffset = line.find(" V. ")
            #Let's combine the characters up to firstOffset.
            for indis in range(firstOffset):
                plaintiffField += line[indis]
            #If the list is empty, let's add our first Node.
            if(len(secondaryTableList_plaintiff) == 0):
                secondIndexElement = Node(plaintiffField,[])    
                secondaryTableList_plaintiff.append(secondIndexElement)
            #If there is an Node in the list, scan the list so that the Node we added is not duplicated.
            else:    
                loop_counter = 0
                #If there is a node in the list whose key is equal to the plaintiff field, there is no need to add it.
                for obj in secondaryTableList_plaintiff:
                    if obj.key == plaintiffField:
                        break
                    #If it has not exited the loop until the last stage, the Node with this key is not in the list. That's why we need to add.
                    if loop_counter == len(secondaryTableList_plaintiff)-1:
                        secondIndexElement = Node(plaintiffField,[])    
                        secondaryTableList_plaintiff.append(secondIndexElement)
                    else:
                        loop_counter += 1
   
        #Let's take the defendant field.
        secondOffset = line.find("(")
        if secondOffset != -1:
        #.v/.V and ( are excluded. If it is not a switch, the record does not exceed 1 line.
            if not switch:
                #Let's combine the characters between the characters v./V. and (.
                for indis in range(firstOffset+3, secondOffset):
                    defendantField += line[indis]
                defendantField = defendantField.strip()    
                #If our list is empty, let's add the first Node.
                if(len(secondaryTableList_defendant) == 0):
                    secondaryIndexEl = Node(defendantField, [])
                    secondaryTableList_defendant.append(secondaryIndexEl)
                #If there is an Node in the list, scan the list so that the Node we added is not duplicated.
                else:  
                    loop_counter = 0
                    for obj in secondaryTableList_defendant:
                        #If there is a node in the list whose key is equal to the defendant field, there is no need to add it.
                        if obj.key == defendantField:
                            break
                        #If it has not exited the loop until the last stage, the Node with this key is not in the list. That's why we need to add.
                        if loop_counter == len(secondaryTableList_defendant)-1:
                            secondaryIndexEl = Node(defendantField, [])
                            secondaryTableList_defendant.append(secondaryIndexEl)
                        else:
                            loop_counter += 1
            #If it is a switch, the record is 2 lines and we are now on a bottom line.
            else:
                #Let's combine the characters up to the specified sign.
                for indis in range(secondOffset):
                    defendantField += line[indis]
                #If our list is empty, let's add the first Node.
                if(len(secondaryTableList_defendant) == 0):
                    secondaryIndexEl = Node(defendantField, [])
                    secondaryTableList_defendant.append(secondaryIndexEl)
                 #If there is an Node in the list, scan the list so that the Node we added is not duplicated.
                else:
                    loop_counter = 0
                    for obj in secondaryTableList_defendant:
                        #If there is a node in the list whose key is equal to the defendant field, there is no need to add it.
                        if obj.key == defendantField:
                            break
                        #If it has not exited the loop until the last stage, the Node with this key is not in the list. That's why we need to add.
                        if loop_counter == len(secondaryTableList_defendant)-1:
                            secondaryIndexEl = Node(defendantField, [])
                            secondaryTableList_defendant.append(secondaryIndexEl)
                        else:
                            loop_counter += 1    
                switch = False
        #Else the corresponding record is 2 lines.
        else:
           #We must combine the characters in the first line until the end of the line, starting with a certain character.
           for indis in range(firstOffset+3, len(line)):
               defendantField += line[indis]
           defendantField = defendantField.strip()
           switch = True 

        if not switch:
            #Let's get the number field.
            thirdOffset = line.find(")")
            # Let's combine all the characters up to this ")"character, starting with a certain character.
            for indis in range(secondOffset+1, thirdOffset):
                numberField += line[indis]
                
            #Let's create the Node that stores the number field.
            indexElement = Node(numberField ,[])
            indexElement.list.append(byteOffset)
            
            #Let's add the resulting Node to the relevant list.
            indexTableList.append(indexElement)
            
            #Since the secondary key of the secondary index file is the case number, I should add it to the list here.
            #If I can find the key of the secondary list that belongs to this loop, I should add the number field to its list.
            for obj in secondaryTableList_plaintiff:
                #Let's find the Node whose key is plaintiffField in this loop and add the case number to the Node's list.
                if obj.key == plaintiffField:
                    obj.list.append(numberField)

            #Since the secondary key of the secondary index file is the case number, I should add it to the list here.
            #If I can find the key of the secondary list that belongs to this loop, I should add the number field to its list.
            for obj in secondaryTableList_defendant:
                #Let's find the Node whose key is defendantField in this loop and add the case number to the Node's list.
                if obj.key == defendantField:
                    obj.list.append(numberField)
        else:
            pass
        
        #If the record is two lines, it will be useful for us not to lose the information here when moving to the second line.
        if not switch:
            plaintiffField = ""
            numberField = ""
            defendantField = ""
 
#After creating the lists for the relevant index files, let's transfer the content of these lists to the files.

with open("indexFile.txt", "w") as wf:
    for row in indexTableList:
        line = row.key + " "
        strList = " ".join(map(str, row.list))
        line += strList
        wf.write(line + '\n')
        
with open("secondaryIndexFile_plaintiff.txt", "w") as wf:
    for row in secondaryTableList_plaintiff:
        line = row.key
        strList = " ".join(row.list)
        line += strList#
        wf.write(line + '\n') 
        
with open("secondaryIndexFile_defendant.txt", "w") as wf:
    for row in secondaryTableList_defendant:
        line = row.key
        strList = " ".join(row.list)
        line += strList
        wf.write(line + '\n')

#This function sorts the files in alphabetical order
def sortFile(fileName):
    txtFile = open(f"{fileName}.txt", "r")
    lines = txtFile.readlines()
    lines.sort()
    sortedTxtFile = open(f"{fileName}_sorted.txt", "w")
    for line in lines:
        sortedTxtFile.write(line)
    sortedTxtFile.close()
    txtFile.close()

#Let's sort each resulting file in alphabetical order
fileName = "indexFile"
sortFile(fileName)
fileName = "secondaryIndexFile_plaintiff"
sortFile(fileName)
fileName = "secondaryIndexFile_defendant"
sortFile(fileName)

def find_offset(case_number):
    with open("indexFile.txt", "r") as file:
        for line in file:
            parts = line.split()
            num = parts[0]
            offset = parts[1]
            if num == case_number:
                return offset
    return None



def get_case_from_offset(offset):
    with open("demo.txt", "r") as file:
        file.seek(int(offset))
        return file.readline().strip()



def search():
    print("Hangi alanda arama yapmak istersiniz?")
    print("1. Plaintiff")
    print("2. Defendant")
    print("3. Case Number")

    choice = input("Seçiminizi yapınız (1/2/3): ")

    if choice == "1":
        search_plaintiff()
    elif choice == "2":
        search_defendant()
    elif choice == "3":
        search_case_number()
    else:
        print("Geçersiz seçim!")


def search_plaintiff():
    keyword = input("Plaintiff adını giriniz: ").strip().lower()
    found = False  # Bir eşleşme bulunup bulunmadığını takip etmek için

    with open("secondaryIndexFile_plaintiff.txt", "r") as file:
        for line in file:
            parts = line.strip().split()  # Boşluklara göre ayır
            plantiff_name = ""
            case_numbers = []
            for part in parts:
                if part.isdigit():
                    case_numbers.append(part)
                else:
                    plantiff_name += part + " "

            plantiff_name = plantiff_name.strip().lower()

            if keyword == plantiff_name:
                found = True
                print(f"Plantiff: {plantiff_name.capitalize()}")

                # Case numaralarını ayır
                for case_number in case_numbers:
                    offset = find_offset(case_number)
                    if offset is not None:
                        case_data = get_case_from_offset(offset)
                        print(f"Case Number: {case_number}")
                        print(f"Case Data: {case_data}")
                    else:
                        print(f"Case number bulunamadı: {case_number}")

    if not found:
        print("Plantiff bulunamadı:", keyword)


def search_defendant():
    keyword = input("Defendant adını giriniz: ").strip().lower()

    found = False  # Bir eşleşme bulunup bulunmadığını takip etmek için

    with open("secondaryIndexFile_defendant.txt", "r") as file:
        for line in file:
            parts = line.strip().split()  # Boşluklara göre ayır
            defendant_name = ""
            case_numbers = []
            for part in parts:
                if part.isdigit():
                    case_numbers.append(part)
                else:
                    defendant_name += part + " "

            defendant_name = defendant_name.strip().lower()

            if keyword == defendant_name:
                found = True
                print(f"Defendant: {defendant_name.capitalize()}")

                # Case numaralarını ayır
                for case_number in case_numbers:
                    offset = find_offset(case_number)
                    if offset is not None:
                        case_data = get_case_from_offset(offset)
                        print(f"Case Number: {case_number}")
                        print(f"Case Data: {case_data}")
                    else:
                        print(f"Case number bulunamadı: {case_number}")

    if not found:
        print("Defendant bulunamadı:", keyword)




def search_case_number():
    keyword = input("Case number'ı giriniz: ").strip().lower()

    with open("indexFile.txt", "r") as file:
        for line in file:
            if keyword in line.lower():
                # Case number'a ait offset değerini alın
                offset = int(line.split()[1])
                # Offset değerine göre orijinal dosyadan veriyi alın
                case_data = get_case_from_offset(offset)
                print("Bulunan Case Verisi:")
                print(case_data)
                return

    print("Case number bulunamadı:", keyword)


search()
