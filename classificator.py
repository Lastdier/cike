from sklearn import svm
from sklearn import preprocessing
from methods import *
import time

# 读取snownlp的情感分析结果
senti_dict = {}
train_sentiment = open('data/TrainSentiment.csv', encoding='utf-8')
sentiment_data = train_sentiment.readlines()
train_sentiment.close()
for ttt in sentiment_data:
    l1 = ttt.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    senti_dict[l2[0]] = float(l2[1])

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
        '''
        if line_count > num_of_train:
            break
        '''
        line = line.strip()
        content = line.split('\t')
        if not len(content) == 2:
            continue
        comment_id = content[0]
        comment = content[1]
        if (len(re.findall(r'[。，,；;]', comment)) == 0 and not comment.__contains__('<')):
            continue
        if label_ref.get(comment_id) is None:
            continue
        else:
            view_list = label_ref[comment_id]
        view_count = len(view_list)  # 读取视角数
        views = []
        for s in range(view_count):
            views.append(view_list[s][0])
        compViews = getCompSentence(views, comment)
        comviews = getInverseSen(views,comment)
        if (len(compViews) > 0 or len(comviews) > 0):
            continue
        lines = re.split('。|,|，|:|：|；|\n',comment)
        this_snownlp_result = senti_dict[comment_id]
        for view,motion in view_list:
            strour = getSentence(view, views, lines)
            words_list=word_filter(strour,StopWords)
            result_X.append(search_features_and_wight(this_snownlp_result,words_list, features))
            if motion == emotion:
                result_Y.append(1)
            else:
                result_Y.append(0)
        line_count += 1
    return result_X, result_Y

TOTAL_NUMBER_OF_TRAIN = 14533
NUM_OF_TRAIN = 14533
FEATURES_FILE = 'motion_pos.csv'
TEST_FILE = 'Test.csv'
OUTPUT_FILE = 'predict_pos.csv'
NUM_OF_FEATURES = 11021#11021 5099
CLASS_EMOTION = 'pos'
itime=time.time()

#加载词典
NormaleViews=load_table('data/NormalViews.csv',1)
SpecialViews = load_dict('data/SpecialViews.csv')
StopWords = load_dict('data/StopWords.csv')

# 初始化分类器
clf = svm.LinearSVC()
# 将测试对象转化为向量
features = get_features(FEATURES_FILE, NUM_OF_FEATURES)

train_x, train_y = create_training_set(features, CLASS_EMOTION, NUM_OF_TRAIN)
train_x = preprocessing.normalize(train_x)
clf.fit(train_x, train_y)
t=time.time()
print('训练完成共用时'+str(t-itime))
test_file = open(('data/'+TEST_FILE), encoding='utf-8')
test_data = test_file.readlines()
test_file.close()
result_file = open(('result/'+OUTPUT_FILE), 'w', encoding='utf-8')
line_count = 0

# 读取snownlp的结果
sentiment_dict = {}
test_sentiment = open('data/TestSentiment.csv', encoding='utf-8')
sentiment_data = test_sentiment.readlines()
test_sentiment.close()
for jjj in sentiment_data:
    l1 = jjj.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    sentiment_dict[l2[0]] = float(l2[1])

for line in test_data:
    line_count += 1
    '''
    if not line_count > NUM_OF_TRAIN:
        continue
    '''
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    comment_id = l2[0]
    comment = l2[1]
    # 识别视角
    views = getViews(comment, NormaleViews, SpecialViews)
    # 用于存放经过规则处理之后应删除的视角
    remove_views = []
    # 处理比较句
    compViews = getCompSentence(views, l2[1])
    for comview in compViews:
        result_file.write('%s\t%s\t%d\n' % (comment_id, comview, 0))
        remove_views.append(comview)
    # 把比较句中的视角词删除了，避免有些视角词同时出现在特殊句式中，这里还有个优先级待做
    for view in remove_views:
        views.remove(view)
    remove_views = []
    # 处理反比句
    comviews = getInverseSen(views, l2[1])
    for comview in comviews:
        result_file.write('%s\t%s\t%d\n' % (comment_id,comview,0))
        remove_views.append(comview)
    for view in remove_views:
        views.remove(view)
    if views == []:
        continue
    lines = re.split('。|,|，|:|：|；|\n',comment)
    this_snownlp_result = sentiment_dict[comment_id]
    for i in range(0, len(views)):
        sentence = getSentence(views[i], views, lines)
        words_list = word_filter(sentence, StopWords)
        test_x = search_features_and_wight(this_snownlp_result,words_list, features)
        test_x = [test_x]
        test_x = preprocessing.normalize(test_x)
        test_y = clf.predict(test_x)
        if(CLASS_EMOTION=='neg' and int(test_y[0])==0):
            if(l2[1].__contains__('召回') or l2[1].__contains__('自燃')):
                test_y[0]=1
        result_file.write('%s\t%s\t%d\n' % (comment_id, views[i],test_y[0]))
result_file.close()
t=time.time()
print('共用时'+str(t-itime))