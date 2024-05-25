#her bir tablo için linked list tanımla. birinci tablo node'ları case numarası ve bir boyutlu offset array'i tutar.
#ikinci ve üçüncü tablolar için linked list string ve string dizisi tutar.
#from ctypes.wintypes import BYTE
#from re import A


class Node:
    def __init__(self, key, listt):
        self.key = key
        self.list = listt

#buradaki değişkenleri döngünün içinde kullanacağız. her bir satırı kelime kelime belirlediğimiz işaretlere kadar tarayıp 
#field değerlerini alacağız. bu değerleri aldıktan sonra ilgili listelere ekleyeceğiz. En sonunda bu listeleri ilgili dosyalara ekleyeceğiz        
plaintiffField = ""
defendantField = ""
numberField = ""
#switch bir satırı aşan kayıtları belirlemek için kullanılır.
switch = False
#tablo oluşturmak için gereken listeleri oluşturalım
indexTableList = []
secondaryTableList_plaintiff = [] 
secondaryTableList_defendant = []
#offset bulmak için length kullanalım
lengthOfCursor = 0
#ilk önce demo dosyasını okuyalım
with open("court-cases.txt", "r") as f:
    for line in f:
        #Her satırın uzunluğunu bulalım
        if not switch:
            byteOffset = lengthOfCursor
        lengthOfCursor += len(line) + 1 #+1 is added for \n character at the end of the each row
        if not switch:
        #Birinci alanı alalım. V. yi görene kadar ekle
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
                    if loop_counter == len(secondaryTableList_plaintiff)-1:# son aşamaya kadar loop'tan çıkmadıysa bu key'in eşiti yoktur.
                        secondIndexElement = Node(plaintiffField,[])    
                        secondaryTableList_plaintiff.append(secondIndexElement)
                        #print(secondIndexElement.key)
                    else:
                        loop_counter += 1
   
        #ikinci alanı alalım
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
                
        else: ##ilk olarak firstOffset+2 den almalıyım. ikinci olarak 0.satırdan başlamalıyım.          
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
                
            #üçüncü alan birinci index tablosunda olacağı için index listesi hazırlayalım
            indexElement = Node(numberField ,[])# bu index elemanını daha sonra indextablosuna ekleme ve yazıdr.
            indexElement.list.append(byteOffset)
            
            #oluşan index listesini index tablosuna aktaralım
            indexTableList.append(indexElement)
            #ikincil index tablosunun secondary key'i dava numarası olduğundan listeye ekleme işlemini burada yapmalıyım.
            #eğer ikincil index tablosunda ilk alan varsa o ilk alanı bulmalı ve numarayı onun listesine eklemeliyim
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
 
#ilgili tablolar için dizileri oluşturduktan sonra bu dizilerin içeriğini dosyalara aktaralım
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

#demo dosyasını 3 alana bölelim.
#birinci alan en iki karakteri v. ya da V. olan alandır. bu son iki karakteri çıkar.
#ikinci alan en son karakteri ( işareti olan alandır. bu son karakteri çıkar.
#üçüncü alan en son karakteri ) olan alandır. bu son karakteri çıkar.

#ilk tablo için dava numarası ve o satırın başlangıç adresini alalım.
#ikinci tabloda davacı adı ve ona karşılık gelen dava numaraları
#üçüncü tabloda davalı adı ve ona karşılık gelen dava numaraları

#search algoritmasıyla birinci tablodan direkt olarak o satırın başlangıç offset'ine gideriz.
#ikinci ve üçüncü tablodan bir dava numarası dizisiyle direkt birinci tabloya gideriz. her dava numarası için ilgili satırı çekeriz.

#dosyaları yazdırma işlemi bittikten sonra kullanıcıya neyi kullanarak arama yapacağını sormalıyız.

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
