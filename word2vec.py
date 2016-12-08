from gensim.models import word2vec
import numpy as np

model = word2vec.Word2Vec.load('data/word_vec.model')
weight = open('data/weight.csv', encoding='utf-8')
weight_data = weight.readlines()
weight.close()
weight_dict = {}
for kkk in weight_data:
    l1 = kkk.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    weight_dict[l2[0]] = float(l2[1])

# 输入为分好词的列表
def get_vec(word_list):
    foo = np.array([0.] * 200)                     # 现在使用200维的词向量
    count = 0
    for word in word_list:
        if not weight_dict.get(word) is None:
            vector = np.array(model[word])            # 读取模型中的词向量
            vector *= weight_dict[word]  # 词向量乘以权重
            foo = vector + foo
            count += 1
    if not count == 0:
        foo = foo / count
    result = foo.tolist()
    return result
