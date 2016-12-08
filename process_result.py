result_file = open('result/result_3.csv', encoding='utf-8')
result = result_file.readlines()
result_file.close()

output = open('result/result.csv', 'w', encoding='utf-8')
for line in result:
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 3:
        continue
    if l2[2] == '1':
        output.write('%s,%s,%s\n' % (l2[0], l2[1], 'pos'))
    elif l2[2] == '-1':
        output.write('%s,%s,%s\n' % (l2[0], l2[1], 'neg'))
    else:
        output.write('%s,%s,%s\n' % (l2[0], l2[1], 'neu'))
output.close()
