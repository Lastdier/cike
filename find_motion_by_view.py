# coding=GBK
"""
根据提供的视角词，分别有View View_1107 new_view这三个文件
提供的情感词，分别有pos_dict.csv neg_dict.csv
根据标点符号把一段话分割成几个小段，每个小段再进行分词，如果该小段内有情感词，则按照这个情感词作为该段内视角的情感，如果没有情感词，则拓展到其他段
例如：
"""
import jieba
jieba.load_userdict('data/View.csv') # file_name为自定义词典的路径
jieba.load_userdict('data/View_1107.csv')
jieba.load_userdict('data/new_view.csv')
jieba.load_userdict('data/pos_dict.csv')
jieba.load_userdict('data/neg_dict.csv')


#加载文件数据
trainTest = open('tempdata/TrainTest.csv','r',encoding='utf8')
trainTestLines = trainTest.readlines()
for line in trainTestLines:
    line = line.strip()
    line = line.split('\t')
    print('编号：', line[0], '----内容：', line[1])

    if(line[1]):
        line[1].strip()
        content = line[1].split('，')
        for x in content:
            seg_list = jieba.cut(x)
            print('分词为：',"/".join(seg_list))



