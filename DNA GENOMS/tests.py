from matplotlib import pyplot as plt
from collections import Counter
import seaborn as sns
import pandas as pd
import numpy as np
import time
import os
import re

def get_domain(x, domain):
    w = 0
    pattern = ''.join(['(?:' + letter + '|N)' if letter in ('A', 'C', 'T', 'G') else letter for letter in list(domain)])   
    sentence = x
    if not re.findall(pattern, x):
        w = 0
    else:
        w = 1
    return w

def get_changed(x, genome_val):
    w = []
    for y in range(len(genome_val)):
        if x[y] == genome_val[y] or x[y] == 'N':
            continue
        else:
            c = [genome_val[y], y, x[y]]
            w.append(c)
    return w



start = time.time()
#this is better than manualy setting limiter 
# NOTE this is slower by ~0,04000 
# if you wanna get those ~0,04000 back just delete engine and change sep to ";"
df = pd.read_csv("genomes.csv",  sep = None,engine ='python', )


#I need this becouse i don;t know if this val will pas filtering
genome_id  = "M_AURIS_702100"
genome_row = df.loc[df["id"] == genome_id]
genome_val = genome_row.iloc[0]['genome']
genome_len = len(genome_val)


#filtering in this way becouse if we wanna see wrong ones we have an option to see what went wrong 
df['genome'] = df['genome'].str.strip()
filtered_df = df[~df['genome'].str.match('^[ACTGN-]+$')]
removed = len(filtered_df)
print(f"Removed {removed} rows")


#merging two dataframes 
df.drop(filtered_df.index, axis=0,inplace=True)


#now we filtering our data to get only values that have same len like refrence genome
df.drop(df[df['genome'].str.len() < genome_len].index, inplace=True)


#removing all strings that are identical to our refrence becouse nothing will change 
carbon_copy = df[df['genome'] == genome_val] 
len_copies = len(carbon_copy.index)
df.drop(carbon_copy.index, axis=0,inplace=True)


df['mutations'] = df['genome'].map(lambda x: get_changed(x, genome_val))


one = 1
search = 'ACCA'
if one == 1:
    #We need to add our refrence genome to this if we wanna see full results for domain search
    # if you need add more rows this isn't most efficient way but im doing only one 
    new_row = {'id': genome_id , 'genome':genome_val}
    df = df.append(new_row, ignore_index=True)
    df['genome'] = df['genome'].str.replace('-', '')
    df['isDomainPresent'] = df['genome'].map(lambda x: get_domain(x, search ))


#droping nans if there are any becouse counter won't work 
big_list = df['mutations'].dropna().to_list()
sum_dict = Counter((''.join(map(str, x)) for y in big_list for x in y))
sum_dict = dict((k, v) for k, v in sum_dict.items() if v >= 10)
sum_dict = {k: v for k, v in sorted(sum_dict.items(), key=lambda item: item[1])}

#keys = list(sum_dict.keys())
#vals = [sum_dict[k] for k in keys]
#sns.barplot(x=keys,y=vals)
#plt.show()

plt.hist([i[-1] for i in sum_dict],  bins=len(sum_dict), color='g', label = "Real distribution")
plt.show()


print(sum_dict)
end = time.time()
print(end - start)
