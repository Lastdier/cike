check_data = {}                                                   # 存储标签表（正确答案）
comment_views_checked = {}                                         # 存储已经找到的视角数（用于计算漏判）
Train_data = {}
Label_data = {}
Train_result_data={}
views={}
from methods import *
zhaodanshijiao={}
tp, fp, fn1, fn2 = 0, 0, 0, 0
label_file = open('data/Label.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
StopWords = load_dict('data/StopWords.csv')
flag=False
temp_id=0
for line in label_data:
    temp=''
    l1 = line.strip()
    content = l1.split('\t')
    if not len(content) == 3:
        continue
    comment_id = content[0]
    zhaodanshijiao[comment_id]=zhaodanshijiao.get(comment_id,0)+1
    comment_view = content[1]
    views[comment_view]=1
    view_emotion = content[2]
    if check_data.get(comment_id) is None:
        check_data[comment_id] = {comment_view: view_emotion}
        Label_data[comment_id] = comment_view
    else:
        check_data[comment_id][comment_view] = view_emotion
        Label_data[comment_id]+=' '
        Label_data[comment_id]+=comment_view
    comment_views_checked[comment_id] = comment_views_checked.get(comment_id, 0) + 1

train_file = open('data/Train.csv', encoding='utf-8')
train_data = train_file.readlines()
train_file.close()
for line in train_data:
    l1 = line.strip()
    content = l1.split('\t')
    if not len(content) == 2:
        continue
    comment_id = content[0]
    comment_content = content[1]
    Train_data[comment_id]=comment_content

wrong_data = open('result/id_wrong.csv','w', encoding='utf-8')
result_file = open('result/result.csv', encoding='utf-8')
result_data = result_file.readlines()
result_file.close()
for line in result_data:
    l1 = line.strip()
    content = l1.split(',')
    if not len(content) == 3:
        continue
    comment_id = content[0]
    comment_view = content[1]
    view_emotion = content[2]
    if Train_result_data.get(comment_id) is None:
        Train_result_data[comment_id] = comment_view
    else:
        Train_result_data[comment_id]+=' '
        Train_result_data[comment_id]+=comment_view
    if check_data.get(comment_id) is None:
        fn2 += 1
        continue
    if check_data.get(comment_id).get(comment_view) is None:
        fn2+=1
        '''
        wrong_data.write(comment_id + ' 多判视角为：' +comment_view+' 实际视角为：'+ Label_data[comment_id]+' 句子：'+Train_data[comment_id] + '\n')
       '''
        continue
    if view_emotion == check_data[comment_id][comment_view]:
        tp += 1
    else:
        fp += 1
        #if (Train_data[comment_id].__contains__('然而') or Train_data[comment_id].__contains__('但是')):
        #if(view_emotion=='pos' and check_data[comment_id][comment_view]=='neu' ):
            #word_list = word_filter(Train_data[comment_id], StopWords)
            #wrong_data.write(Train_data[comment_id] +' 分词结果'+listTostring(word_list) +'\n')
            #wrong_data.write(comment_id+'\t' + '实际情感:'+check_data[comment_id][comment_view]+' 预测情感:'+view_emotion+'\t'+Train_data[comment_id] + '\n')
    comment_views_checked[comment_id] -= 1

for comment_id in comment_views_checked:
    if(comment_views_checked[comment_id] !=0 and Train_result_data.get(comment_id) is not None):
        pass
        #wrong_data.write(comment_id + ' 实际视角为：' +Label_data[comment_id] + ' 预测视角为：'+Train_result_data[comment_id]+ ' 句子：' + Train_data[comment_id] + '\n')
    elif (comment_views_checked[comment_id] != 0 and Train_result_data.get(comment_id) is None):
        pass;
        #wrong_data.write(comment_id + ' 实际视角为：' + Label_data[comment_id]+ ' 句子：' +Train_data[comment_id] + '\n')
    fn1 += comment_views_checked[comment_id]

print('正确的情感分析数：'+str(tp))
print('错误的情感分析数：'+str(fp))
print('漏判的视角数：'+str(fn1))
print('无效(多判)的视角数：'+str(fn2))
p=tp/(tp+fp+fn2)
r=tp/(tp+fn1)
f1=2*p*r/(p+r)
print('准确率是：'+str(p*100)+'%')
print('召回率是：'+str(r*100)+'%')
print('F1是：'+str(f1*100)+'%')

'''
线上:0.59126 机器学习+修改特权权重方法为:cw
不要那些自己加的什么 neg neu
正确的情感分析数：17038
错误的情感分析数：3044
漏判的视角数：534
无效(多判)的视角数：1666
准确率是：78.34283612286187%
召回率是：96.9610744366037%
F1是：86.66327568667344%

'''