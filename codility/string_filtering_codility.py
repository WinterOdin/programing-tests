from datetime import datetime
a = datetime.strptime('2013-09-05 14:08:15', '%Y-%m-%d %H:%M:%S').date()

data = "photo.jpg, Warsaw, 2013-09-05 14:08:15\njohn.png, London, 2015-06-20 15:13:22\nmyFriends.png, Warsaw, 2013-09-05 14:07:13\n Eiffel.jpg, Paris, 2015-07-23 08:03:02\npisatower.jpg, Paris, 2015-07-22 23:59:59\nBOB.jpg, London, 2015-08-05 00:02:03\nnotredame.png, Paris, 2015-09-01 12:00:00\nme.jpg, Warsaw, 2013-09-06 15:40:22\na.png, Warsaw, 2016-02-13 13:33:50\nb.jpg, Warsaw, 2016-01-02 15:12:22\nc.jpg, Warsaw, 2016-01-02 14:34:30\nd.jpg, Warsaw, 2016-01-02 15:15:01\ne.png, Warsaw, 2016-01-02 09:49:09\nf.png, Warsaw, 2016-01-02 10:55:32\ng.jpg, Warsaw, 2016-02-29 22:13:11"

lines = data.splitlines()
lines_split = [i for item in lines for i in item.split(',')]
compiled = [lines_split[i:i + 3] for i in range(0, len(lines_split), 3)]
sorted_comp = sorted(compiled, key = lambda x: datetime.strptime(x[2][1:], '%Y-%m-%d %H:%M:%S'))

list_names = []
for x in sorted_comp:
    ext = x[0].split(".")
    new_name = [x[1],'.',ext[1]]
    list_names.append(''.join(new_name))


for x in list_names:
    hash = {}
    for x in range(0, len(list_names)):
        if list_names[x] not in hash:
            hash[list_names[x]] = 1
        else:
            count = hash[list_names[x]]
            hash[list_names[x]] += 1
            list_names[x] += str(count)
 

for x in range(0, len(list_names)):
    print(list_names[x], end = ' ')