import jieba
import re
import jieba.posseg
import math
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
    outStr = ''
    for word in list:
        outStr += word
    return outStr

def getPosseg(string,StopWords):
    result=[]
    words = jieba.posseg.cut(string)
    for word,flag in words:
        if(StopWords.get(word) is None):
            result.append((word,flag))
    return result

#删除一些共现的词,比如东风日产和日产同时出现，不用日产
def removeAmbiguous(word,views,list):
    for l in list:
        if(l in views):
            views.remove(word)
            break
    return views

#得到一些歧义视角词，在Views里面没有的
def getAmbiousViews(views,temp_comment):
    ambiguous = ['风光', '标志','阳光','通用']
    for view in ambiguous:
        pattern = r'[跟，、代 —]+'+view+ '+|'+view+ '+[跟，、代 —]+'
        if (len(re.findall(pattern, temp_comment)) > 0):
            views.append(view)
    pattern = r'[跟、代 —]+发现+'
    if (len(re.findall(pattern, temp_comment)) > 0):
        views.append('发现')
    return views

#主要是为了比如北京现代 时尚 同时出现被误判
def removeSpecialViews(views,temp_comment):
    if('道奇挑战者' not in views and '道奇' in temp_comment and '挑战者' in temp_comment):
        views.append('挑战者')
    if('现代' in views):
        p = r'.*(现代.*传统).*|.*(传统.*现代).*|.*(现代.*时尚).*|.*(时尚.*现代).*|.*(现代.*科技).*|.*(科技.*现代).*|.*(音乐.*现代).*|.*(现代.*音乐).*|.*(现代.*经典).*|.*(经典.*现代).*|.*(现代.*绅士).*|.*(绅士.*现代).*|.*(现代.*文明).*|.*(文明.*现代).*|.*(现代.*服务).*|.*(服务.*现代).*.*(现代.*中国).*|.*(中国.*现代).*|.*(现代.*文明).*|.*(文明.*现代).*|.*(现代.*农业).*|.*(农业.*现代).*|.*(现代.*教育).*|.*(教育.*现代).*|.*(现代.*美).*|.*(美.*现代).*|.*(现代.*人).*|.*(人.*现代).*'
        if len(re.findall(p, temp_comment)) > 0:
            views.remove('现代')
    if ('日产' in views):
        richan = ['东风日产', '日产轩逸', '日产奇骏']
        views=removeAmbiguous('日产',views,richan)
    if('大众tiguan' in views and '大众' in views):
        views.remove('大众')
    if ('大众tiguan' in views and 'tiguan' in views):
        views.remove('tiguan')
    if('上汽通用五菱' in views and '五菱' in views):
        views.remove('五菱')
    if ('高尔夫' in views):
        richan = ['大众高尔夫', '大众高尔夫7', '大众一汽高尔夫','别克高尔夫']
        views = removeAmbiguous('高尔夫', views, richan)
    if ('盖世' in views):
        richan = ['比亚迪宋', '比亚迪', '宋']
        views = removeAmbiguous('盖世', views, richan)
    if ('丰田' in views):
        richan = ['丰田卡罗拉', '丰田酷路泽4600','一汽丰田卡罗拉']
        views = removeAmbiguous('丰田', views, richan)
    if ('迈锐宝xl' in views):
        richan = ['雪佛兰迈锐宝xl']
        views = removeAmbiguous('迈锐宝xl', views, richan)
    return views

#处理歧义，比如比速腾，要的是速腾不是比速
def getSpecialV(views,comment):
    Views = ['速腾','速派','夏朗','夏利','帕萨特','众泰']
    for view in Views:
        pattern = r'[小大比]+' + view+'+'
        if (len(re.findall(pattern,comment)) > 0):
            views.append(view)
            comment=comment.replace(view,'')
    return views,comment

#处理含中文的视角词
def preNormalViews(str):
    #处理产生歧义的词
    lists=['东南角','东南越蛇种','东东南','东南边','东南枝','东南倾','东南西北','东南亚','东南地区','薛东南','前麦弗逊','麦弗逊前','捷克姆拉达','Václav',' 200T','狗狗Polo','大火中的Polo','1.4TEA211','长安宝宝','迈腾全国猪价资讯','XDS','Cross Lavida','Der Yeti in Berlin','Yak Yeti酒店','别克制','高尔夫度假酒店','','']
    # 现代出现了557次，然后有很多会导致歧义！
    xiandai = ['地球梦发动机','地球梦科技','现代消费者','更现代','期待现代','现代学徒','现代奥运会','现代企业','现代露天剧场','现代风格','现代化','现代人','现代龙泉青','现代生活','既现代','融入现代','组成现代','现代文化','现代文明','现代交通安全','现代五项队','现代职业教育','现代豪华','现代艺术','现代诗歌','近现代','后现代','现代感','现代天地','现代豪华','现代制药','现代农业','现代都市','现代艺术','现代诗歌','近现代','后现代','现代感','现代天地','现代豪华','现代制药','现代农业','现代都市','回现代']
    # 大众出现了300+次，然后有很多会导致歧义！
    dazhong = ['TSI330','的阳光','C级别','C级豪华','C级全新','C级高端','c级车','C级车','大众旅游','大众资讯','大众喜爱','330御尊','长安福特店','30E','H5FF408','280TSI','DSG','dsg','TSI','现代灵感','现代气息','又现代','现代的活力','现代工业','历史与现代','现代级','现代电影院','现代物流','现代功能','现代医学','现代高端','现代钢琴','现代卫浴','现代科学']
    str = replace(str, lists)
    str = replace(str, xiandai)
    str = replace(str, dazhong)
    str = str.replace('一汽吉林4S店', '一汽')
    lists = ['MLB','ESP','[熊猫]','1.4TEA211', 'Yak Yeti酒店', '别克制', '高尔夫度假酒店', '唐山', '唐僧', '唐太宗', '唐古', '后唐', '唐都', '唐侯', '唐斌',
             '唐唯实', '展唐科技', '唐装', '唐朝', '盛唐改装', '唐河','suv','科技','EA888','大众化','汽车城','dsc','马丁脸','esp','比速度','大中华','中华人民','中华民族','中华元素','中华艺术宫','实现中华','中华商业','中华全国']
    str = replace(str, lists)
    str = str.replace('[起亚律动]', '')
    str = str.replace('变形金刚', '')
    str = str.replace('[Lavida生活]', '')
    str = str.replace('雷克萨斯rx200t', '雷克萨斯rx')
    return str

#处理含中文的视角词
def preSpecialViews(str):
    # 处理带有单位的数字
    lists = ['qq群', 'qq号', '@qq']
    str = replace(str, lists)
    pattern = r'\d+[元|万|转|幅|马|款|米|年|多|人|台|辆|名|公|月]|\d+rpm|\d+公里|\d+mm|\d+积分|\d+月\d+日|\d+n·m|\d\.\d\t|\d\.\d排量|\d\.\dl|\d+\-\d+'
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
    if (len(re.findall('^[0-9]+$', str)) > 0):
        for view in SpecialView:
            if (str.__contains__(view)):
                str = str.replace(view, '')
                views.append(view)
        if (str == '' or str.isdigit()):
            pass
        else:
            views = []
    else:
        for view in SpecialView:
            temp = view
            temp_comment = str.replace(view, '')
            temp += temp_comment
            if (temp == str):
                views.append(view)
                break
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
    if(comment.__contains__('北京汽车') and  not comment.__contains__('北京汽车绅') and not comment.__contains__('北京汽车B')):
        views.append('北京')
    if (comment.__contains__('东南汽车') == False or comment.__contains__('上汽通用汽车别克')==False or comment.__contains__('众泰汽车')==False):
        comment = comment.replace('汽车', '')
    temp_comment = comment
    #得到一些特殊视角词,例如小夏利：小夏 夏利 应该是夏利
    if ('小' in comment or '大' in comment or '比' in comment):
        views,comment = getSpecialV(views,comment)
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
            if (len(re.findall('^[a-zA-Z]+$',word))>0):
                for view in getSpecilaView(word, SpecialViews):
                    views.append(view)
    if('风光' in comment or '标志' in comment or '阳光' in comment or '发现' in comment or '通用'in comment):
        views=getAmbiousViews(views,comment)
    views=removeSpecialViews(views,temp_comment)
    views = list(set(views))
    for view in views:
        if(view not in temp_comment):
            views.remove(view)
    return views

#得到含有视角词的句子以及无视角词的句子
def getSentence(view,views,lines):
    strour = ''
    if(len(views)==1):
        for j in range(0, len(lines)):
            strour+=lines[j]
    else:
        temp = 0
        for j in range(0, len(lines)):
            temp_len = 0
            if (lines[j].__contains__(view)):
                strour += lines[j]
                temp = j
            elif (strour != ''):
                for s in range(0, len(views)):
                    if ((lines[j].__contains__(views[s])) == False):
                        temp_len += 1
                if (temp_len == len(views) and j > temp):
                    strour += lines[j]
                    temp = j
    return strour

#得到按距离切分好的句子，按照两个视角的中点来切分视角，不考虑标点符号
def getAllSentence(views,str):
    x_cache = {}
    if(len(views)==1):
        x_cache[views[0]]=str
    else:
        marker_set = ['☢', '☣', '☤', '☥', '☦', '☧', '☨', '☩', '☪', '☫', '☬', '☭', '☮', '☯', '☰', '*', '＊', '✲', '✿',
                      '❁', '♚', '☸', '♕', '♗', '♝', '♘', '♞', '♖', '♜', '♟', '✈', '〠', '۩', '♨', 'ღ', '✪', '✄',
                      '✁',
                      '☂', '☄', '☇']  # 用来标记视角的占位
        pointer = 0
        cache = {}
        for view in views:
            cache[marker_set[pointer]] = view
            str = str.replace(view, marker_set[pointer])  # 先识别分词器无法区分的视角，再用特殊标记标记出来
            pointer += 1
        StopWords = load_dict('data/StopWords.txt')
        words_list = word_filter(str, StopWords)
        view_index = []  # 找出视角词出现的下标
        foo = 0
        for word in words_list:
            if (cache.get(word) is not None):
                view_index.append(foo)
            foo += 1
        divide_index = []  # 计算出分隔点的下标
        for I in range(len(view_index) - 1):
            divide_index.append(math.ceil((view_index[I] + view_index[I + 1]) / 2))
        # 判断每一段应该是哪个情感，然后统计
        word_cache =''
        words_list_pointer = 0  # 记录处理到评论中的哪个词了
        for I in divide_index:
            while words_list_pointer <= I:
                word_cache+=words_list[words_list_pointer]
                words_list_pointer += 1
            for view in list(cache):
                if view in word_cache:
                    if x_cache.get(view) is None:
                        x_cache[cache[view]] = word_cache
                    else:
                        x_cache[cache[view]] += word_cache
            word_cache =''
        while words_list_pointer < len(words_list):
            word_cache += words_list[words_list_pointer]
            words_list_pointer += 1
        for view in list(cache):
            if view in word_cache:
                if x_cache.get(view) is None:
                    x_cache[cache[view]] = word_cache
                else:
                    x_cache[cache[view]] += word_cache
    return x_cache

#得到视角词对应的按距离切分后得到的句子
def getSenten(x_cache,view):
    return x_cache[view]