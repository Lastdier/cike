result = {}
neg_file = open('result/0.62058.csv', encoding='utf-8')
result_file = open('result/testresult.csv','w', encoding='utf-8')
neg_data = neg_file.readlines()
neg_file.close()
for line in neg_data:
    l1 = line.strip()
    content = l1.split(',')
    if not len(content) == 3:
        continue
    comment_id = content[0]
    view = content[1]
    emotion=content[2]
    result_file.write(comment_id+','+view+','+emotion+'\n')