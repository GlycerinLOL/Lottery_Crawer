def Diff(li1, li2): 
    return (list(set(li1).symmetric_difference(set(li2))))


list1 = [1,2,3,4,5]
list2 = [5,6,7,8,9]

print(Diff(list1, list2))