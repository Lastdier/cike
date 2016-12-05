#getStopWords.py 得到停用词表
#getDict.py 做特征提取,得到情感词典
#getView.py 做视角提取,得到视角词表
from methods import *
import math
import re
import jieba.posseg
import time
from snownlp import SnowNLP

#得到一个完整的基础视角词表,输入是AllViews:由两个Label.csv中获取的视角词+拓展的视角词组成，输出是所有视角词组成的字典
def getFirstView(labelname):
    # 存储从Label.csv中获得的视角词
    views={}
    lists=['208','335','560','630','730','3008','5008']
    for word in lists:
        views[word]=1
    #获取Label中的视角词
    label_file = open(labelname, encoding='utf-8')
    label_data = label_file.readlines()
    label_file.close()
    for line in label_data:
        line = line.strip()
        content=line
        zhPattern1 = re.compile(u'[\u4e00-\u9fa5]+')
        match1 = zhPattern1.search(content)
        if match1:
            #包含中文的视角词不可拆,为视角词拓展做准备
            jieba.suggest_freq(content, True)
        if(content.isdigit()==False):
            views[content]=1
    return views

#删除一些拓展出来的视角词，主要针对英文，比如拓展的视角词为:k2k3k4，但是实际上k2、k3、k4本身是视角词，所以k2k3k4属于误判
def removewSpecilaView(str,SpecialViews):
    temp=str
    SpecialView=list(SpecialViews)
    SpecialView.sort(key=lambda x: len(x), reverse=True)
    for view in SpecialView:
        if(str.__contains__(view)):
            str=str.replace(view,'')
    if(str==''):
        temp=str
    return temp

#根据现有的视角词后面出现英文，数字，-,·来扩展视角词
#基本拓展完毕，除了视角词纯粹是英文/数字的还没有做，其他的完成了。目前的功能就只是把一些不要的视角词删了，然后输出到Views.csv
def getSecondView(views,testname,ViewPathname):
    newviews = {}
    View_First = open(ViewPathname, 'w', encoding='utf-8')
    '''
    label_file = open(testname,encoding='utf-8')
    label_data = label_file.readlines()
    label_file.close()
    for line in label_data:
        line = line.strip()
        line = line.split('\t')
        content = line[1]
        temp = 0
        count = 0
        newview = ''
        # 视角词在最后会提取不到，加。
        content = content + '。'
        pattern = r'\d+[款|年|版|台|月|日|周|寸|缸|辆|副|轮|键|T]|\d+:\d+|\d\.\d|\d+连冠|\d+公里|\d+小时|http:\s+|201\d|\d+km/h|[\d+|\d+.\d+|.\d+]+[t|起|万|元]'
        lists = ['4s', 'pk', 'performance', '1-','1,6']
        for word in lists:
            content = content.replace(word, '')
        for word in re.findall(pattern, content):
            content = content.replace(word, '')
        for word in jieba.cut(content):
            count += 1
            if (views.get(word) is not None):
                if (newview == ''):
                    temp = count
                    newview = word
                    continue
            else:
                if (newview != '') and (count - temp) == 1:
                    if re.match('^[0-9a-zA-Z]+$', word):
                        word = removewSpecilaView(word, views)
                    if (re.match('^[0-9a-zA-Z]+$', word) and word.isdigit()==False) or word == '-' or word == '系' or word == '·' or word == ' ' or word=='－' or word=='\0xa':
                        temp = count
                        newview += word
                    else:
                        if re.match('^[\w]+[-|·]+$', newview):
                            newview = newview.replace('-', '')
                        if re.match('^[\w]+[·]+$', newview):
                            newview = newview.replace('·', '')
                        if re.match('^[\w]+[ ]+$', newview):
                            newview = newview.replace(' ', '')
                        newview = newview.replace('http', '')
                        if (views.get(newview) is None and newviews.get(newview) is None and newview.isdigit() == False and newview.isalpha() == False):
                            newviews[newview] = 1
                            if(newview.__contains__('-') or newview.__contains__('·') or newview.__contains__(' ') or newview.__contains__('\0xa')):
                                #View_First.write(newview + '\n')
                                 #views[newview] = 1
                                 print(newview)
                                 newview = ''
    '''
    #去除重复的视角词
    views=list(set(list(views)))
    #列表按长度降序排序
    views.sort(key=lambda x:len(x),reverse=True)
    for view in views:
        if(view!='发现' and view!='阳光' and view !='标志' and view!='雷凌双擎'):
            View_First.write(view+'\n')

#根据视角词表是否会被jeiba切开分为NormalViws：会被切开+SpecilaViews:不会被切开
def SegViews(ViewPathname,NormalName,SpecialName,):
    normalview=open(NormalName,'w',encoding='utf-8')
    specialview = open(SpecialName, 'w', encoding='utf-8')
    label_file = open(ViewPathname, encoding='utf-8')
    label_data = label_file.readlines()
    label_file.close()
    for line in label_data:
        l1 = line.strip()
        if((l1.__contains__('-') or l1=='ｍｋ１'  or l1.__contains__('\xa0') or l1.__contains__(' '))):
            normalview.write(l1 + '\n')
            continue
        #是否有中文
        zhPattern1 = re.compile(u'[\u4e00-\u9fa5]+')
        match1 = zhPattern1.search(l1)
        if match1:
            normalview.write(l1 + '\n')
        else:
            specialview.write(l1 + '\n')
    normalview.close()
    specialview.close()

def getDict(trainname,labelname,stopWords,pospath,negpath):
    word_neg_count = {}  # 每个词在负面中出现的次数
    word_pos_count = {}  # 每个词在正面中出现的次数
    word_neu_count = {}  # 每个词在中性中出现的次数
    word_occur = {}  # 每个词在多少个文本中出现，用于计算idf
    doc_pos_count, doc_neg_count, doc_neu_count = 0, 0, 0  # 文本的情感频数
    label_ref = {}  # 字典保存label
    views = {}  # 记录出现过的视角词
    # 读取训练集输出
    label = open(labelname, encoding='utf-8')
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
        views[label_view] = 1
        if label_ref.get(label_id) is None:
            label_ref[label_id] = [[label_view, label_emotion]]
        else:
            label_ref[label_id].append(
                [label_view, label_emotion])  # label_ref[id][视角][0]是视角名称，label_ref[id][视角][1]是判断结果

    # 读取训练集输入
    train = open(trainname, encoding='utf-8')
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
        if label_ref.get(comment_id) is None:
            continue
        else:
            view_list = label_ref[comment_id]
        view_count = len(view_list)  # 读取视角数
        lines = re.split('。|,|，|:|：|；|\n', comment)
        dict = {}
        for view, motion in view_list:
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
                    for s in range(0, view_count):
                        if ((lines[j].__contains__(view_list[s][0])) == False):
                            temp_len += 1
                    if (temp_len == view_count and j > temp):
                        strour += lines[j]
                        dict[view] = strour
                        temp = j
            dict[view] = dict[view].replace(view, '')
            words_list = word_filter(dict[view],stopWords)
            if motion == 'pos':
                for word in words_list:
                    word_pos_count[word] = word_pos_count.get(word, 0) + 1
                    word_occur[word] = word_occur.get(word, 0) + 1
                doc_pos_count += 1
            if motion == 'neg':
                for word in words_list:
                    word_neg_count[word] = word_neg_count.get(word, 0) + 1
                    word_occur[word] = word_occur.get(word, 0) + 1
                doc_neg_count += 1
            if motion == 'neu':
                for word in words_list:
                    word_neu_count[word] = word_neu_count.get(word, 0) + 1
                    word_occur[word] = word_occur.get(word, 0) + 1
                doc_neu_count += 1
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
    '''
    idf = {}
    for word in word_occur:
        idf[word] = math.log10((doc_neg_count + doc_neu_count + doc_pos_count) / word_occur.get(word))
    '''
    # ++++++++++++++++++++++++++++计算wc+++++++++++++++++++++++
    word_pos_w = {}
    word_neg_w = {}
    word_neu_w = {}
    for word in word_occur:
        word_pos_count[word] = word_pos_count.get(word, 0)
        word_neg_count[word] = word_neg_count.get(word, 0)
        word_neu_count[word] = word_neu_count.get(word, 0)
        word_count = word_pos_count.get(word, 0) + word_neg_count.get(word, 0) + word_neu_count.get(word, 0)
        word_pos_w[word] = word_pos_count.get(word, 0) / word_count
        word_neg_w[word] = word_neg_count.get(word, 0) / word_count
        word_neu_w[word] = word_neu_count.get(word, 0) / word_count

    # 直接输出wc按数值排序不为0的
    pos_wc = []
    neg_wc = []
    pos = open(pospath, 'w', encoding='utf-8')
    neg = open(negpath, 'w', encoding='utf-8')
    for word in word_occur:
        # 去除视角词,去除停用词表,然后只要有中文的
        if (views.get(word) is not None or re.match('^[\u4e00-\u9fa5]+$', word) == None):
            continue
        if (word_pos_w[word] > 0):
            pos_wc.append((word, word_pos_w[word]))
        if (word_neg_w[word] > 0):
            neg_wc.append((word, word_neg_w[word]))
    pos_wc.sort(key=lambda x: x[1], reverse=True)
    neg_wc.sort(key=lambda x: x[1], reverse=True)
    for word, weighting in pos_wc:
        pos.write('%s\t%.2f\n' % (word, weighting))
    for word, weighting in neg_wc:
        neg.write('%s\t%.2f\n' % (word, weighting))

#得到停用词表
def getStopWords(filename,StopName,NormaleViews,SpecialViews):
    train = open(filename, encoding='utf-8')
    train_data = train.readlines()
    stopWords={}
    pathName = open(StopName, 'w', encoding='utf-8')
    ImportangWords = {}
    important_words = ['ssss', 'fashion', 'dreamcar']
    for word in important_words:
        ImportangWords[word]=1
    for line in train_data:
        line = line.strip()
        line = line.split('\t')
        if not len(line) == 2:
            continue
        comment = line[1]
        views = getViews(comment, NormaleViews, SpecialViews)
        for view in views:
            comment=comment.replace(view,'')
        words = jieba.posseg.cut(comment)
        for word,flag in words:
            #不要的;x u p q m p
            if(stopWords.get(word) is None and (flag=='m' or flag=='x' or flag=='p' or flag=='q' or flag=='u' or re.match('^[0-9a-zA-Z]+$',word))):
                stopWords[word]=1
                if (ImportangWords.get(word) is None):
                    pathName.write(word + '\n')

#利用snownlp,得到数据集中每个句子的情感为积极的概率，输出文件格式为：句子ID+句子情感为积极的概率
def get_SentenceSentiment(filename,pathname):
    label_file = open(filename, encoding='utf-8')
    label_data = label_file.readlines()
    label_file.close()
    result = open(pathname, 'w', encoding='utf-8')
    for line in label_data:
        line = line.strip()
        line = line.split('\t')
        s = SnowNLP(line[1])
        result.write('%s\t%.8f\n' % (line[0], s.sentiments))

#得到情感词典
NormaleViews=load_table('data/NormalViews.csv',1)
SpecialViews = load_dict('data/SpecialViews.csv')
#输入的文件名称
trainname='data/Train.csv'
labelname='data/Label.csv'
testname='data/Test.csv'
#输出的停用词表的文件名称
StopName='data/Test_Stopwords.csv'
#输出的情感词典的文件名称
pospath='data/pos_dict.csv'
negpath='data/neg_dict.csv'
#各种视角词文件名称
Allviews='data/AllViews.csv'
ViewPathname='data/Views.csv'
NormalName='data/NormalViews.csv'
SpecialName='data/SpecialViews.csv'
#句子的情感概率值文件名称
SentenceName='data/TrainSentiment.csv'
#主要是得到视角词，输入是AllViews,输出是Views+SpecialViews+NormalViews
iTime=time.time()
#views=getFirstView(Allviews)
eTime=time.time()
print("得到基础视角表总共用时：" + str(eTime - iTime))
iTime=time.time()
#getSecondView(views,testname,ViewPathname)
eTime=time.time()
print("得到总视角表总共用时：" + str(eTime - iTime))
iTime=time.time()
#SegViews(ViewPathname,NormalName,SpecialName,)
eTime=time.time()
print("拆分总视角表总共用时：" + str(eTime - iTime))
#得到停用词表，输入是数据集+SpecialViews+NormalViews，输入是StopWords.csv
itime=time.time()
#getStopWords(trainname,StopName,NormaleViews,SpecialViews)
etime=time.time()
print('得到停用词表总共用时:'+str(etime-itime))
#得到情感词典，输入是文件名称+停用词表，输出是积极情感词典+消极情感词典
stopWords = load_dict(StopName)
itime=time.time()
getDict(trainname,labelname,stopWords,pospath,negpath)
etime=time.time()
print('得到情感词典总共用时:'+str(etime-itime))
iTime=time.time()
#get_SentenceSentiment(trainname,SentenceName)
eTime=time.time()
print("得到句子的情感概率值总共用时：" + str(eTime - iTime))