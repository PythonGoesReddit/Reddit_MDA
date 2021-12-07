import pandas as pd
pd.set_option('display.float_format', lambda x: '{:.6f}'.format(x))

def initialize_burt(feature_dict):
    N = len(feature_dict)*2
    colnames_nested = [[x+"_present", x+"_absent"] for x in feature_dict.keys()]
    colnames = [i for subl in colnames_nested for i in subl]
    Burt = pd.DataFrame(
    data= [[0]*N]*N,
    columns=pd.Series(colnames),
    index=pd.Series(colnames))
    return Burt

#print(initialize_burt(feats)) This works!


def update_burt(bm, feature_dict):
    colnames_nested = [[x+"_present", x+"_absent"] for x in feature_dict.keys()]
    colnames = [i for subl in colnames_nested for i in subl]
    if colnames != list(bm.columns):
        print("Input dictionary is in wrong format.")
        return
    for key1 in feature_dict:
        for key2 in feature_dict:
            if feature_dict[key1] == 1 and feature_dict[key2] == 1:
                bm.loc[key1+"_present",key2+"_present"] += 1
                bm.loc[key2+"_present",key1+"_present"] += 1
            if feature_dict[key1] == 0 and feature_dict[key2] == 0:
                bm.loc[key1+"_absent",key2+"_absent"] += 1
                bm.loc[key2+"_absent",key1+"_absent"] += 1
            if feature_dict[key1] == 1 and feature_dict[key2] == 0:
                bm.loc[key1+"_present",key2+"_absent"] += 1
                bm.loc[key2+"_absent",key1+"_present"] += 1
            elif feature_dict[key1] == 0 and feature_dict[key2] == 1:
                bm.loc[key1+"_absent",key2+"_present"] += 1
                bm.loc[key2+"_present",key1+"_absent"] += 1

feats_list = [
    {"f1":1, "f2":1, "f3":1},
    {"f1":0, "f2":0, "f3":0},
    {"f1":0, "f2":0, "f3":0},
    {"f1":1, "f2":1, "f3":1}]

BM = initialize_burt(feats_list[0])
for item in feats_list:
    update_burt(BM, item)
