from sklearn import svm
from sklearn import preprocessing
from create_training_set import *


clf = svm.SVC()
train_x, train_y = create_training_set('neg_dict.csv', 400, 'neg')
normal_x = preprocessing.normalize(train_x)
scaled_x = preprocessing.scale(normal_x)
clf.fit(scaled_x, train_y)


