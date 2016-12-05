# cike_guoshuang

methods 存放所有方法////////
PreProcess 这个主要是做预处理，得到停用词表+情感词典+视角词表///////
create_training_set 根据词典将训练集构造成向量/////////
classificator 训练SVM并预测测试数据/////////
merge 将挑选正面的结果和挑选负面的结果组合/////////
filter_result 这个纯粹是为了提高最后正确率，将Train和Test中相同的找出来，修正Label，
个人有疑问就是机器学习应该两个相同的句子特征向量是一样的，为何还会有不一样的结果？/////////
check_file 检验结果的F1值


