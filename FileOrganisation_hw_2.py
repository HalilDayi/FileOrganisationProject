import os.path
import re
class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []


class BPlusTree:
    def __init__(self, t):
        self.root = BPlusTreeNode(True)
        self.t = t  # Minimum degree (defines the range for number of keys)

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BPlusTreeNode()
            self.root = temp
            temp.children.append(root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, key, value)
        else:
            self.insert_non_full(root, key, value)

    def insert_non_full(self, node, key, value):
        if node.is_leaf:
            i = len(node.keys) - 1
            node.keys.append((None, None))
            while i >= 0 and key < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = (key, value)
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            self.insert_non_full(node.children[i], key, value)

    def split_child(self, node, i):
        t = self.t
        y = node.children[i]
        z = BPlusTreeNode(y.is_leaf)
        node.children.insert(i + 1, z)
        node.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]
        if not y.is_leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and key == node.keys[i][0]:
            return node.keys[i][1]
        elif node.is_leaf:
            return None
        else:
            return self.search(key, node.children[i])


def create_bplus_tree(offsets_file, t):
    bplus_tree = BPlusTree(t)

    with open(offsets_file, "r") as rf:
        lines = rf.readlines()
        for line in lines:
            parts = line.strip().split()
            case_number = parts[0]
            offset = int(parts[1])
            bplus_tree.insert(case_number, offset)
    return bplus_tree


def search_case(bplus_tree, case_number):
    offset = bplus_tree.search(case_number)
    if offset is not None:
        #burada offsetle index dosyasına gidip ordan kaydı alacağız
        with open("court-cases.txt", "r") as rf:
            rf.seek(offset)
            record = rf.readline().strip()
            if ")" not in record:
                record += " " + rf.readline()
            return record
    else:
        return None

def create_idx_file(original_file):
    lengthOfCursor = 0
    byteOffset = 0
    match = 0
    idxList = []
    caseList = []
    firstRow = True
    with open(original_file, "r") as rf:
        for line in rf:
            if ")" in line:
                byteOffset = lengthOfCursor
                if(firstRow):
                    idxList.append(str(byteOffset))
                firstRow = True
                match = re.search(r'\((\d+)\)', line)
                caseList.append(str(match.group(1)))

            elif ")" not in line:
                byteOffset = lengthOfCursor
                idxList.append(str(byteOffset))
                firstRow = False
                lengthOfCursor += len(line) + 1
                continue
            lengthOfCursor += len(line) + 1

    with open("index_file.txt", "w") as wf:
        for i in range(len(caseList)):
            wf.write(f"{caseList[i]} {idxList[i]}\n")

def main():
    print("===========================================")
    print(" Welcome to the Court Case Search System ")
    print("===========================================")
    print("\nThis system allows you to search for court cases by their case number.")
    print("You can enter a case number to retrieve the case name and its offset in the file.")
    print("To exit the system, simply type 'exit'.")
    print("===========================================\n")

    cases_file = 'court-cases.txt'

    #Batch process ile bu fonksiyonu belirli aralıklarla çalıştırıp dosyanın güncel kalmasını sağlayabiliriz.
    #Ancak bu dosya tarihi bir dosya olduğu için değiştirilmesi pek beklenmez.
    if not os.path.isfile('index_file.txt'):
        create_idx_file('court-cases.txt')
    offsets_file = 'index_file.txt'
    t = 3  # Minimum degree

    bplus_tree = create_bplus_tree(offsets_file, t)

    while True:
        case_number_to_search = input("Please enter a case number to search (or type 'exit' to quit): ")
        if case_number_to_search.lower() == 'exit':
            break
        case_name = search_case(bplus_tree, case_number_to_search)
        if case_name:
            print(f"\nCase Name: {case_name}\n")
        else:
            print("\nCase not found.\n")

    print("===========================================")
    print(" Thank you for using the Court Case Search System ")
    print("===========================================")


if __name__ == "__main__":
    main()
