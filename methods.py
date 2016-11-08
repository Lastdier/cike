import jieba.posseg
import re
jieba.load_userdict('data/NormalViewdict.csv')
words_that_should_not_be_divided = {'召回','自燃','短轴','看上去','EA1111.4T','大帕萨特','B7.5','高尔夫大使','女子高尔夫',
                                    '5000','AS5174','PM2.5',
        '奥迪量产','DL382','中华区','PLA3.0','申联阳光','双龙大道','双龙山森林公园','双龙寺','大众汽车集团',
        '捷豹路虎汽车','EA211','大本田','ESP','特斯拉杀手','1.4TFSI','大众style','小辉腾','EVO150.4','V6发动机',
        'v6发动机','NEX12.2','MC261','200T','变形金刚','小康生活','东风标志','PassatA','媒体大众','350牛米','现代感',
        '标志性','马丁脸','前麦弗逊','现代化','PQ34','EA88','PQ35','荣威新能源','马自达工厂','上海通用工厂',
        '捷克姆拉达','标致大道','大众一家','上海大众汽车','大众赛车','C级车',
        'C级豪华','C级轿跑','C级别','高尔夫运动','别克4S店', '长安', '小夏', '长城', '大切', '凯泽西', '发现四', '大宝',
        '小理', '小四', '小海', '大发', '大奔', '大众', '小八', '拉达', '小七', '小科', '老马', '长马', '汉能', '迷你',
        '起亚'}
dict_file = open('data/NormalViewdict.csv', encoding='utf-8')
dict_data = dict_file.readlines()
dict_file.close()
for i in dict_data:
    i1 = i.strip()
    i2 = i1.split(' ')
    words_that_should_not_be_divided.add(i2[0])
for l in words_that_should_not_be_divided:
    jieba.suggest_freq(l, True)

#将句子中有歧义的词，带单位的数字删除
def preProcess(str):
    #处理带有单位的数字
    pattern=r'\d+[N牛m米马力r元公斤T年万辆月日]|[\[][\S]*[\]]|DQ\d+|\d+-\d+|TSI\d+'
    for word in re.findall(pattern,str):
        str=str.replace(word,'')
    #处理产生歧义的词
    p = r".*(现代.*传统).*|.*(传统.*现代).*|.*(现代.*时尚).*|.*(时尚.*现代).*|.*(现代.*科技).*|.*(科技.*现代).*|.*(音乐.*现代).*|.*(现代.*音乐).*|.*(现代.*经典).*|.*(经典.*现代).*|.*(现代.*绅士).*|.*(绅士.*现代).*|.*(现代.*文明).*|.*(文明.*现代).*|.*(现代.*服务).*|.*(服务.*现代).*.*(现代.*中国).*|.*(中国.*现代).*|.*(现代.*文明).*|.*(文明.*现代).*|.*(现代.*农业).*|.*(农业.*现代).*|.*(现代.*教育).*|.*(教育.*现代).*|.*(现代.*美).*|.*(美.*现代).*|.*(现代.*人).*|.*(人.*现代).*"
    if(len(re.findall(p,str))>0):
        str=str.replace('现代','')
    p = r".*(330.*速派).*|.*(330.*帕萨特).*|.*(帕萨特.*330).*|.*(速派.*330).*"
    if (len(re.findall(p, str)) > 0):
        str = str.replace('330', '')
    #车型词和品牌词一起出现
    p = r".*(上汽大众.途安L).*|.*(途安L.上汽大众).*"
    if (len(re.findall(p, str)) > 0):
        str = str.replace('上汽大众', '')
    lists=['汽车','狗狗Polo','大火中的Polo','1.4TEA211','长安宝宝','迈腾全国猪价资讯','XDS','Cross Lavida','Der Yeti in Berlin','Yak Yeti酒店','别克制','高尔夫度假酒店','','']
    #现代出现了557次，然后有很多会导致歧义！
    xiandai=['现代消费者','更现代','期待现代','现代学徒','现代奥运会','现代企业','现代露天剧场','现代风格','现代化','现代人','现代龙泉青','现代生活','既现代','融入现代','组成现代','现代文化','现代文明','现代交通安全','现代五项队','现代职业教育','现代豪华','现代艺术','现代诗歌','近现代','后现代','现代感','现代天地','现代豪华','现代制药','现代农业','现代都市','现代艺术','现代诗歌','近现代','后现代','现代感','现代天地','现代豪华','现代制药','现代农业','现代都市','回现代']
    #大众出现了300+次，然后有很多会导致歧义！
    dazhong=['大众旅游','大众资讯','大众喜爱','330御尊','长安福特店','30E','H5FF408','280TSI']
    str=replace(str,lists)
    str =replace(str,xiandai)
    str =replace(str,dazhong)
    str=str.replace('全新帕萨特','帕萨特')
    str=str.replace('新帕萨特','帕萨特')
    str = str.replace('小夏利', '夏利')
    str = str.replace('一汽吉林4S店', '一汽')
    str = str.replace('比速腾', '速腾')
    str = str.replace('进口大众尚酷DSG', '大众尚酷DSG')
    return str

#删除同义词
def delete_words(list):
    if ('帕萨特'in list and 'Passat' in list):
        list.remove('Passat')
    if ('帕萨特'in list and '帕萨特B1' in list):
        list.remove('帕萨特')
    if ('上汽大众斯柯达'in list and 'Kodiaq' in list ):
        list.remove('Kodiaq')
    if ('上汽大众斯柯达' in list and '上汽斯柯达' in list):
        list.remove('上汽斯柯达')
    if ('上汽大众斯柯达' in list and '斯柯达' in list):
        list.remove('斯柯达')
    if ('上汽大众途安L' in list and '途安L' in list):
        list.remove('上汽大众途安L')
    return list

#删除句子中会产生歧义的词，比如现代化，可能会被是被为视角词;现代
def replace(str,lists):
    for word in lists:
        if(str.__contains__(word)==True):
            str=str.replace(word,'')
    return str

#j加载特殊视角词表
def load_table(source):
    file=open(source, encoding='utf-8').readlines()
    view=[]
    for line in file:
        line = line.strip()
        view.append(line)
    return view

# 删除不需要的词，将剩余的词转换为list
def word_filter(string):
    result = []                     # 以list装载数据
    string= preProcess(string)
    path = 'data/SpecialView.csv'
    SpecialView = load_table(path)
    # 第一遍先找出特殊的视角词，并且返回不含特殊视角词的句子
    for spcialview in SpecialView:
        if (string.__contains__(spcialview) == True):
            result.append(spcialview)
            string= string.replace(spcialview, '')
    words = jieba.posseg.cut(string)
    for word,flag in words:
        if 'u' in flag:
            pass
        elif 'x' == flag:
            pass
        elif 'p' == flag:
            pass
        elif 'q' == flag:
            pass
        elif 'm' == flag:
            pass
        else:
            result.append(word)
    result = delete_words(result)
    return result

def search_features_and_wight(word_list, features_list):
    num_of_features = len(features_list)
    result = [0.] * num_of_features
    for word in word_list:
        for fea in features_list:
            if fea[0] == word:
                result[features_list.index(fea)] += float(fea[1])
    return result

def get_features(dict_name, k):
    # 加载字典
    my_dict = open('data/' + dict_name, encoding='utf-8')
    data = my_dict.readlines()
    my_dict.close()
    features = []
    count = 1
    for line in data:
        if count > k:
            break
        l1 = line.strip()
        this_line = l1.split('\t')
        features.append([this_line[0], this_line[1]])
        count += 1
    return features
