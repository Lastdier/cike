# coding=GBK
from sklearn import svm
from sklearn import preprocessing
from create_training_set import *
import numpy as np


TOTAL_NUMBER_OF_TRAIN = 14533
NUM_OF_TRAIN = 14534
FEATURES_FILE = 'pos_dict.csv'
TEST_FILE = 'Test.csv'
OUTPUT_FILE = 'predict_pos.csv'
NUM_OF_FEATURES = 10101
CLASS_EMOTION = 'pos'

# 初始化分类器
clf = svm.LinearSVC()

train_x, train_y = create_training_set(FEATURES_FILE, NUM_OF_FEATURES, CLASS_EMOTION, NUM_OF_TRAIN)
train_x = preprocessing.normalize(train_x)
clf.fit(train_x, train_y)


# 将测试对象转化为向量
features = get_features(FEATURES_FILE, NUM_OF_FEATURES)

# 加载视角词典
view_file = open('data/View.csv', encoding='utf-8')
view_data = view_file.readlines()
view_file.close()
views_list = []
for line in view_data:
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    views_list.append(l2[1])

# 加载补充视角词典
appended_view = open('data/view_1107.csv', encoding='utf-8')
appended_view_data = appended_view.readlines()
appended_view.close()
for line in appended_view_data:
    l1 = line.strip()
    views_list.append(l1)

test_file = open(('data/'+TEST_FILE), encoding='utf-8')
test_data = test_file.readlines()
test_file.close()
result_file = open(('result/'+OUTPUT_FILE), 'w', encoding='utf-8')
line_count = 0
for line in test_data:
    line_count += 1
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    comment_id = l2[0]
    comment = l2[1]
    # 识别视角
    words_list = word_filter(comment)
    words_list_pointer = 0  # 记录词表下标
    views_index = []  # 记录视角词出现的下标
    for word in words_list:
        for view in views_list:
            if word == view:
                views_index.append(words_list_pointer)
        words_list_pointer += 1
    view_count = len(views_index)  # 此评论视角数
    view_set = {-1}
    for index in views_index:
        view_set.add(words_list[index])
    view_set.remove(-1)
    if len(view_set) == 1:
        view_count = 1

    # 处理文本并测试
    # 单视角
    if view_count == 1:
        test_x = search_features_and_wight(words_list, features)
        test_x = [test_x]
        test_x = preprocessing.normalize(test_x)
        test_y = clf.predict(test_x)
        result_file.write('%s\t%s\t%d\n' % (comment_id, words_list[views_index[0]], test_y[0]))

    # 多视角
    if view_count > 1:
        result = {}
        divide_points = []
        for i in range(len(views_index) - 1):
            divide_points.append(math.ceil((views_index[i]+views_index[i+1])/2))
        divide_points.append(len(words_list)-1)
        words_cache = []
        words_list_pointer = 0
        for point in divide_points:
            while words_list_pointer <= point:
                words_cache.append(words_list[words_list_pointer])
                words_list_pointer += 1
            test_x = search_features_and_wight(words_cache, features)
            num_of_view = divide_points.index(point)                          # 第几个视角
            this_view = words_list[views_index[num_of_view]]                  # 这个视角的名字
            if result.get(this_view) is None:
                result[this_view] = [test_x]
            else:
                result[this_view].append(test_x)
            words_cache = []
        for view in result:
            x = [result[view]]
            x = np.array(x)
            test_x = np.sum(x, axis=1)
            test_x = preprocessing.normalize(test_x)
            test_y = clf.predict(test_x)
            result_file.write('%s\t%s\t%d\n' % (comment_id, view, test_y[0]))

result_file.close()
