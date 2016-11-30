label_file = open('data/Train.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
trains={}
for line in label_data:
    line = line.strip()
    line=line.split('\t')
    trains[line[1]]=line[0]

label_file = open('data/Label.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
check_data={}
for line in label_data:
    temp=''
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

result = open('result/filted_testresult.csv','w', encoding='utf-8')
label_file = open('data/Test.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
tests={}
lists={}
for line in label_data:
    line = line.strip()
    line=line.split('\t')
    if(trains.get(line[1])is not None):
        lists[line[0]]=1
        if(check_data.get(trains[line[1]]) is not None):
            for i in range(0,len(list(check_data[trains[line[1]]]))):
                result.write((line[0]+','+list(check_data[trains[line[1]]])[i]+','+check_data[trains[line[1]]][list(check_data[trains[line[1]]])[i]])+'\n')
        else:
            pass
label_file = open('result/result.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
trains={}
for line in label_data:
    temp=line
    line = line.strip()
    line=line.split(',')
    if(lists.get(line[0]) is None):
        result.write(temp)