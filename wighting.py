from methods import *
import math

word_neg_count = {}                                 # 每个词在负面中出现的次数
word_pos_count = {}                                 # 每个词在正面中出现的次数
word_neu_count = {}                                 # 每个词在中性中出现的次数
word_occur = {}                                     # 每个词在多少个文本中出现，用于计算idf
doc_pos_count, doc_neg_count, doc_neu_count = 0, 0, 0     # 文本的情感频数
label_ref = {}                                      # 字典保存label

# 读取训练集输出
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
        label_ref[label_id].append([label_view, label_emotion])  # label_ref[id][视角][0]是视角名称，label_ref[id][视角][1]是判断结果

# 读取训练集输入
train = open('data/Train.csv', encoding='utf-8')
train_data = train.readlines()
train.close()
for line in train_data:
    line = line.strip()
    content = line.split('\t')
    if not len(content) == 2:
        continue
    comment_id = content[0]
    comment = content[1]
# +++++++++++++++++++++++++++++++统计部分++++++++++++++++++++++++++++++++
    words_list = word_filter(comment)
    if label_ref.get(comment_id) is None:
        continue
    else:
        view_list = label_ref[comment_id]
    view_count = len(view_list)                 # 读取视角数

    # 单视角
    if view_count == 1:
        occur_cache = {0}
        for word in words_list:
            occur_cache.add(word)
        occur_cache.remove(0)
        for word in occur_cache:
            word_occur[word] = word_occur.get(word, 0) + 1
        if view_list[0][1] == 'pos':
            for word in words_list:
                word_pos_count[word] = word_pos_count.get(word, 0) + 1
            doc_pos_count += 1
        if view_list[0][1] == 'neg':
            for word in words_list:
                word_neg_count[word] = word_neg_count.get(word, 0) + 1
            doc_neg_count += 1
        if view_list[0][1] == 'neu':
            for word in words_list:
                word_neu_count[word] = word_neu_count.get(word, 0) + 1
            doc_neu_count += 1

    # 多视角，将评论分成多个部分，视为多个文本
    elif view_count > 1:
        view_index = []                     # 找出视角词出现的下标
        foo = 0
        for word in words_list:
            for view in view_list:
                if word == view[0]:
                    view_index.append(foo)
            foo += 1

        divide_index = []                       # 计算出分隔点的下标
        for i in range(len(view_index)-1):
            divide_index.append(math.ceil((view_index[i]+view_index[i+1])/2))
        divide_index.append(len(words_list)-1)

        # 判断每一段应该是哪个情感，然后统计
        word_cache = []
        words_list_pointer = 0                  # 记录处理到评论中的哪个词了
        for i in divide_index:
            this_emotion = 'neu'
            while words_list_pointer <= i:
                word_cache.append(words_list[words_list_pointer])
                words_list_pointer += 1
            for view in view_list:
                if view[0] in word_cache:
                    this_emotion = view[1]
                    break
            if this_emotion == 'pos':
                for word in word_cache:
                    word_pos_count[word] = word_pos_count.get(word, 0) + 1
                doc_pos_count += 1
            if this_emotion == 'neg':
                for word in word_cache:
                    word_neg_count[word] = word_neg_count.get(word, 0) + 1
                doc_neg_count += 1
            if this_emotion == 'neu':
                for word in word_cache:
                    word_neu_count[word] = word_neu_count.get(word, 0) + 1
                doc_neu_count += 1
            occur_cache = {0}
            for word in word_cache:
                occur_cache.add(word)
            occur_cache.remove(0)
            for word in occur_cache:
                word_occur[word] = word_occur.get(word, 0) + 1
            word_cache = []

# +++++++++++++++++++++++++++++计算bdc++++++++++++++++++++++++++++++++++
# 二分类还是三分类？
bdc = {}
for word in word_occur:
    result = 0
    p_pos = word_pos_count.get(word, 0) / doc_pos_count
    p_neg = word_neg_count.get(word, 0) / doc_neg_count
    p_neu = word_neu_count.get(word, 0) / doc_neu_count
    s = p_neg + p_pos + p_neu
    if not p_pos == 0:
        result += (p_pos / s) * math.log2((p_pos / s))
    if not p_neg == 0:
        result += (p_neg / s) * math.log2((p_neg / s))
    if not p_neu == 0:
        result += (p_neu / s) * math.log2((p_neu / s))
    result /= math.log2(3)
    result += 1
    bdc[word] = result

# ++++++++++++++++++++++++++++计算tf+++++++++++++++++++++++
pos_tf = {}
total_pos_words = 0
for word in word_pos_count:
    total_pos_words += word_pos_count.get(word)
for word in word_occur:
    pos_tf[word] = pos_tf.get(word, 0)
    pos_tf[word] = word_pos_count.get(word, 0) / total_pos_words

neg_tf = {}
total_neg_words = 0
for word in word_neg_count:
    total_neg_words += word_neg_count.get(word)
for word in word_occur:
    neg_tf[word] = neg_tf.get(word, 0)
    neg_tf[word] = word_neg_count.get(word, 0) / total_neg_words

# +++++++++++++++++++++++++++++++++++++计算idf+++++++++++++++++++++++++++
idf = {}
for word in word_occur:
    idf[word] = math.log10((doc_neg_count + doc_neu_count + doc_pos_count) / word_occur.get(word))

# 输出
path = open('result/wight.csv', 'w', encoding='utf-8')
path.write('word\tpos_tf\tneg_tf\tidf\tbdc\tpos_tf_idf\tneg_tf_idf\tpos_tf_bdc\tneg_tf_bdc\n')
for word in word_occur:
    # tf做了乘100000的处理
    path.write('%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n' %
               (word, pos_tf[word]*1e5, neg_tf[word]*1e5, idf[word], bdc[word],
                pos_tf[word]*idf[word]*1e5, neg_tf[word]*idf[word]*1e5,
                pos_tf[word]*bdc[word]*1e5, neg_tf[word]*bdc[word]*1e5))
path.close()
