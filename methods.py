import jieba.posseg


jieba.load_userdict('data/my_dict.csv')
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
dict_file = open('data/my_dict.csv', encoding='utf-8')
dict_data = dict_file.readlines()
dict_file.close()
for i in dict_data:
    i1 = i.strip()
    i2 = i1.split(' ')
    words_that_should_not_be_divided.add(i2[0])
for l in words_that_should_not_be_divided:
    jieba.suggest_freq(l, True)
# 删除不需要的词，将剩余的词转换为list


def word_filter(string):
    result = []                     # 以list装载数据
    words = jieba.posseg.cut(string)
    for word, flag in words:
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

