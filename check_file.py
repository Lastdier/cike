check_data = {}                                                   # 存储标签表（正确答案）
comment_views_checked = {}                                         # 存储已经找到的视角数（用于计算漏判）
tp, fp, fn1, fn2 = 0, 0, 0, 0


label_file = open('data/Label_test.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
for line in label_data:
    l1 = line.strip()
    content = l1.split('\t')
    if not len(content) == 3:
        continue
    comment_id = content[0]
    comment_view = content[1]
    view_emotion = content[2]
    if check_data.get(comment_id) is None:
        check_data[comment_id] = {comment_view: view_emotion}
    else:
        check_data[comment_id][comment_view] = view_emotion
    comment_views_checked[comment_id] = comment_views_checked.get(comment_id, 0) + 1

result_file = open('result/result.csv', encoding='utf-8')
result_data = result_file.readlines()
result_file.close()
for line in result_data:
    l1 = line.strip()
    content = l1.split(',')
    if not len(content) == 3:
        continue
    comment_id = content[0]
    comment_view = content[1]
    view_emotion = content[2]
    if check_data.get(comment_id) is None:
        fn2 += 1
        continue
    if check_data.get(comment_id).get(comment_view) is None:
        fn2 += 1
        continue
    if view_emotion == check_data[comment_id][comment_view]:
        tp += 1
    else:
        fp += 1
    comment_views_checked[comment_id] -= 1

for comment_id in comment_views_checked:
    fn1 += comment_views_checked[comment_id]

R = tp/(tp + fn1)
P = tp/(tp + fp + fn2)
F1 = 2 * P * R / (P + R)
print('tp: %d\nfp: %d\nfn1: %d\nfn2: %d\nR: %.3f\nP: %.3f\nF1: %.3f' % (tp, fp, fn1, fn2, R, P, F1))
