from sklearn import svm
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
from methods import *
import time

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

TOTAL_NUMBER_OF_TRAIN = 14533
NUM_OF_TRAIN = 10000
FEATURES_FILE = 'pos_dict.csv'
TEST_FILE = 'Train.csv'
OUTPUT_FILE = 'predict_pos.csv'
NUM_OF_FEATURES = 10271#14271 4797
CLASS_EMOTION = 'pos'
itime=time.time()

#加载词典
NormaleViews=load_table('data/NormalViews.csv',1)
SpecialViews = load_dict('data/SpecialViews.csv')
StopWords = load_dict('data/StopWords.csv')

# 初始化分类器
clf = svm.LinearSVC()
#model = GradientBoostingClassifier()
# 将测试对象转化为向量
features = get_features(FEATURES_FILE, NUM_OF_FEATURES)

train_x, train_y = create_training_set(features, CLASS_EMOTION, NUM_OF_TRAIN)
train_x = preprocessing.normalize(train_x)
clf.fit(train_x, train_y)
#model.fit(train_x, train_y)
t=time.time()
print('训练完成共用时'+str(t-itime))
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
    views = getViews(comment, NormaleViews, SpecialViews)
    # 处理比较句
    if (comment.__contains__('？') and comment.__contains__('怎么')):
        for comview in views:
            result_file.write('%s\t%s\t%d\n' % (comment_id, comview, 1))
        continue
    comviews = getCompSentence(views, l2[1])
    for comview in comviews:
        result_file.write('%s\t%s\t%d\n' % (comment_id, comview, 0))
        views.remove(comview)
    # 处理反比句
    comviews = getInverseSen(views, l2[1])
    for comview in comviews:
        result_file.write('%s\t%s\t%d\n' % (comment_id, comview, 0))
        views.remove(comview)
    lines = re.split('。|,|，|:|：|；|\n', l2[1])
    for i in range(0, len(views)):
        sentence = getSentence(views[i], views, lines)
        words_list = word_filter(sentence, StopWords)
        test_x = search_features_and_wight(words_list, features)
        test_x = [test_x]
        test_x = preprocessing.normalize(test_x)
        test_y = clf.predict(test_x)
        result_file.write('%s\t%s\t%d\n' % (comment_id, views[i],test_y[0]))
result_file.close()
t=time.time()
print('共用时'+str(t-itime))