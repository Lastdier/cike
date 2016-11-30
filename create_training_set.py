from methods import *

def create_training_set(features,emotion, num_of_train):
    result_X = []         # 结果
    result_Y = []         # 分类结果

    #加载停用词表
    StopWords = load_dict('data/StopWords.csv')

    # 加载label
    label_ref = {}
    label = open('data/Label.csv', encoding='utf-8')
    label_data = label.readlines()
    label.close()
    for line in label_data:
        line = line.strip()
        content = line.split('\t')
        if not len(content) == 3:
            continue
        label_id = content[0]
        label_view = content[1]
        label_emotion = content[2]
        if label_ref.get(label_id) is None:
            label_ref[label_id] = [[label_view, label_emotion]]
        else:
            label_ref[label_id].append([label_view, label_emotion])

    # 加载评论
    train = open('data/Train.csv', encoding='utf-8')
    train_data = train.readlines()
    train.close()
    line_count = 1
    for line in train_data:
        if line_count > num_of_train:
            break
        line = line.strip()
        content = line.split('\t')
        if not len(content) == 2:
            continue
        comment_id = content[0]
        comment = content[1]
        if label_ref.get(comment_id) is None:
            continue
        else:
            view_list = label_ref[comment_id]
        view_count = len(view_list)  # 读取视角数

        lines = re.split('。|,|，|:|：|；|\n',comment)
        dict = {}
        for view,motion in view_list:
            dict[view] = ''
            strour = ''
            temp = 0
            for j in range(0, len(lines)):
                temp_len = 0
                if (lines[j].__contains__(view)):
                    strour += lines[j]
                    dict[view] = strour
                    temp = j
                elif (dict[view] != ''):
                    for s in range(0,view_count):
                        if ((lines[j].__contains__(view_list[s][0])) == False):
                            temp_len += 1
                    if (temp_len == view_count and j > temp):
                        strour += lines[j]
                        dict[view] = strour
                        temp = j
            words_list=word_filter(dict[view],StopWords)
            result_X.append(search_features_and_wight(words_list, features))
            if motion == emotion:
                result_Y.append(1)
            else:
                result_Y.append(0)
        line_count += 1
    return result_X, result_Y