import jieba.posseg
import time

# 加载列表
def load_table(source):
    file = open(source, encoding='utf-8').readlines()
    view = []
    for line in file:
        line = line.strip()
        view.append(line)
    return view

def getStopWords(filename,StopName):
    train = open(filename, encoding='utf-8')
    train_data = train.readlines()
    stopWords={}
    for line in train_data:
        line = line.strip()
        line = line.split('\t')
        if not len(line) == 2:
            continue
        comment = line[1]
        words = jieba.posseg.cut(comment)
        for word, flag in words:
            if 'u' in flag:
                stopWords[word]=1
            elif 'p' == flag:
                stopWords[word] = 1
            elif 'q' == flag:
                stopWords[word] = 1
            elif 'm' == flag:
                stopWords[word] = 1
            else:
                pass
    pathName = open(StopName, 'w', encoding='utf-8')
    stopWords = (list(stopWords))
    stopWords.sort(key=lambda x: len(x), reverse=True)
    for view in stopWords:
        pathName.write(view + '\n')

filename='data/Train.csv'
StopName='data/Stopwords.csv'
itime=time.time()
getStopWords(filename,StopName)
etime=time.time()
print('总共用时:'+str(etime-itime))