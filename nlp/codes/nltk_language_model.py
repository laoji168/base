# coding=utf-8
"""
统计语言建模
2.1 理解单词频率
"""
def fun_2_1():
    from nltk.util import ngrams
    from nltk.corpus import alpino

    # Unigram (一元语法)代表单个标识符。以下代码用于为 Alpino 语料库生成 unigrams
    print alpino.words()
    unigrams = ngrams(alpino.words(), 1)
    for i in unigrams:
        # print i
        pass

    # 考虑另一个有关从 alpino 语料库生成 quadgrams 或 fourgrams (四元语法)的例子
    unigrams = ngrams(alpino.words(), 4)
    for i in unigrams:
        # print i
        pass

    # bigram(二元语法)指的是一对标识符。为了在文本中找到 bigrams,首先需要搜索
    # 小写单词,把文本创建为小写单词列表后,然后创建 BigramCollocationFinder 实例。
    # 在 nltk.metrics 包中找到的 BigramAssocMeasures 可用于在文本中查找 bigrams
    from nltk.collocations import BigramCollocationFinder
    from nltk.corpus import webtext
    from nltk.metrics import BigramAssocMeasures
    tokens = [t.lower() for t in webtext.words('grail.txt')]
    words = BigramCollocationFinder.from_words(tokens)
    print words.nbest(BigramAssocMeasures.likelihood_ratio, 10)

    # 在上面的代码中,我们可以添加一个用来消除停止词和标点符号的单词过滤器
    from nltk.corpus import stopwords
    set1 = set(stopwords.words('english'))
    stops_filter = lambda w: len(w) < 3 or w in set1
    words.apply_word_filter(stops_filter)
    print words.nbest(BigramAssocMeasures.likelihood_ratio, 10)

    # 这里,我们可以将 bigrams 的频率更改为其他数字。
    # 另一种从文本中生成 bigrams 的方法是使用词汇搭配查找器,如下代码所示
    import nltk
    text1 = "Hardwork is the key to success. Never give up!"
    word = nltk.tokenize.wordpunct_tokenize(text1)
    finder = BigramCollocationFinder.from_words(word)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    value = finder.score_ngrams(bigram_measures.raw_freq)
    print sorted(bigram for bigram, score in value)

    # 为了生成 fourgrams 并生成 fourgrams 的频率,可以使用如下代码
    text = "Hello how are you doing ? I hope you find the book interesting"
    tokens = nltk.wordpunct_tokenize(text)
    fourgrams = nltk.collocations.QuadgramCollocationFinder.from_words(tokens)
    for fourgram, freq in fourgrams.ngram_fd.items():
        print (fourgram, freq)


# 2.1.1 为给定的文本开发MLE
# 最大似然估计(Maximum Likelihood Estimate, MLE),是 NLP 领域中的一项重要任务,
# 其也被称作多元逻辑回归或条件指数分类器。Berger 和 Della Pietra 曾于 1996 年首次介绍
# 了它。最大熵模型被定义在 NLTK 中的 nltk.classify.maxent 模块里,在该模块中,
# 所有的概率分布被认为是与训练数据保持一致的。该模型用于指代两个特征,即输入特征
# 和联合特征。输入特征可以认为是未加标签单词的特征,而联合特征可以认为是加标签单
# 词的特征。MLE 用于生成 freqdist,它包含了文本中给定标识符出现的概率分布。参数
# freqdist 由作为概率分布基础的频率分布组成。
# 让我们来看看 NLTK 中有关最大熵模型的代码



if __name__ == '__main__':
    import nltk
    # nltk.download('alpino')
    # nltk.download('webtext')
    fun_2_1()