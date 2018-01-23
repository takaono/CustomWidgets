# -*- coding: utf-8 -*-

def makeListByDictKey(key, listOfDict):
    if len(listOfDict) == 0:
        return []

    if not listOfDict[0].has_key(key):
        return []

    return [d[key] for d in listOfDict]