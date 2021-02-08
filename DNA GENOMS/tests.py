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


file_name = input("Enter File name: ")
while(os.path.isfile(file_name )==False):
    print("Not a valid file name")
    file_name = input("Enter File name: ")


#this is better than manualy setting limiter 
# NOTE this is slower by ~0,04000 
# if you wanna get those ~0,04000 back just delete engine and change sep to ";"
df = pd.read_csv(file_name, sep = None, engine ='python',)
copy_df = df.copy()

#I need this becouse i don;t know if this val will pas filtering
#genome_id  = "M_AURIS_702100"
reference_id   = input("Enter genome id: ")
while((df['id'] == reference_id ).any() == False):
    print("Genome id wasn't found")
    reference_id   = input("Enter genome id: ")

searched_domain = input("Enter searched domain or press 0 if you don't wanna search for any domain: ")
if searched_domain != '0':
    search = searched_domain
    one = 1
else:
    one = 0


genome_row = df.loc[df["id"] == reference_id ]
genome_val = genome_row.iloc[0]['genome']
genome_len = len(genome_val)


cols = ['id','genome']
df['count'] = df.groupby(cols)['id'].transform('size')
#removing all strings that are identical to our refrence becouse nothing will change 
df.drop_duplicates(subset=['id'] ,inplace=True)
dup_genome = (len(df[df['genome'] == genome_val]))
df.drop_duplicates(subset=['genome'] ,inplace=True)

#now we filtering our data to get only values that have same len like refrence genome
df.drop(df[df['genome'].str.len() < genome_len].index, inplace=True)

#filtering for only containing A,C,T,G,N
df['genome'] = df['genome'].str.strip()
filtered_df = df[~df['genome'].str.match('^[ACTGN-]+$')]
df.drop(filtered_df.index, axis=0,inplace=True)



#mutations 
df['mutations'] = df['genome'].map(lambda x: get_changed(x, genome_val))


if one == 1:
    #We need to add our refrence genome to this if we wanna see full results for domain search
    # if you need add more rows this isn't most efficient way but im doing only one 
    new_row = {'id': reference_id  , 'genome':genome_val, 'count':dup_genome}
    df = df.append(new_row, ignore_index=True)
    df['genome'] = df['genome'].str.replace('-', '')
    df['isDomainPresent'] = df['genome'].map(lambda x: get_domain(x, search ))
    


#droping nans if there are any becouse counter won't work 
print(df['mutations'])
big_list = df['mutations'].dropna().to_list()
print(df['mutations'].dropna())
sum_dict = Counter((''.join(map(str, x)) for y in big_list for x in y))

print(sum_dict)

############# filtering and sorting data for ploting #####################

#allow keys with value >= 5
sum_dict = dict((k, v) for k, v in sum_dict.items() if v >= 2)
print(sum_dict)
#sort data desc if you wanna asc remove reverse
sum_dict = {k: v for k, v in sorted(sum_dict.items(), key=lambda item: item[1], reverse=True)}
print(sum_dict)
out_vis  = input("Enter File name for generated graph: ")
out_csv  = input("Enter File name for generated CSV: ")


#get biggest val for y axis we can do that by just getting first val form dict but what if you wanna sort asc
#we added 10 just to make plot more readable 
maxY = max(sum_dict.values())+10
ind = np.arange(len(sum_dict))
palette = sns.color_palette("husl", len(sum_dict))
plt.bar(ind, list(sum_dict.values()), color=palette)
plt.yticks(np.arange(0, maxY, 5))
plt.xticks(ind, list(sum_dict.keys()), rotation=30)
plt.title('Frequency of mutations that occured >= 2 times')
plt.savefig(out_vis+".pdf")




print(df)


end = time.time()
print(end - start)
