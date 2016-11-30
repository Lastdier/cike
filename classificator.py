from sklearn import svm
from sklearn import preprocessing
from create_training_set import *
from methods import *
import time

itime=time.time()
TOTAL_NUMBER_OF_TRAIN = 14533
NUM_OF_TRAIN = 10000
FEATURES_FILE = 'motion_neg.csv'
TEST_FILE = 'Train.csv'
OUTPUT_FILE = 'predict_neg.csv'
NUM_OF_FEATURES = 147
CLASS_EMOTION = 'neg'

# 初始化分类器
clf = svm.LinearSVC()

# 将测试对象转化为向量
features = get_features(FEATURES_FILE, NUM_OF_FEATURES)

#加载词典
NormaleViews=load_table('data/NormalViews.csv')
SpecialViews = load_dict('data/SpecialViews.csv')
StopWords = load_dict('data/StopWords.csv')

itime1=time.time()
train_x, train_y = create_training_set(features, CLASS_EMOTION, NUM_OF_TRAIN)
etim=time.time()
print('初始化样本总共用时:'+str(etim-itime1))
itime2=time.time()
train_x = preprocessing.normalize(train_x)
clf.fit(train_x, train_y)
etim=time.time()
print('训练完成总共用时:'+str(etim-itime2))

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
    views = []
    # 处理中文的歧义视角
    comment = preNormalViews(comment)
    # 找出普通视角词
    for view in NormaleViews:
        if (comment.__contains__(view) == True):
            views.append(view)
            comment = comment.replace(view, '')
    # 处理含数字的歧义视角
    comment = preSpecialViews(comment)
    temp_views = jieba.cut(comment)
    for word in temp_views:
        if (SpecialViews.get(word) is not None):
            views.append(word)
        else:
            # 处理英文+数字的视角
            if ((re.match('^[0-9a-zA-Z]+$', word)) and word.isalpha() == False and (word.isdigit() == False)):
                for view in getSpecilaView(word, SpecialViews):
                    views.append(view)
    views = list(set(views))
    # 处理比较句
    if (l2[1].__contains__('?') or l2[1].__contains__('？')):
        for comview in views:
            result_file.write('%s\t%s\t%d\n' % (comment_id,comview,0))
        continue
    comviews = getCompSentence(views,l2[1])
    for comview in comviews:
        result_file.write('%s\t%s\t%d\n' % (comment_id, comview, 0))
        views.remove(comview)
    # 处理反比句
    comviews = getInverseSen(views,l2[1])
    for comview in comviews:
        result_file.write('%s\t%s\t%d\n' % (comment_id, comview, 0))
        views.remove(comview)
    lines = re.split('。|,|，|:|：|；|\n',l2[1])
    dict = {}
    for i in range(0, len(views)):
        motion = ''
        lists = []
        dict[views[i]] = ''
        strour = ''
        temp = 0
        for j in range(0, len(lines)):
            temp_len = 0
            if (lines[j].__contains__(views[i])):
                strour += lines[j]
                dict[views[i]] = strour
                temp = j
            elif (dict[views[i]] != ''):
                for s in range(0, len(views)):
                    if ((lines[j].__contains__(views[s])) == False):
                        temp_len += 1
                if (temp_len == len(views) and j > temp):
                    strour += lines[j]
                    dict[views[i]] = strour
                    temp = j
        words_list = word_filter(dict[views[i]],StopWords)
        test_x = search_features_and_wight(words_list, features)
        test_x = [test_x]
        test_x = preprocessing.normalize(test_x)
        test_y = clf.predict(test_x)
        result_file.write('%s\t%s\t%d\n' % (comment_id,views[i], test_y[0]))
etim=time.time()
print('总共用时:'+str(etim-itime))
result_file.close()