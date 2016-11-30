# cike_guoshuang

wighting 生成权重////////
filter 过滤掉权重词典中的视角词///////
convert_dict 将Excel输出的csv转换成utf-8///////
create_training_set 根据词典将训练集构造成向量/////////
classificator 训练SVM并预测测试数据/////////
merge 将挑选正面的结果和挑选负面的结果组合/////////
check_file 检验结果的F1值

修改:
1.methods.py,更换为存储其他.py用到的方法
2.creat_trainning_set.py,更换为按照,.;?等切分句子,视角词所在的分句的情感词+无视角的句子所在的情感词作为视角词的情感词
3.classificator.py修改为直接判断句子中所有的视角词,然后判断每个视角词的情感,先分为对比句,反比句,疑问句
4.删除Label_Test.csv,直接在check_file.py那里设置测试样本有多少行
新增:
1.getStopWords.py,按照词性得到p,q,m,u,作为停用词表(感觉这个可能不需要了)
2.getView.py,之前的所有的视角词作为基础视角词表,按照后缀是英文/数字等拓展
待做:
1.合并wighting.py+filter.py+convert_dict.py直接从weighting从抽取出特征,得到情感词典
2.将规则和机器学习结合在一起,问题是样本要怎么分?
3.测试了不同的视角词,基于规则的方法,结果从0.45-0.54不等,接下来寻找拓展视角词的办法,讲find_more_view.py完善




