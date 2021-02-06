import numpy as np
import pandas as pd
import time
import re

start = time.time()
#this is better than manualy setting limiter 
# NOTE this is slower by ~0,04000 
# if you wanna get those ~0,04000 back just delete engine and change sep to ";"

df = pd.read_csv("genomes.csv",  sep = None, engine ='python', )

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


#removing all strings that are identical to our refrence
#im doing this beouse if we wanna do some % or graphs we need to know how many identical results are
carbon_copy = df[df['genome'] == genome_val] 
len_copies = len(carbon_copy.index)
df.drop(carbon_copy.index, axis=0,inplace=True)
print(df.head())


end = time.time()
print(end - start)






