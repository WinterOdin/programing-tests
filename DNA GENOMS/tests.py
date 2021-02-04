import numpy as np
import pandas as pd
import time
import re

start = time.time()
#this is better than csv.DictReader
df = pd.read_csv("genomes.csv", sep=',')
#I need this becouse i don;t know if this val will pas filtering
genome_id  = "M_AURIS_702100"
genome_row = df.loc[df["id"] == genome_id]
genome_val = genome_row.iloc[0]['genome']

#filtering
df['genome'] = df['genome'].str.strip()
filtered_df = df[~df['genome'].str.match('^[ACTGN-]+$')]
invalid_val = len(filtered_df)



#merging two dataframes 
df.drop(filtered_df.index, axis=0,inplace=True)

print(df)

end = time.time()
print(end - start)






