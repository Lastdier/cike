import jieba.posseg
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

view_list = []
result = {''}                 # set
result.remove('')

view_file = open('data/View.csv', encoding='utf-8')
view_data = view_file.readlines()
view_file.close()
for line in view_data:
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    view = l2[1]
    view_list.append(view)

a_view_file = open('data/view_1107.csv', encoding='utf-8')
a_view_data = a_view_file.readlines()
a_view_file.close()
for line in view_data:
    l1 = line.strip()
    view_list.append(l1)


test_file = open('data/Test.csv', encoding='utf-8')
test_data = test_file.readlines()
test_file.close()
for line in test_data:
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    comment = l2[1]
    words_list = jieba.posseg.cut(comment)

    # 自动机
    state = False
    cache = ''
    for word, flag in words_list:
        if not state:
            for view in view_list:
                if word == view:
                    cache = word
                    state = True
        else:
            if flag == 'eng':
                cache = cache + word
                continue
            elif flag == 'x':
                if word == ',':
                    result.add(cache)
                    state = False
                    continue
                elif word == '、':
                    result.add(cache)
                    state = False
                    continue
                elif word == '。':
                    result.add(cache)
                    state = False
                    continue
                elif word == '，':
                    result.add(cache)
                    state = False
                    continue
                elif word == '/':
                    result.add(cache)
                    state = False
                    continue
                elif word == '：':
                    result.add(cache)
                    state = False
                    continue
                elif word == '<':
                    result.add(cache)
                    state = False
                    continue
                elif word == '>':
                    result.add(cache)
                    state = False
                    continue
                elif word == '》':
                    result.add(cache)
                    state = False
                    continue
                else:
                    cache = cache + word
                    continue
            is_view = False
            for view in view_list:
                if word == view:
                    is_view = True
                    break
            if is_view:
                cache = cache + word
            else:
                result.add(cache)
                state = False

new_file = open('result/new_view.csv', 'w', encoding='utf-8')
for view in result:
    new_file.write('%s\n' % view)
new_file.close()
