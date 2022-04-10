import pandas as pd
import itertools

class Apriori:

    def __init__(self, dataseturl, min_support = 2, min_confidence = 50):
        # import dataset
        self.dataset = pd.read_csv(dataseturl)
        self.dataset = sorted([[row[column] for column in list(self.dataset) if str(row[column]) != 'nan'] for index, row in self.dataset.iterrows()])
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = []
        self.itemlist = {}
        self.association_rules = []

    # Generate Candidate set of size "size"
    def generate_frequent_itemset(self, item_list, size, previous_frequent_itemset = []):
        if size == 1:
            candidate_set = {}
            for itemset in item_list:
                for item in itemset:
                    candidate_set[item] = (candidate_set[item] if candidate_set.__contains__(item) else 0 )+itemset.count(item)
            self.itemlist = {item:candidate_set[item] for item in list(candidate_set.keys()) if (candidate_set[item]/len(candidate_set)*100) >= self.min_support}
            return candidate_set, {item:candidate_set[item] for item in list(candidate_set.keys()) if (candidate_set[item]/len(candidate_set)*100) >= self.min_support}
        else:
            previous_frequent_itemset = (list(previous_frequent_itemset.keys()))
            # print("========== Size ", size)
            previous_frequent_itemset_combinations = sorted(list(set([item for t in previous_frequent_itemset for item in t]))) if size > 2 else sorted(previous_frequent_itemset)
            
            previous_frequent_itemset_combinations = list(itertools.combinations(previous_frequent_itemset_combinations, size))
            # print("=========================\n Master Combinations \n ", previous_frequent_itemset_combinations)
            candidate = {}
            frequent_itemset = {}
            for item in previous_frequent_itemset_combinations:
                count = 0
                for iter2 in item_list:
                    # print('============================================== \nitem : ', item, "iter2 : ", iter2)
                    if check_sub_lists(item, iter2):
                        count+=1
                    # print("Update count : ", count)
                # print(f"Count {item} : {count} ")
                candidate[item] = count
            for key, value in candidate.items():
                if (value/len(candidate)*100) >= self.min_support:
                    # print("Key : ",key, " value : ", value, " freq_check : ", subset_frequency(key, item_list, size - 1 ))
                    if subset_frequency(key, previous_frequent_itemset, size-1):
                        frequent_itemset[key] = value 
                        self.itemlist[key] = value
    
            return candidate, frequent_itemset
            pass
        pass

    # TODO: Generate frequent itemset
    def get_frequent_itemset(self):
        size = 1
        res = {}
        while True:
            can, res = self.generate_frequent_itemset(self.dataset, size, previous_frequent_itemset=res)
            print(f"=================================================== \n Frequent Itemset Size {size} : {res}")
            if res and size > 1:
                self.frequent_itemsets.append({"size": size, "itemset": res})
            if not res:
                break
            size+=1
        pass

    # TODO: Generate association rules
    def generate_association_rules(self):
        self.get_frequent_itemset()
        association_rules = []
        for itemset in self.frequent_itemsets:
            print(f" ======================================\n Itemset size {itemset['size']}")
            rules = []
            for item in list(itemset['itemset'].keys()):
                # if itemset['size'] == 2:
                #     print("Items : ", item, " s2 : ",[it for it in item])
                subsets = list(itertools.combinations(item, itemset['size'] - 1)) if itemset['size'] - 1 > 1 else [it for it in item]
                rules.append(subsets)
            # print("Rules : ", rules)
            itemset_keys = list(itemset["itemset"].keys())
            for i in range(0, len(itemset_keys)):
                for iter1 in rules[i]:
                    a = iter1
                    b = set(itemset_keys[i]) - (set(iter1) if itemset["size"] > 2 else set({iter1}))
                    # print(" iter1 : ", iter1, "itemset_keys[i] : ", itemset_keys[i])
                    confidence = (get_support(itemset_keys[i], self.itemlist)/get_support(iter1, self.itemlist))*100
                    if confidence >= self.min_confidence:
                        print("{} -> {} = ".format(a,b), confidence)
        pass

    # TODO:  Displaying output
    def ouput(self):
        pass

def check_sub_lists(list1, list2):
    list1 = list(list1)
    list2 = sorted(list2)
    sub_lists = []
    for L in range(0, len(list2)+1):
        for subset in itertools.combinations(list2, L):
            sub_lists.append(list(subset))
    # print("SUBLIST : ",sub_lists)
    return True if list1 in sub_lists else False

def subset_frequency(itemset, candidate_set, size):
    if size > 1:    
        subsets = list(itertools.combinations(itemset, size))
    else:
        subsets = itemset
    # print("============ Freq Subset : ", subsets, "Candidate : ", candidate_set)
    for item in subsets:
        if not item in candidate_set:
            return False
    return True
    pass

def get_support(itemset, itemlist):
    return itemlist[itemset]

def main():
    # apriori_obj = Apriori('Dataset1.csv',)
    min_support = int(input('\n Please enter minimum support \n'))
    min_confidence = int(input('\n Please enter minimum confidence \n' ))
    apriori_obj = Apriori('Amazon_Dataset1.csv',min_support, min_confidence)
    apriori_obj.generate_association_rules()
    #apriori_obj.generate_candidate(apriori_obj.dataset, 4)

    pass

if __name__ == '__main__':
    main()