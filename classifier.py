from sklearn.ensemble import GradientBoostingClassifier
import time
from methods import *
from word2vec import *
import jieba

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

# 读取二元组权重
bigram_pos_dict = {}
bigram_neg_dict = {}
bi_sentiment = open('data/bigram_sentiment.csv', encoding='utf-8')
bi_data = bi_sentiment.readlines()
bi_sentiment.close()
for ttt in bi_data:
    l1 = ttt.strip()
    l2 = l1.split(',')
    if not len(l2) == 5:
        continue
    bigram_pos_dict[l2[0]] = float(l2[3])
    bigram_neg_dict[l2[0]] = float(l2[4])

# 读取三元组权重
thigram_pos_dict = {}
thigram_neg_dict = {}
thi_sentiment = open('data/thigram_sentiment.csv', encoding='utf-8')
thi_data = thi_sentiment.readlines()
thi_sentiment.close()
for ttt in thi_data:
    l1 = ttt.strip()
    l2 = l1.split(',')
    if not len(l2) == 5:
        continue
    thigram_pos_dict[l2[0]] = float(l2[3])
    thigram_neg_dict[l2[0]] = float(l2[4])

# 读取单词权重
unigram_pos_dict = {}
unigram_neg_dict = {}
uni_sentiment = open('data/unigram_weight.csv', encoding='utf-8')
uni_data = uni_sentiment.readlines()
uni_sentiment.close()
for ttt in uni_data:
    l1 = ttt.strip()
    l2 = l1.split('\t')
    if not len(l2) == 3:
        continue
    unigram_pos_dict[l2[0]] = float(l2[1])
    unigram_neg_dict[l2[0]] = float(l2[2]) * (193.33 / 266.31)

def create_training_set(num_of_train):
    result_X = []         # 结果
    result_Y = []         # 分类结果

    # 加载停用词表
    StopWords = load_dict('data/StopWords.txt')

    # 加载label
    label_ref = {}
    label = open('data/Label.csv', encoding='utf-8')
    label_data = label.readlines()
    label.close()
    for ooo in label_data:
        ooo = ooo.strip()
        content = ooo.split('\t')
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
    this_line_count = 1
    for ooo in train_data:
        if this_line_count > num_of_train:
            break
        ooo = ooo.strip()
        content = ooo.split('\t')
        if not len(content) == 2:
            continue
        this_comment_id = content[0]
        this_comment = content[1]
        if label_ref.get(this_comment_id) is None:
            continue
        else:
            view_list = label_ref[this_comment_id]
        view_count = len(view_list)  # 读取视角数
        views=[]
        for s in range(view_count):
            views.append(view_list[s][0])
        this_lines = re.split('。|,|，|:|：|；|\n', this_comment)
        for this_view, motion in view_list:
            strour = getSentence(this_view,views,this_lines)
            # 去停前识别二元组
            this_unfiltered = jieba.cut(strour)
            this_unfiltered_list = []
            for this_foo in this_unfiltered:
                this_unfiltered_list.append(this_foo)
            this_pos_bi_feature = 0.
            this_neg_bi_feature = 0.
            this_count = 0
            for this_pointer in range(len(this_unfiltered_list) - 1):
                this_bigram = this_unfiltered_list[this_pointer] + '^' + this_unfiltered_list[this_pointer + 1]
                if not bigram_pos_dict.get(this_bigram) is None:
                    this_pos_bi_feature += bigram_pos_dict[this_bigram]
                    this_neg_bi_feature += bigram_neg_dict[this_bigram]
                    this_count += 1
            if not this_count == 0:
                this_pos_bi_feature = this_pos_bi_feature / this_count
                this_neg_bi_feature = this_neg_bi_feature / this_count

            # 识别三元组
            this_pos_thi_feature = 0.
            this_neg_thi_feature = 0.
            this_count = 0
            for this_pointer in range(len(this_unfiltered_list) - 2):
                this_thigram = this_unfiltered_list[this_pointer] + '^' + this_unfiltered_list[this_pointer + 1] + \
                               '^' + this_unfiltered_list[this_pointer+2]
                if not thigram_pos_dict.get(this_thigram) is None:
                    this_pos_thi_feature += thigram_pos_dict[this_thigram]
                    this_neg_thi_feature += thigram_neg_dict[this_thigram]
                    this_count += 1
            if not this_count == 0:
                this_pos_thi_feature = this_pos_thi_feature / this_count
                this_neg_thi_feature = this_neg_thi_feature / this_count

            this_words_list = word_filter(strour, StopWords)

            # 单词在去停后识别
            this_pos_uni_feature = 0.
            this_neg_uni_feature = 0.
            this_count = 0
            for this_word in this_words_list:
                if not unigram_pos_dict.get(this_word) is None:
                    this_pos_uni_feature += unigram_pos_dict[this_word]
                    this_neg_uni_feature += unigram_neg_dict[this_word]
                    this_count += 1
            if not this_count == 0:
                this_pos_uni_feature = this_pos_uni_feature / this_count
                this_neg_uni_feature = this_neg_uni_feature / this_count

            this_word_vec = get_vec(this_words_list)                          # 词向量200维
            this_snownlp_result = senti_dict[this_comment_id]
            this_word_vec.append(this_snownlp_result)                        # 1维snownlp情感分析整个句子结果
            this_word_vec.append(this_pos_bi_feature - this_neg_bi_feature)                        # 1维2元组正面概率
            this_word_vec.append(this_pos_thi_feature - this_neg_thi_feature)                      # 1维3元组正面概率
            this_word_vec.append(this_pos_uni_feature - this_neg_uni_feature)                      # 1维单词正面概率
            result_X.append(this_word_vec)        # 特征为204维
            if motion == 'pos':
                result_Y.append(1)
            elif motion == 'neg':
                result_Y.append(-1)
            else:
                result_Y.append(0)
        this_line_count += 1
    return result_X, result_Y
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

TOTAL_NUMBER_OF_TRAIN = 14533
NUM_OF_TRAIN = 10000
TEST_FILE = 'Train.csv'
OUTPUT_FILE = 'result.csv'
itime = time.time()

# 加载词典
NormaleViews = load_table('data/NormalViews.csv', 1)
SpecialViews = load_dict('data/SpecialViews.csv')
StopWords = load_dict('data/StopWords.txt')

# 初始化分类器
clf = GradientBoostingClassifier(n_estimators=400)
# 将测试对象转化为向量

train_x, train_y = create_training_set(NUM_OF_TRAIN)

clf.fit(train_x, train_y)
t = time.time()
print('训练完成共用时'+str(t-itime))
test_file = open(('data/'+TEST_FILE), encoding='utf-8')
test_data = test_file.readlines()
test_file.close()
result_file = open(('result/'+OUTPUT_FILE), 'w', encoding='utf-8')
line_count = 0

# 读取snownlp的结果
sentiment_dict = {}
test_sentiment = open('data/TrainSentiment.csv', encoding='utf-8')
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
    if not line_count > NUM_OF_TRAIN:
        continue
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    comment_id = l2[0]
    comment = l2[1]
    # 识别视角
    views = getViews(comment, NormaleViews, SpecialViews)
    # 规则？
    # 用于存放经过规则处理之后应删除的视角
    remove_views = []
    # 处理比较句
    compViews = getCompSentence(views, l2[1])
    for comview in compViews:
        result_file.write('%s,%s,%s\n' % (comment_id, comview,'neu'))
        remove_views.append(comview)
    # 把比较句中的视角词删除了，避免有些视角词同时出现在特殊句式中，这里还有个优先级待做
    for view in remove_views:
        views.remove(view)
    remove_views = []
    # 处理反比句
    comviews = getInverseSen(views, l2[1])
    for comview in comviews:
        result_file.write('%s,%s,%s\n' % (comment_id, comview,'neu'))
        remove_views.append(comview)
    for view in remove_views:
        views.remove(view)
    if views == []:
        continue
    # 分类器判断
    lines = re.split('。|,|，|:|：|；|\n', l2[1])
    for i in range(len(views)):
        sentence = getSentence(views[i], views, lines)
        # 去停前识别bigram
        unfiltered = jieba.cut(sentence)
        unfiltered_list = []
        for foo in unfiltered:
            unfiltered_list.append(foo)
        pos_bi_feature = 0.
        neg_bi_feature = 0.
        count = 0
        for pointer in range(len(unfiltered_list) - 1):
            bigram = unfiltered_list[pointer] + '^' + unfiltered_list[pointer + 1]
            if not bigram_pos_dict.get(bigram) is None:
                pos_bi_feature += bigram_pos_dict[bigram]
                neg_bi_feature += bigram_neg_dict[bigram]
                count += 1
        if not count == 0:
            pos_bi_feature = pos_bi_feature / count
            neg_bi_feature = neg_bi_feature / count

        # 识别三元组
        pos_thi_feature = 0.
        neg_thi_feature = 0.
        count = 0
        for pointer in range(len(unfiltered_list) - 2):
            thigram = unfiltered_list[pointer] + '^' + unfiltered_list[pointer + 1] + '^' + \
                      unfiltered_list[pointer + 2]
            if not thigram_pos_dict.get(thigram) is None:
                pos_thi_feature += thigram_pos_dict[thigram]
                neg_thi_feature += thigram_neg_dict[thigram]
                count += 1
        if not count == 0:
            pos_thi_feature = pos_thi_feature / count
            neg_thi_feature = neg_thi_feature / count

        words_list = word_filter(sentence, StopWords)

        # 单词在去停后识别
        pos_uni_feature = 0.
        neg_uni_feature = 0.
        count = 0
        for word in words_list:
            if not unigram_pos_dict.get(word) is None:
                pos_uni_feature += unigram_pos_dict[word]
                neg_uni_feature += unigram_neg_dict[word]
                count += 1
        if not count == 0:
            pos_uni_feature = pos_uni_feature / count
            neg_uni_feature = neg_uni_feature / count
        word_vec = get_vec(words_list)                              # 200维词向量
        snownlp_result = sentiment_dict[comment_id]                 # snownlp情感分析结果作为1个维度
        word_vec.append(snownlp_result)
        word_vec.append(pos_bi_feature - neg_bi_feature)
        word_vec.append(pos_thi_feature - neg_thi_feature)
        word_vec.append(pos_uni_feature - neg_uni_feature)
        test_x = [word_vec]
        test_y = clf.predict(test_x)
        if (int(test_y[0]) == 0):
            if(sentence.__contains__('召回') or sentence.__contains__('自燃')):
                result_file.write('%s,%s,%s\n' % (comment_id, views[i], 'neg'))
            else:
                result_file.write('%s,%s,%s\n' % (comment_id, views[i], 'neu'))
        elif (int(test_y[0]) == 1):
            result_file.write('%s,%s,%s\n' % (comment_id, views[i], 'pos'))
        elif (int(test_y[0]) == -1):
            result_file.write('%s,%s,%s\n' % (comment_id, views[i], 'neg'))
result_file.close()
t = time.time()
print('共用时'+str(t-itime))