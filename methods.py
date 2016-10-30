import jieba.posseg


# 删除不需要的词，将剩余的词转换为list
def word_filter(string):
    result = []                     # 以list装载数据
    words = jieba.posseg.cut(string)
    for word, flag in words:
        if 'u' == flag:
            pass
        elif 'x' == flag:
            pass
        elif 'p' == flag:
            pass
        elif 'q' == flag:
            pass
        elif 'm' == flag:
            pass
        elif 'eng' == flag:
            pass
        else:
            result.append(word)
    return result
