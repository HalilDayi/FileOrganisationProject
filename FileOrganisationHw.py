#her bir tablo için linked list tanýmla. birinci tablo node'larý case numarasý ve bir boyutlu offset array'i tutar.
#ikinci ve üçüncü tablolar için linked list string ve string dizisi tutar.
#from ctypes.wintypes import BYTE
#from re import A


class Node:
    def __init__(self, key, listt):
        self.key = key
        self.list = listt

#buradaki deðiþkenleri döngünün içinde kullanacaðýz. her bir satýrý kelime kelime belirlediðimiz iþaretlere kadar tarayýp 
#field deðerlerini alacaðýz. bu deðerleri aldýktan sonra ilgili listelere ekleyeceðiz. En sonunda bu listeleri ilgili dosyalara ekleyeceðiz        
plaintiffField = ""
defendantField = ""
numberField = ""
#switch bir satýrý aþan kayýtlarý belirlemek için kullanýlýr.
switch = False
#tablo oluþturmak için gereken listeleri oluþturalým
indexTableList = []
secondaryTableList_plaintiff = [] 
secondaryTableList_defendant = []
#offset bulmak için length kullanalým
lengthOfCursor = 0
#ilk önce demo dosyasýný okuyalým
with open("court-cases.txt", "r") as f:
    for line in f:
        #Her satýrýn uzunluðunu bulalým
        if not switch:
            byteOffset = lengthOfCursor
        lengthOfCursor += len(line) + 1 #+1 is added for \n character at the end of the each row
        if not switch:
        #Birinci alaný alalým. V. yi görene kadar ekle
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
                    if loop_counter == len(secondaryTableList_plaintiff)-1:# son aþamaya kadar loop'tan çýkmadýysa bu key'in eþiti yoktur.
                        secondIndexElement = Node(plaintiffField,[])    
                        secondaryTableList_plaintiff.append(secondIndexElement)
                        #print(secondIndexElement.key)
                    else:
                        loop_counter += 1
   
        #ikinci alaný alalým
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
                
        else: ##ilk olarak firstOffset+2 den almalýyým. ikinci olarak 0.satýrdan baþlamalýyým.          
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
                
            #üçüncü alan birinci index tablosunda olacaðý için index listesi hazýrlayalým
            indexElement = Node(numberField ,[])# bu index elemanýný daha sonra indextablosuna ekleme ve yazýdr.
            indexElement.list.append(byteOffset)
            
            #oluþan index listesini index tablosuna aktaralým
            indexTableList.append(indexElement)
            #ikincil index tablosunun secondary key'i dava numarasý olduðundan listeye ekleme iþlemini burada yapmalýyým.
            #eðer ikincil index tablosunda ilk alan varsa o ilk alaný bulmalý ve numarayý onun listesine eklemeliyim
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
 
#ilgili tablolar için dizileri oluþturduktan sonra bu dizilerin içeriðini dosyalara aktaralým
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

#demo dosyasýný 3 alana bölelim.
#birinci alan en iki karakteri v. ya da V. olan alandýr. bu son iki karakteri çýkar.
#ikinci alan en son karakteri ( iþareti olan alandýr. bu son karakteri çýkar.
#üçüncü alan en son karakteri ) olan alandýr. bu son karakteri çýkar.

#ilk tablo için dava numarasý ve o satýrýn baþlangýç adresini alalým.
#ikinci tabloda davacý adý ve ona karþýlýk gelen dava numaralarý
#üçüncü tabloda davalý adý ve ona karþýlýk gelen dava numaralarý

#search algoritmasýyla birinci tablodan direkt olarak o satýrýn baþlangýç offset'ine gideriz.
#ikinci ve üçüncü tablodan bir dava numarasý dizisiyle direkt birinci tabloya gideriz. her dava numarasý için ilgili satýrý çekeriz.

#dosyalarý yazdýrma iþlemi bittikten sonra kullanýcýya neyi kullanarak arama yapacaðýný sormalýyýz.
print("Hangi alan ile kayit arayacaksaniz o alani veren karakteri giriniz:\na-Plaintiff \nb-Defendant \nc-Case No")
field = input()
while(field != "a" and field != "b" and field != "c"):
    print("Lutfen gecerli karakterlerden birini giriniz!\na-Plaintiff \nb-Defendat \nc-Case No")
    field = input()

#kullanýcý search fonksiyonu ile arama yapar. search fonksiyonu ilgili kayýtlarý döndürür.
def search():
    pass