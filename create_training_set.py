from methods import *
import math


def create_training_set(dict_name, k, emotion, num_of_train):
    result_X = []         # 结果
    result_Y = []         # 分类结果

    # 加载字典
    features = get_features(dict_name, k)

    # 加载label
    label_ref = [[] for i in range(28172)]        # 用list保存label，训练集评论最大id是28171
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
        try:
            id_num = int(label_id)
        except:
            continue
        label_ref[id_num].append([label_view, label_emotion])  # label_ref[id][视角][0]是视角名称，label_ref[id][视角][1]是判断结果

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
        try:
            id_num = int(comment_id)
        except:
            continue

        words_list = word_filter(comment)
        view_list = label_ref[id_num]
        view_count = len(view_list)  # 读取视角数

        # 单视角
        if view_count == 1:
            if view_list[0][1] == emotion:
                result_X.append(search_features_and_wight(words_list, features))
                result_Y.append(1)
            else:
                result_X.append(search_features_and_wight(words_list, features))
                result_Y.append(0)

        # 多视角，将评论分成多个部分，视为多个文本
        elif view_count > 1:
            view_index = []  # 找出视角词出现的下标
            foo = 0
            for word in words_list:
                for view in view_list:
                    if word == view[0]:
                        view_index.append(foo)
                foo += 1

            divide_index = []  # 计算出分隔点的下标
            for I in range(len(view_index) - 1):
                divide_index.append(math.ceil((view_index[I] + view_index[I + 1]) / 2))

            # 判断每一段应该是哪个情感，然后统计
            word_cache = []
            words_list_pointer = 0  # 记录处理到评论中的哪个词了
            x_cache = {}
            y_cache = {}
            for I in divide_index:
                this_emotion = 'neu'
                while words_list_pointer <= I:
                    word_cache.append(words_list[words_list_pointer])
                    words_list_pointer += 1
                for view in view_list:
                    if view[0] in word_cache:
                        this_view = view[0]
                        this_emotion = view[1]
                        break
                if x_cache.get(this_view) is None:
                    x_cache[this_view] = [search_features_and_wight(word_cache, features)]
                else:
                    x_cache[this_view].append(search_features_and_wight(word_cache, features))
                if this_emotion == emotion:
                    y_cache[this_view] = 1
                else:
                    y_cache[this_view] = 0
                word_cache = []
            for view in x_cache:
                result_cache = [0.] * k
                for j in range(k):
                    for vector in x_cache[view]:
                        result_cache[j] += vector[j]
                result_X.append(result_cache)
                result_Y.append(y_cache[view])

        line_count += 1

    return result_X, result_Y
