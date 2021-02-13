from datetime import datetime
S = "test.txt"
with open(S) as f:
    lines = f.read().splitlines()
lines_str = [l[0: -1].split() for l in lines]

file_size = 14 * 2**20
filtered = []

for x in lines_str:
    if 'x' in x[1] and int(x[5]) < file_size and x[0] == 'admin':
        filtered.append(x)

if len(filtered) == 1:
    date = [x[2],x[3],x[4]]
    return " ".join(str(x) for x in date)
else:
    compare = []
    for x in filtered:
        date = [x[2],x[3],x[4]]
        date_str = " ".join(str(x) for x in date)
        date_obj = datetime.strptime(date_str, '%d %b %Y').date()
        compare.append(date_obj)
    early = min(compare)
    early_str = early.strftime('%d %b %Y')
    return early_str