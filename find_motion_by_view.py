# coding=GBK
"""
�����ṩ���ӽǴʣ��ֱ���View View_1107 new_view�������ļ�
�ṩ����дʣ��ֱ���pos_dict.csv neg_dict.csv
���ݱ����Ű�һ�λ��ָ�ɼ���С�Σ�ÿ��С���ٽ��зִʣ������С��������дʣ����������д���Ϊ�ö����ӽǵ���У����û����дʣ�����չ��������
���磺
"""
import jieba
jieba.load_userdict('data/View.csv') # file_nameΪ�Զ���ʵ��·��
jieba.load_userdict('data/View_1107.csv')
jieba.load_userdict('data/new_view.csv')
jieba.load_userdict('data/pos_dict.csv')
jieba.load_userdict('data/neg_dict.csv')


#�����ļ�����
trainTest = open('tempdata/TrainTest.csv','r',encoding='utf8')
trainTestLines = trainTest.readlines()
for line in trainTestLines:
    line = line.strip()
    line = line.split('\t')
    print('��ţ�', line[0], '----���ݣ�', line[1])

    if(line[1]):
        line[1].strip()
        content = line[1].split('��')
        for x in content:
            seg_list = jieba.cut(x)
            print('�ִ�Ϊ��',"/".join(seg_list))



