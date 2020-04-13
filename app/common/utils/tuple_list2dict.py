# coding=utf-8
# email:  lixin@datagrand.com
# create: 2020/4/13-12:08 下午


def tuple_list2dict(t):
    dict = {}
    for a, b, c in t:
        if a in dict:
            if b not in dict[a]:
                dict[a][b] = c
        else:
            dict[a] = {b: c}
    return dict