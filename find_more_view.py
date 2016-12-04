from methods import *
view_list ={}

view_file = open('data/AllViews.csv', encoding='utf-8')
view_data = view_file.readlines()
view_file.close()
for line in view_data:
    l1 = line.strip()
    view_list[l1]=1

#得到合并的视角词,比如大众-奥迪
def getMergeViews(views,view_list,line):
    mergeviews=[]
    for view in views:
        for view2 in views:
            if(view!=view2):
                str=view+'-'+view2
                if(line.__contains__(str)and view_list.get(str)is None):
                    mergeviews.append(str)
    return mergeviews

def getNewViews(views,view_list,word_lists,line):
    pass
result_file = open('data/Test.csv',encoding='utf-8')
test_data=result_file.readlines()
result_file.close()
line_count = 0
NormaleViews=load_table('data/NormalViews.csv')
SpecialViews = load_dict('data/SpecialViews.csv')
#加载停用词表
StopWords = load_dict('data/StopWords.csv')
newviews={}
result=open('data/new_view.csv','w',encoding='utf-8')
for line in test_data:
    line_count += 1
    l1 = line.strip()
    l2 = l1.split('\t')
    if not len(l2) == 2:
        continue
    comment_id = l2[0]
    comment = l2[1]
    # 识别视角
    views=getViews(comment, NormaleViews, SpecialViews)
    pattern = r'[\d*\.\d*|\d+]+tsidsg|[\d*\.\d*|\d+]+tsi|[v|V]\d|[\d*\.\d*|\d+]+连冠|[\d*\.\d*|\d+]+公里|[\d*\.\d*|\d+]+小时|[\d*\.\d*|\d+]+[t|起|万|元|T|款|年|版|台|月|日|周|寸|缸|辆|副|轮|键]+|\d\.\d|\d*:\d*|201\d|\d+km/h'
    lists = ['4s', 'pk', 'performance', '1-', '1,6']
    for word in lists:
        comment = comment.replace(word, '')
    for word in re.findall(pattern, comment):
        comment = comment.replace(word, '')
    for view in views:
        pattern = r'^[0-9a-zA-Z\-]+' + view + '+[0-9a-zA-Z\-]+|' + view + '+[0-9a-zA-Z\-]+[级|系列]*|^[0-9a-zA-Z\-]+' + view + ''
        for word in re.findall(pattern, comment):
            if(newviews.get(word) is None and l2[1].__contains__(word) and view_list.get(word) is None and word.__contains__('-')==False):
                if (len(re.findall('[a-zA-Z]', word)) > 0):
                    result.write(word + '\t' + l2[1] + '\n')
                    newviews[word] = 1
    #for mview in getMergeViews(views,view_list,comment):
        #if(newviews.get(mview)is None):
            #newviews[mview]=1