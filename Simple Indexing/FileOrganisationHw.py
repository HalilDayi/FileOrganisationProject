# A list representing an index table holds Node entities. In the primary index list, the nodes maintain a case number
# and a one-dimensional offset list. The secondary index lists hold the name of the plaintiff or defendant and the
# case numbers associated with those persons.


class Node:
    def __init__(self, key, listt):
        self.key = key
        self.list = listt


# We're going to use the variables here inside the loop.We will scan each line up to the marks we have determined
# character by character and get the field values. Once we have these values, we will add them to the corresponding
# lists. Eventually, we will add these lists to the relevant files.
plaintiffField = ""
defendantField = ""
numberField = ""
# switch is used to identify records that have two lines.
switch = False
# Let's create the lists required to create the index files. Each list consists of two fields. The first is the key
# and the second is the list. These lists represent index files. After the loop is finished, each of them is written
# to separate files.
indexTableList = []
secondaryTableList_plaintiff = []
secondaryTableList_defendant = []
# Let's use length to find offset value.
lengthOfCursor = 0
# First, let's read the court-cases file.
with open("court-cases.txt", "r") as f:
    for line in f:
        # Let's find the offset of each record.
        if not switch:
            byteOffset = lengthOfCursor
        # 1 is added for \n character at the end of each row.
        lengthOfCursor += len(line) + 1
        if not switch:
            # Combine characters until you see V./v. to get the plaintiff field.
            firstOffset = line.find(" v. ")
            if firstOffset == -1:
                firstOffset = line.find(" V. ")
            # Let's combine the characters up to firstOffset.
            for indis in range(firstOffset):
                plaintiffField += line[indis]
            # If the list is empty, let's add our first Node.
            if len(secondaryTableList_plaintiff) == 0:
                secondIndexElement = Node(plaintiffField, [])
                secondaryTableList_plaintiff.append(secondIndexElement)
            # If there is a Node in the list, scan the list so that the Node we added is not duplicated.
            else:
                loop_counter = 0
                # If there is a node in the list whose key is equal to the plaintiff field, there is no need to add it.
                for obj in secondaryTableList_plaintiff:
                    if obj.key == plaintiffField:
                        break
                    # If it has not exited the loop until the last stage, the Node with this key is not in the list.
                    # That's why we need to add.
                    if loop_counter == len(secondaryTableList_plaintiff) - 1:
                        secondIndexElement = Node(plaintiffField, [])
                        secondaryTableList_plaintiff.append(secondIndexElement)
                    else:
                        loop_counter += 1

        # Let's take the defendant field.
        secondOffset = line.find("(")
        if secondOffset != -1:
            # .v/.V and ( are excluded. If it is not a switch, the record does not exceed 1 line.
            if not switch:
                # Let's combine the characters between the characters v./V. and (.
                for indis in range(firstOffset + 3, secondOffset):
                    defendantField += line[indis]
                defendantField = defendantField.strip()
                # If our list is empty, let's add the first Node.
                if len(secondaryTableList_defendant) == 0:
                    secondaryIndexEl = Node(defendantField, [])
                    secondaryTableList_defendant.append(secondaryIndexEl)
                # If there is a Node in the list, scan the list so that the Node we added is not duplicated.
                else:
                    loop_counter = 0
                    for obj in secondaryTableList_defendant:
                        # If there is a node in the list whose key is equal to the defendant field, there is no need
                        # to add it.
                        if obj.key == defendantField:
                            break
                        # If it has not exited the loop until the last stage, the Node with this key is not in the
                        # list. That's why we need to add.
                        if loop_counter == len(secondaryTableList_defendant) - 1:
                            secondaryIndexEl = Node(defendantField, [])
                            secondaryTableList_defendant.append(secondaryIndexEl)
                        else:
                            loop_counter += 1
            # If it is a switch, the record is 2 lines, and we are now on a bottom line.
            else:
                # Let's combine the characters up to the specified sign.
                for indis in range(secondOffset):
                    defendantField += line[indis]
                # If our list is empty, let's add the first Node.
                if len(secondaryTableList_defendant) == 0:
                    secondaryIndexEl = Node(defendantField, [])
                    secondaryTableList_defendant.append(secondaryIndexEl)
                # If there is a Node in the list, scan the list so that the Node we added is not duplicated.
                else:
                    loop_counter = 0
                    for obj in secondaryTableList_defendant:
                        # If there is a node in the list whose key is equal to the defendant field, there is no need
                        # to add it.
                        if obj.key == defendantField:
                            break
                        # If it has not exited the loop until the last stage, the Node with this key is not in the
                        # list. That's why we need to add.
                        if loop_counter == len(secondaryTableList_defendant) - 1:
                            secondaryIndexEl = Node(defendantField, [])
                            secondaryTableList_defendant.append(secondaryIndexEl)
                        else:
                            loop_counter += 1
                switch = False
        # Else the corresponding record is 2 lines.
        else:
            # We must combine the characters in the first line until the end of the line, starting with a certain
            # character.
            for indis in range(firstOffset + 3, len(line)):
                defendantField += line[indis]
            defendantField = defendantField.strip()
            switch = True

        if not switch:
            # Let's get the number field.
            thirdOffset = line.find(")")
            # Let's combine all the characters up to this ")"character, starting with a certain character.
            for indis in range(secondOffset + 1, thirdOffset):
                numberField += line[indis]

            # Let's create the Node that stores the number field.
            indexElement = Node(numberField, [])
            indexElement.list.append(byteOffset)

            # Let's add the resulting Node to the relevant list.
            indexTableList.append(indexElement)

            # Since the secondary key of the secondary index file is the case number, I should add it to the list
            # here. If I can find the key of the secondary list that belongs to this loop, I should add the number
            # field to its list.
            for obj in secondaryTableList_plaintiff:
                # Let's find the Node whose key is plaintiffField in this loop and add the case number to the Node's
                # list.
                if obj.key == plaintiffField:
                    obj.list.append(numberField)

            # Since the secondary key of the secondary index file is the case number, I should add it to the list
            # here. If I can find the key of the secondary list that belongs to this loop, I should add the number
            # field to its list.
            for obj in secondaryTableList_defendant:
                # Let's find the Node whose key is defendantField in this loop and add the case number to the Node's
                # list.
                if obj.key == defendantField:
                    obj.list.append(numberField)
        else:
            pass

        # If the record is two lines, it will be useful for us not to lose the information here when moving to the
        # second line.
        if not switch:
            plaintiffField = ""
            numberField = ""
            defendantField = ""

# After creating the lists for the relevant index files, let's transfer the content of these lists to the files.

with open("indexFile.txt", "w") as wf:
    for row in indexTableList:
        line = row.key + " "
        strList = " ".join(map(str, row.list))
        line += strList
        wf.write(line + '\n')

with open("secondaryIndexFile_plaintiff.txt", "w") as wf:
    for row in secondaryTableList_plaintiff:
        line = row.key + " "
        strList = " ".join(row.list)
        line += strList
        wf.write(line + '\n')

with open("secondaryIndexFile_defendant.txt", "w") as wf:
    for row in secondaryTableList_defendant:
        line = row.key + " "
        strList = " ".join(row.list)
        line += strList
        wf.write(line + '\n')


# This function sorts the files in alphabetical order
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


############################################################################################################
def display_intro():
    """Displays the welcome message."""
    print("="*50)
    print(" " * 15 + "WELCOME")
    print("="*50)
    print("This project allows you to search court cases based on specific criteria. "
          "You can choose one of the options below to perform a search:\n")

def display_guide():
    """Displays the search options."""
    print("="*50)
    print("Search options are as follows: ")
    print("1. Plaintiff: Search for cases by the plaintiff's name.")
    print("2. Defendant: Search for cases by the defendant's name.")
    print("3. Case Number: Search for cases by a specific case number.\n")

def find_offset(case_number):
    """Finds the offset of a given case number."""
    with open("indexFile_sorted.txt", "r") as file:
        for line in file:
            parts = line.split()
            num = parts[0]
            offset = parts[1]
            if num == case_number:
                return offset
    return None

def get_case_from_offset(offset):
    """Retrieves case data from given offset."""
    with open("court-cases.txt", "r") as file:
        file.seek(int(offset))
        return file.readline().strip()

def search():
    """Main search function."""
    while True:
        display_intro()
        display_guide()
        print("Which field would you like to search in?")
        print("1. Plaintiff")
        print("2. Defendant")
        print("3. Case Number")
        print("4. Exit")

        choice = input("Please make your choice (1/2/3/4): ")

        if choice == "1":
            search_plaintiff()
        elif choice == "2":
            search_defendant()
        elif choice == "3":
            search_case_number()
        elif choice == "4":
            print("See you later!")
            break
        else:
            print("Invalid choice! Please try again.")

def search_plaintiff():
    """Searches for cases based on plaintiff name."""
    while True:
        print("\n !!! You must enter your name exactly as you registered our system. !!! ")
        keyword = input("Enter plaintiff name (press 'm' to return to the main menu, 'q' to quit): ").strip().lower()
        if keyword == 'm':
            return
        elif keyword == 'q':
            exit_program()

        found = False  # Track whether a match was found

        with open("secondaryIndexFile_plaintiff_sorted.txt", "r") as file:
            for line in file:
                parts = line.strip().split()  # Split by spaces
                plaintiff_name = ""
                case_numbers = []
                for part in parts:
                    if part.isdigit():
                        case_numbers.append(part)
                    else:
                        plaintiff_name += part + " "

                plaintiff_name = plaintiff_name.strip().lower()

                if keyword == plaintiff_name:
                    found = True
                    print(f"\nPlaintiff: {plaintiff_name.capitalize()}\n")

                    # Separate case numbers
                    for case_number in case_numbers:
                        offset = find_offset(case_number)
                        if offset is not None:
                            case_data = get_case_from_offset(offset)
                            # Remove case number from case data
                            case_data = case_data.replace(f"({case_number})", "")
                            print("--------------------------------------------------")
                            print(f"Case Number: {case_number}")
                            print(f"Case Data: {case_data}")
                            print("--------------------------------------------------")
                        else:
                            print(f"Case number not found: {case_number}")
                            print("\n You may have entered incorrect or incomplete data. Please try again")
        if not found:
            print("Plaintiff not found:", keyword)
            print("\n You may have entered incorrect or incomplete data. Please try again")
        return_to_menu()

def search_defendant():
    """Searches for cases based on defendant name."""
    while True:
        print("\n !!! You must enter your name exactly as you registered our system. !!! ")
        keyword = input("Enter defendant name (press 'm' to return to the main menu, 'q' to quit): ").strip().lower()
        if keyword == 'm':
            return
        elif keyword == 'q':
            exit_program()

        found = False  # Track whether a match was found

        with open("secondaryIndexFile_defendant_sorted.txt", "r") as file:
            for line in file:
                parts = line.strip().split()  # Split by spaces
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
                    print(f"\nDefendant: {defendant_name.capitalize()}\n")

                    # Separate case numbers
                    for case_number in case_numbers:
                        offset = find_offset(case_number)
                        if offset is not None:
                            case_data = get_case_from_offset(offset)
                            # Remove case number from case data
                            case_data = case_data.replace(f"({case_number})", "")
                            print("--------------------------------------------------")
                            print(f"Case Number: {case_number}")
                            print(f"Case Data: {case_data}")
                            print("--------------------------------------------------")
                        else:
                            print(f"Case number not found: {case_number}")
                            print("\n You may have entered incorrect or incomplete data. Please try again")

        if not found:
            print("Defendant not found:", keyword)
            print("\n You may have entered incorrect or incomplete data. Please try again")

        return_to_menu()


def search_case_number():
    """Searches for cases based on case number."""
    while True:
        print("\n !!! You must enter your name exactly as you registered our system. !!! ")
        keyword = input("Enter case number (press 'm' to return to the main menu, 'q' to quit): ").strip().lower()
        if keyword == 'm':
            return
        elif keyword == 'q':
            exit_program()

        with open("indexFile_sorted.txt", "r") as file:
            for line in file:
                if keyword in line.lower():
                    # Get the offset value for the case number
                    offset = int(line.split()[1])
                    # Retrieve the data from the original file using the offset value
                    case_data = get_case_from_offset(offset)
                    print("\nCase Number: " + keyword + "\n")
                    print("--------------------------------------------------")
                    print("Case Data Found:")
                    print(case_data)
                    print("--------------------------------------------------")
                    return

        print("Case number not found:", keyword)
        print("\n You may have entered incorrect or incomplete data. Please try again")
        return_to_menu()

def return_to_menu():
    """Returns to the main menu or quits the program."""
    print("\nPress 'm' to return to the main menu, 'q' to quit...")
    choice = input().strip().lower()
    if choice == 'q':
        exit_program()

def exit_program():
    """Exits the program."""
    print("See you later!")
    exit()

search()
