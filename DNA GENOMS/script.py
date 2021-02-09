from matplotlib import pyplot as plt
from collections import Counter
import seaborn as sns
import pandas as pd
import numpy as np
import argparse
import time
import os
import re

parser = argparse.ArgumentParser(description="Find genome mutations")
parser.add_argument('-i','--input_csv',metavar='', required=True, help="Path to input CSV")
parser.add_argument('-o','--out_vis', metavar='', required=True, help="Path to output pdf")
parser.add_argument('-u','--out_csv', metavar='', required=True, help="Path to output CSV ")
parser.add_argument('-s','--searched_domain', metavar='', help="String to be searched")
parser.add_argument('-id','--reference_id', metavar='', required=True, help=" ID of the reference genome")
args = parser.parse_args()

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

if __name__ == '__main__':
    file_name = args.input_csv

    
    # NOTE this is slower by ~0,04000 
    # if you wanna get those ~0,04000 back just delete engine and change sep to ";"
    df = pd.read_csv(file_name, sep = None, engine ='python',)
 

    reference_id   = args.reference_id
    #if you wanna check if user input contains only ACTGN letters just   bool(re.match('^[ACTGN]+$', searched_domain)) == True
    if args.searched_domain:
        search = args.searched_domain
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

    #filtering for only containing A,C,T,G,N,-
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
    big_list = df['mutations'].dropna().to_list()
    sum_dict = Counter((''.join(map(str, x)) for y in big_list for x in y))
    
    df.sort_values(['id'], inplace=True, ascending=False)


    ############# filtering and sorting data for ploting #####################
    #allow keys with value >= 5
    sum_dict = dict((k, v) for k, v in sum_dict.items() if v >= 2)
    #sort data desc if you wanna asc remove reverse
    sum_dict = {k: v for k, v in sorted(sum_dict.items(), key=lambda item: item[1], reverse=True)}

    out_vis  = args.out_vis
    out_csv  = args.out_csv


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
    df.to_csv(out_csv+".csv", index = False)

