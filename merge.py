result = {}

neg_file = open('result/predict_neg.csv', encoding='utf-8')
neg_data = neg_file.readlines()
neg_file.close()
for line in neg_data:
    l1 = line.strip()
    content = l1.split('\t')
    if not len(content) == 3:
        continue
    comment_id = content[0]
    view = content[1]
    if content[2] == '1':
        emotion = 'neg'
    if content[2] == '0':
        emotion = 'neu'
    if result.get(comment_id) is None:
        result[comment_id] = [[view, emotion]]
    else:
        result[comment_id].append([view, emotion])

pos_file = open('result/predict_pos.csv', encoding='utf-8')
pos_data = pos_file.readlines()
pos_file.close()
for line in pos_data:
    l1 = line.strip()
    content = l1.split('\t')
    if not len(content) == 3:
        continue
    comment_id = content[0]
    view = content[1]
    if content[2] == '1':
        for i in range(len(result[comment_id])):
            if result[comment_id][i][0] == view:
                result[comment_id][i][1] = 'pos'

result_file = open('result/result.csv', 'w', encoding='utf-8')
for comment_id in result:
    for view in result[comment_id]:
        result_file.write('%s,%s,%s\n' % (comment_id, view[0], view[1]))
result_file.close()