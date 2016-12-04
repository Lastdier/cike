'''
#根据现有的视角词后面出现英文，数字，-,·来扩展视角词
def getSecondView(views,testname,ViewPathname):
    newviews = {}
    View_First = open(ViewPathname, 'w', encoding='utf-8')
    '''
    label_file = open(testname,encoding='utf-8')
    label_data = label_file.readlines()
    label_file.close()
    for line in label_data:
        line = line.strip()
        line = line.split('\t')
        content = line[1]
        temp = 0
        count = 0
        newview = ''
        # 视角词在最后会提取不到，加。
        content = content + '。'
        pattern = r'\d+[款|年|版|台|月|日|周|寸|缸|辆|副|轮|键|T]|\d+:\d+|\d\.\d|\d+连冠|\d+公里|\d+小时|http:\s+|201\d|\d+km/h|[\d+|\d+.\d+|.\d+]+[t|起|万|元]'
        lists = ['4s', 'pk', 'performance', '1-','1,6']
        for word in lists:
            content = content.replace(word, '')
        for word in re.findall(pattern, content):
            content = content.replace(word, '')
        for word in jieba.cut(content):
            count += 1
            if (views.get(word) is not None):
                if (newview == ''):
                    temp = count
                    newview = word
                    continue
            else:
                if (newview != '') and (count - temp) == 1:
                    if re.match('^[0-9a-zA-Z]+$', word):
                        word = removewSpecilaView(word, views)
                    if (re.match('^[0-9a-zA-Z]+$', word) and word.isdigit()==False) or word == '-' or word == '系' or word == '·' or word == ' ' or word=='－' or word=='\0xa':
                        temp = count
                        newview += word
                    else:
                        if re.match('^[\w]+[-|·]+$', newview):
                            newview = newview.replace('-', '')
                        if re.match('^[\w]+[·]+$', newview):
                            newview = newview.replace('·', '')
                        if re.match('^[\w]+[ ]+$', newview):
                            newview = newview.replace(' ', '')
                        newview = newview.replace('http', '')
                        if (views.get(newview) is None and newviews.get(newview) is None and newview.isdigit() == False and newview.isalpha() == False):
                            newviews[newview] = 1
                            if(newview.__contains__('-') or newview.__contains__('·') or newview.__contains__(' ') or newview.__contains__('\0xa')):
                                #View_First.write(newview + '\n')
                                 #views[newview] = 1
                                 print(newview)
                                 newview = ''
    views=list(set(list(views)))
    views.sort(key=lambda x:len(x),reverse=True)
    for view in views:
        if(view!='发现' and view!='阳光' and view !='标志' and view!='雷凌双擎'):
            View_First.write(view+'\n')
label_file = open('data/Train.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
pos={}
import re
result = open('data/getDict.csv','w' ,encoding='utf-8')
for line in label_data:
    l1 = line.strip()
    line=line.split('\t')
    if line[1].__contains__('车型：'):
        pos[line[0]]=line[1]
label_file = open('data/Label.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
id={}
for line in label_data:
    line=line.strip()
    line=line.split('\t')
    if (pos.get(line[0]) is not None):
        result.write(line[0] + '\t' +line[2]+'\t'+pos[line[0]])
from sklearn.ensemble import GradientBoostingClassifier
# !usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
from sklearn import metrics
import numpy as np
import Pickle as pickle
import importlib,sys
importlib.reload(sys)
sys.setdefaultencoding('utf8')

# Multinomial Naive Bayes Classifier
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model


# KNN Classifier
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# SVM Classifier
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model


# SVM Classifier using cross validation
def svm_cross_validation(train_x, train_y):
    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs=1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in best_parameters.items():
        print(para, val)
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model


def read_data(data_file):
    import gzip
    f = gzip.open(data_file, "rb")
    train, val, test = pickle.load(f)
    f.close()
    train_x = train[0]
    train_y = train[1]
    test_x = test[0]
    test_y = test[1]
    return train_x, train_y, test_x, test_y


if __name__ == '__main__':
    data_file = "mnist.pkl.gz"
    thresh = 0.5
    model_save_file = None
    model_save = {}

    test_classifiers = ['NB', 'KNN', 'LR', 'RF', 'DT', 'SVM', 'GBDT']
    classifiers = {'NB': naive_bayes_classifier,
                   'KNN': knn_classifier,
                   'LR': logistic_regression_classifier,
                   'RF': random_forest_classifier,
                   'DT': decision_tree_classifier,
                   'SVM': svm_classifier,
                   'SVMCV': svm_cross_validation,
                   'GBDT': gradient_boosting_classifier
                   }

    print('reading training and testing data...')
    train_x, train_y, test_x, test_y = read_data(data_file)
    num_train, num_feat = train_x.shape
    num_test, num_feat = test_x.shape
    is_binary_class = (len(np.unique(train_y)) == 2)
    print('******************** Data Info *********************')
    print('#training data: %d, #testing_data: %d, dimension: %d' % (num_train, num_test, num_feat))

    for classifier in test_classifiers:
        print('******************* %s ********************' % classifier)
        start_time = time.time()
        model = classifiers[classifier](train_x, train_y)
        print('training took %fs!' % (time.time() - start_time))
        predict = model.predict(test_x)
        if model_save_file != None:
            model_save[classifier] = model
        if is_binary_class:
            precision = metrics.precision_score(test_y, predict)
            recall = metrics.recall_score(test_y, predict)
            print('precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))
        accuracy = metrics.accuracy_score(test_y, predict)
        print('accuracy: %.2f%%' % (100 * accuracy))

    if model_save_file != None:
        pickle.dump(model_save, open(model_save_file, 'wb'))
'''
from snownlp import SnowNLP
label_file = open('data/Train.csv', encoding='utf-8')
label_data = label_file.readlines()
label_file.close()
pos={}
result = open('data/TrainSentiment.csv','w' ,encoding='utf-8')
for line in label_data:
    l1 = line.strip()
    line=line.split('\t')
    s=SnowNLP(line[1])
    result.write('%s\t%.8f\n' % (line[1],s.sentiments))
