#her bir tablo i�in linked list tan�mla. birinci tablo node'lar� case numaras� ve bir boyutlu offset array'i tutar.
#ikinci ve ���nc� tablolar i�in linked list string ve string dizisi tutar.
#from ctypes.wintypes import BYTE
#from re import A


class Node:
    def __init__(self, key, listt):
        self.key = key
        self.list = listt

#buradaki de�i�kenleri d�ng�n�n i�inde kullanaca��z. her bir sat�r� kelime kelime belirledi�imiz i�aretlere kadar taray�p 
#field de�erlerini alaca��z. bu de�erleri ald�ktan sonra ilgili listelere ekleyece�iz. En sonunda bu listeleri ilgili dosyalara ekleyece�iz        
plaintiffField = ""
defendantField = ""
numberField = ""
#switch bir sat�r� a�an kay�tlar� belirlemek i�in kullan�l�r.
switch = False
#tablo olu�turmak i�in gereken listeleri olu�tural�m
indexTableList = []
secondaryTableList_plaintiff = [] 
secondaryTableList_defendant = []
#offset bulmak i�in length kullanal�m
lengthOfCursor = 0
#ilk �nce demo dosyas�n� okuyal�m
with open("court-cases.txt", "r") as f:
    for line in f:
        #Her sat�r�n uzunlu�unu bulal�m
        if not switch:
            byteOffset = lengthOfCursor
        lengthOfCursor += len(line) + 1 #+1 is added for \n character at the end of the each row
        if not switch:
        #Birinci alan� alal�m. V. yi g�rene kadar ekle
            firstOffset = line.find("v.") or line.find("V.")# it definitely exist since not switch
            for indis in range(firstOffset):
                plaintiffField += line[indis]
            if(len(secondaryTableList_plaintiff) == 0):
                secondIndexElement = Node(plaintiffField,[])    
                secondaryTableList_plaintiff.append(secondIndexElement)
            else:    
                loop_counter = 0   
                for obj in secondaryTableList_plaintiff:
                    if obj.key == plaintiffField:
                        break
                    if loop_counter == len(secondaryTableList_plaintiff)-1:# son a�amaya kadar loop'tan ��kmad�ysa bu key'in e�iti yoktur.
                        secondIndexElement = Node(plaintiffField,[])    
                        secondaryTableList_plaintiff.append(secondIndexElement)
                        #print(secondIndexElement.key)
                    else:
                        loop_counter += 1
   
        #ikinci alan� alal�m
        secondOffset = line.find("(")
        if secondOffset != -1:
        #range between .v and ( excluded.
            if not switch:
                for indis in range(firstOffset+2, secondOffset):
                    defendantField += line[indis]
                if(len(secondaryTableList_defendant) == 0):
                    secondaryIndexEl = Node(defendantField, [])
                    secondaryTableList_defendant.append(secondaryIndexEl)
                else:    
                    loop_counter = 0
                    for obj in secondaryTableList_defendant:
                        if obj.key == defendantField:
                            break
                        if loop_counter == len(secondaryTableList_defendant)-1:
                            secondaryIndexEl = Node(defendantField, [])
                            secondaryTableList_defendant.append(secondaryIndexEl)
                        else:
                            loop_counter += 1
            else:
                for indis in range(secondOffset):
                    defendantField += line[indis]
                if(len(secondaryTableList_defendant) == 0):
                    secondaryIndexEl = Node(defendantField, [])
                    secondaryTableList_defendant.append(secondaryIndexEl)
                else:    
                    loop_counter = 0
                    for obj in secondaryTableList_defendant:
                        if obj.key == defendantField:
                            break
                        if loop_counter == len(secondaryTableList_defendant)-1:
                            secondaryIndexEl = Node(defendantField, [])
                            secondaryTableList_defendant.append(secondaryIndexEl)
                        else:
                            loop_counter += 1    
                switch = False
                
        else: ##ilk olarak firstOffset+2 den almal�y�m. ikinci olarak 0.sat�rdan ba�lamal�y�m.          
           for indis in range(firstOffset+2, len(line)):
               defendantField += line[indis]
           defendantField = defendantField.strip()
           switch = True
        
        #if not switch: 
        #    defendantField = ""
        #else:
        #    pass    

        if not switch:
            thirdOffset = line.find(")")
            for indis in range(secondOffset+1, thirdOffset):
                numberField += line[indis]
                
            #���nc� alan birinci index tablosunda olaca�� i�in index listesi haz�rlayal�m
            indexElement = Node(numberField ,[])# bu index eleman�n� daha sonra indextablosuna ekleme ve yaz�dr.
            indexElement.list.append(byteOffset)
            
            #olu�an index listesini index tablosuna aktaral�m
            indexTableList.append(indexElement)
            #ikincil index tablosunun secondary key'i dava numaras� oldu�undan listeye ekleme i�lemini burada yapmal�y�m.
            #e�er ikincil index tablosunda ilk alan varsa o ilk alan� bulmal� ve numaray� onun listesine eklemeliyim
            for obj in secondaryTableList_plaintiff:
                if obj.key == plaintiffField:
                    obj.list.append(numberField)
                    
            for obj in secondaryTableList_defendant:
                if obj.key == defendantField:
                    obj.list.append(numberField)
        else:
            pass
        
        if not switch:
            plaintiffField = ""
            numberField = ""
            defendantField = ""
 
#ilgili tablolar i�in dizileri olu�turduktan sonra bu dizilerin i�eri�ini dosyalara aktaral�m
##################################################################################SILMEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!
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
##################################################################################SILMEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!
#for obj in secondaryTableList_plaintiff:
#    line = obj.key
#    lt = " ".join(obj.list)
#    line += lt
    #print(f"{type(obj.key)} and {type(obj.list)}")
#    print(line)

#demo dosyas�n� 3 alana b�lelim.
#birinci alan en iki karakteri v. ya da V. olan aland�r. bu son iki karakteri ��kar.
#ikinci alan en son karakteri ( i�areti olan aland�r. bu son karakteri ��kar.
#���nc� alan en son karakteri ) olan aland�r. bu son karakteri ��kar.

#ilk tablo i�in dava numaras� ve o sat�r�n ba�lang�� adresini alal�m.
#ikinci tabloda davac� ad� ve ona kar��l�k gelen dava numaralar�
#���nc� tabloda daval� ad� ve ona kar��l�k gelen dava numaralar�

#search algoritmas�yla birinci tablodan direkt olarak o sat�r�n ba�lang�� offset'ine gideriz.
#ikinci ve ���nc� tablodan bir dava numaras� dizisiyle direkt birinci tabloya gideriz. her dava numaras� i�in ilgili sat�r� �ekeriz.

#dosyalar� yazd�rma i�lemi bittikten sonra kullan�c�ya neyi kullanarak arama yapaca��n� sormal�y�z.
print("Hangi alan ile kayit arayacaksaniz o alani veren karakteri giriniz:\na-Plaintiff \nb-Defendant \nc-Case No")
field = input()
while(field != "a" and field != "b" and field != "c"):
    print("Lutfen gecerli karakterlerden birini giriniz!\na-Plaintiff \nb-Defendat \nc-Case No")
    field = input()

#kullan�c� search fonksiyonu ile arama yapar. search fonksiyonu ilgili kay�tlar� d�nd�r�r.
def search():
    pass