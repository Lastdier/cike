# 把train的stopword和test的stopword组合
stop_word = {''}
stop_word.remove('')

test = open('data/Test_Stopwords.csv', encoding='utf-8')
test_data = test.readlines()
test.close()
for line in test_data:
    l1 = line.strip()
    stop_word.add(l1)

train = open('data/Stopwords.csv', encoding='utf-8')
train_data = train.readlines()
train.close()
for line in train_data:
    l1 = line.strip()
    stop_word.add(l1)

output = open('result/Stopwords.txt', 'w', encoding='utf-8')
for word in stop_word:
    output.write(word + '\n')
output.close()
