#coding:utf-8
import time
from methods import *

def process_data(soucre,NormalViews,SpecialViews,poswords,negwords,pathm):
    fr = open(soucre,encoding='utf-8')
    arrayOfLines = fr.readlines()
    fr.close()
    # 存储输出的数据，格式：句子ID，视角词，情感词
    result_file=open(pathm, 'w', encoding='utf-8')
    StopWords = load_dict('data/StopWords.csv')
    for line in arrayOfLines:
        line = line.strip()
        line = line.split('\t')
        comment=line[1]
        comment_id=line[0]
        views = getViews(comment, NormalViews, SpecialViews)
        views=list(set(views))
        word_list=word_filter(comment,StopWords)
        motion = getMotion(word_list, poswords, negwords)
        for myview in views:
            result_file.write(comment_id+','+myview+','+motion+'\n')
    result_file.close()

def replace(str,lists):
    for word in lists:
        str=str.replace(word,'')
    return str

def getSpecilaView(str,SpecialViews):
    views=[]
    SpecialView=list(SpecialViews)
    SpecialView.sort(key=lambda x: len(x), reverse=True)
    for view in SpecialView:
        if(str.__contains__(view)):
            str=str.replace(view,'')
            views.append(view)
    if(str=='' or str.isdigit()):
        pass
    else:
        views=[]
    return views

def listTostring(list):
    outStr = ' '
    for word in list:
        outStr += word
        outStr += ' '
    return outStr

if __name__ == '__main__':
    path = 'data/pos_dict.csv'
    Motions_pos = load_table(path, 0)
    # 加载负面情感词表
    path = 'data/neg_dict.csv'
    Motions_neg = load_table(path, 0)
    # 加载普通视角词
    path = 'data/NormalViews.csv'
    NormalViews = load_table(path,1)
    # 加载特殊视角词，只含数字/英文
    path = 'data/SpecialViews.csv'
    SpecialViews = load_dict(path)
  #处理测试集
    source='result/Tre.csv'
    pathM = 'data/result.csv'
    iTime=time.time()
    process_data(source,NormalViews,SpecialViews,Motions_pos,Motions_neg,pathM)
    eTime=time.time()
    print("总共用时：" + str(eTime - iTime))