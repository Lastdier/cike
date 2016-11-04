# 将词典中的实体词去除
all_views = []
label = open('data/View.csv', encoding='utf-8')
label_data = label.readlines()
label.close()
for line in label_data:
    line = line.strip()
    content = line.split('\t')
    if not len(content) == 2:
        continue
    label_id = content[0]
    label_view = content[1]
    all_views.append(label_view)

wight = open('result/wight.csv', encoding='utf-8')
wight_data = wight.readlines()
wight.close()
filtered_wight = open('result/filtered_wight.csv', 'w', encoding='utf-8')
for line in wight_data:
    l1 = line.strip()
    content = l1.split('\t')
    if not len(content) == 9:
        continue
    word = content[0]
    is_view = False
    for view in all_views:
        if word == view:
            is_view = True
            break
    if is_view:
        continue
    else:
        filtered_wight.write(line)
filtered_wight.close()

