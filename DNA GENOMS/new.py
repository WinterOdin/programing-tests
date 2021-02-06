
list_str = ['AABCDEQHS'* 300, 'LAPEDEXHS'* 300] * 1000
ctr_str = 'AXBCSEQHS'* 300
w_all = []

for x in list_str:
    w = []
    for y in range(len(ctr_str)):
        if x[y] == ctr_str[y]:
            pass
        else:
            c = [ctr_str[y], y, x[y]]
            w.append(c)
            
    w_all.append(w)

print(w_all)