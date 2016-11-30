import jieba
import re

# 反比句
def getInverseSen(views, line):
    comviews = []
    for view in views:
        s1 = '不如' + view
        if (line.__contains__(s1)):
            comviews.append(view)
    return comviews

# 比较句
def getCompSentence(views, line):
    comviews = []
    for view in views:
        s1 = '与' + view + '相比'
        s2 = '比' + view
        if (line.__contains__(s1)):
            comviews.append(view)
        elif (line.__contains__(s2)):
            comviews.append(view)
    return comviews

def preNormalViews(str):
    #处理产生歧义的词
    lists = ['狗狗Polo', '1.4TEA211', 'Yak Yeti酒店', '别克制', '高尔夫度假酒店', '唐山', '唐僧', '唐太宗', '唐古', '后唐', '唐都', '唐侯', '唐斌',
             '唐唯实', '展唐科技', '唐装', '唐朝', '盛唐改装', '唐河','suv','科技']
    str = replace(str, lists)
    str = str.replace('小夏利', '夏利')
    str = str.replace('小夏朗', '夏朗')
    str = str.replace('比速腾', '速腾')
    str = str.replace('上海通用汽车', '上海通用')
    str = str.replace('进口大众尚酷DSG', '大众尚酷DSG')
    # 处理带有单位的数字
    return str

# 将句子中有歧义的词，带单位的数字删除
def preSpecialViews(str):
    # 处理带有单位的数字
    lists = ['qq群','qq号','@qq']
    str = replace(str, lists)
    pattern = r'\d+[元|万|转|幅|马|款|米|年|多]|\d+rpm|\d+公里|\d+积分|\d+月\d+日|\d+n·m|\d\.\d\t|\d\.\d排量|\d\.\dl|\d+\-\d+'
    for word in re.findall(pattern, str):
        str = str.replace(word, '数量')
    return str

# 加载特殊视角词表
def load_table(source):
    file = open(source, encoding='utf-8').readlines()
    view = []
    for line in file:
        line = line.strip()
        view.append(line)
    return view

def replace(str,lists):
    for word in lists:
        str=str.replace(word,'')
    return str

def load_dict(source):
    path=open(source, encoding='utf-8')
    file=path.readlines()
    path.close()
    view={}
    for line in file:
        line = line.strip()
        view[line]=1
    return view

# 删除不需要的词，将剩余的词转换为list
def word_filter(string,StopWords):
    result=[]
    words = jieba.cut(string)
    for word in words:
        if(StopWords.get(word) is None):
            result.append(word)
    return result

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

def search_features_and_wight(word_list, features_list):
    num_of_features = len(features_list)
    result = [0.] * num_of_features
    for word in word_list:
        if(features_list.get(word)is not None):
            result[features_list[word][0]] += float(features_list[word][1])
    return result

def get_features(dict_name, k):
    # 加载字典
    my_dict = open('data/' + dict_name, encoding='utf-8')
    data = my_dict.readlines()
    my_dict.close()
    features = {}
    count = 0
    for line in data:
        if((count+1)>k):
            break
        l1 = line.strip()
        this_line = l1.split('\t')
        features[this_line[0]]= [count, this_line[1]]
        count += 1
    return features