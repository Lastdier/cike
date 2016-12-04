import jieba
import re

# 加载特殊视角词表
def load_table(source,type):
    path=open(source, encoding='utf-8')
    file=path.readlines()
    path.close()
    view=[]
    if(type==1):
        for line in file:
            line = line.strip()
            view.append(line)
    if(type==0):
        for line in file:
            line = line.strip()
            line=line.split('\t')
            view.append(line[0])
    return view

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
        s3 = '超越' + view
        if (line.__contains__(s1)):
            comviews.append(view)
        elif (line.__contains__(s2)):
            comviews.append(view)
        elif (line.__contains__(s3)):
            comviews.append(view)
    return comviews

def listTostring(list):
    outStr = ' '
    for word in list:
        outStr += word
        outStr += ' '
    return outStr

#处理含中文的视角词
def preNormalViews(str):
    #处理产生歧义的词
    p = r".*(现代.*传统).*|.*(传统.*现代).*|.*(现代.*时尚).*|.*(时尚.*现代).*|.*(现代.*科技).*|.*(科技.*现代).*|.*(音乐.*现代).*|.*(现代.*音乐).*|.*(现代.*经典).*|.*(经典.*现代).*|.*(现代.*绅士).*|.*(绅士.*现代).*|.*(现代.*文明).*|.*(文明.*现代).*|.*(现代.*服务).*|.*(服务.*现代).*.*(现代.*中国).*|.*(中国.*现代).*|.*(现代.*文明).*|.*(文明.*现代).*|.*(现代.*农业).*|.*(农业.*现代).*|.*(现代.*教育).*|.*(教育.*现代).*|.*(现代.*美).*|.*(美.*现代).*|.*(现代.*人).*|.*(人.*现代).*"
    if len(re.findall(p, str)) > 0:
        str = str.replace('现代', '')
    lists=['汽车','狗狗Polo','大火中的Polo','1.4TEA211','长安宝宝','迈腾全国猪价资讯','XDS','Cross Lavida','Der Yeti in Berlin','Yak Yeti酒店','别克制','高尔夫度假酒店','','']
    # 现代出现了557次，然后有很多会导致歧义！
    xiandai = ['现代消费者','更现代','期待现代','现代学徒','现代奥运会','现代企业','现代露天剧场','现代风格','现代化','现代人','现代龙泉青','现代生活','既现代','融入现代','组成现代','现代文化','现代文明','现代交通安全','现代五项队','现代职业教育','现代豪华','现代艺术','现代诗歌','近现代','后现代','现代感','现代天地','现代豪华','现代制药','现代农业','现代都市','现代艺术','现代诗歌','近现代','后现代','现代感','现代天地','现代豪华','现代制药','现代农业','现代都市','回现代']
    # 大众出现了300+次，然后有很多会导致歧义！
    dazhong = ['大众旅游','大众资讯','大众喜爱','330御尊','长安福特店','30E','H5FF408','280TSI']
    str = replace(str, lists)
    str = replace(str, xiandai)
    str = replace(str, dazhong)
    str = str.replace('一汽吉林4S店', '一汽')
    str = str.replace('比速腾', '速腾')
    lists = ['1.4TEA211', 'Yak Yeti酒店', '别克制', '高尔夫度假酒店', '唐山', '唐僧', '唐太宗', '唐古', '后唐', '唐都', '唐侯', '唐斌',
             '唐唯实', '展唐科技', '唐装', '唐朝', '盛唐改装', '唐河','suv','科技']
    str = replace(str, lists)
    str = str.replace('小夏利', '夏利')
    str = str.replace('小夏朗', '夏朗')
    str = str.replace('比速腾', '速腾')
    str = str.replace('大众泰', '众泰')
    str = str.replace('上海通用汽车', '上海通用')
    str = str.replace('进口大众尚酷DSG', '大众尚酷DSG')
    str = str.replace('[起亚律动]', '')
    str = str.replace('变形金刚', '')
    str = str.replace('雷克萨斯rx200t', '雷克萨斯rx')
    return str

#处理含中文的视角词
def preSpecialViews(str):
    # 处理带有单位的数字
    lists = ['qq群', 'qq号', '@qq']
    str = replace(str, lists)
    pattern = r'\d+[元|万|转|幅|马|款|米|年|多|人|台|辆|名|公|月]|\d+rpm|\d+公里|\d+积分|\d+月\d+日|\d+n·m|\d\.\d\t|\d\.\d排量|\d\.\dl|\d+\-\d+'
    for word in re.findall(pattern, str):
        str = str.replace(word, '数量')
    return str

def getMotion(result,pos,neg):
    count=0
    for word in result:
        if(word in pos):
            count+=1
        if(word in neg):
            count-=1
    motionValue='neu'
    if(count>0):
        motionValue='pos'
    elif(count<0):
        motionValue='neg'
    return motionValue

#去除不要的词
def replace(str,lists):
    for word in lists:
        str=str.replace(word,'')
    return str

#加载字典
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

#得到合并的视角词,比如:a4q5D3
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

# 加载字典
def get_features(dict_name, k):
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
        features[this_line[0]]= [count,this_line[1]]
        count += 1
    return features

#得到句子中的所有视角词
def getViews(comment,NormaleViews,SpecialViews):
    views = []
    # 处理中文的歧义视角
    comment = preNormalViews(comment)
    # 找出普通视角词
    for view in NormaleViews:
        if (comment.__contains__(view) == True):
            views.append(view)
            comment = comment.replace(view, '')
    # 处理含数字的歧义视角
    comment=preSpecialViews(comment)
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
    return views

#得到含有视角词的句子以及无视角词的句子
def getSentence(view,views,lines):
    strour = ''
    temp = 0
    for j in range(0, len(lines)):
        temp_len = 0
        if (lines[j].__contains__(view)):
            strour += lines[j]
            temp = j
        elif (strour!= ''):
            for s in range(0, len(views)):
                if ((lines[j].__contains__(views[s])) == False):
                    temp_len += 1
            if (temp_len == len(views) and j > temp):
                strour += lines[j]
                temp = j
    return strour