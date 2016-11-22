r = open('result/pos_dict.csv', encoding='gbk')
w = open('data/pos_dict.csv', 'w', encoding='utf-8')
all_data = r.readlines()
for line in all_data:
    d1 = line.strip()
    data = d1.split(',')
    if not len(data) == 4:
        continue
    w.write('%s\t%s\n' % (data[0], data[3]))
r.close()
w.close()
