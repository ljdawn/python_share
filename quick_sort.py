#! /usr/bin/env python

def quicksort_v1(lst):
    if (arg == []):
        return []
    return quicksort_v1([i for i in lst[1:] if i<=lst[0]]) + [lst[0]] + \
           quicksort_v1([i for i in lst[1:] if i>lst[0]])

def quicksort_v2(lst):
    if (lst == []):
        return []
    big_list = []
    small_list = []
    middle = lst[0]
    for i in lst[1:]:
        if i <= middle:
            small_list.append(i)
        else:
            big_list.append(i)
    return quicksort_v2(small_list) + [middle] + quicksort_v2(big_list)

