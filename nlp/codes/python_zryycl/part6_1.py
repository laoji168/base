# coding=utf-8
import nltk
"""
学习分类文本
"""
def fun1():
    """
    性别鉴定
在2.4节中我们看到,男性和女性的名字有各自鲜明的特点。以a、e和i结尾的姓名很可能是女性姓名,
而以k、o、r和s结尾的姓名很可能是男性姓名。建立一个分类器从而更精确地模拟这些差异
    创建分类器的第一步是决定什么样的输入特征是相关的,以及如何为这些特征编码
    :return:
    """
    def gender_features(word):
        return {'suffix1': word[-1:],'suffix2': word[-2:]}
    # 这个函数返回的字典被称为特征集,能把特征名称映射到它们的值。特征名称是区分大小写的字符
    # 串,通常提供一个简短的、可读的特征描述。特征值是简单类型的值,如布尔、数字和字符串。
    # 定义一个特征提取器, 同时准备一些例子和与其对应的类标签
    from nltk.corpus import names
    import random
    names = ([(name, 'male') for name in names.words('male.txt')]+
             [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(names)
    print names
    # 接下来,使用特征提取器处理names数据,并把特征集的结果链表划分为训练集和测试集。训练集用于
    # 训练新的“朴素贝叶斯”分类器
    featuresets = [(gender_features(n), g) for n, g in names]
    train_set, test_set = featuresets[500:], featuresets[:500]
    # 在处理大型语料库时,构建包含所有实例特征的单独链表会占用大量的内存。在这种情况下,使用函
    # 数nltk.classify.apply_features,返回一个像链表但不会在内存存储所有特征集的对象
    from nltk.classify import apply_features
    train_set = apply_features(gender_features, names[500:])
    test_set = apply_features(gender_features, names[:500])
    print train_set
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    # 现在,测试一些没有出现在训练数据
    # 中的名字。
    print classifier.classify(gender_features('Neo'))
    print classifier.classify(gender_features('Trinity'))
    # 我们可以利用大量未见过的数据系统地评估这个分类
    # 器。
    print nltk.classify.accuracy(classifier, test_set)
    # 最后,检查分类器,确定哪些特征对于区分名字的性别是最有效的
    print classifier.show_most_informative_features(5)
    # 此列表显示训练集中以a结尾的名字中女性是男性的38倍,而以k结尾的名字中男性是女性的31倍。这
    # 些比率称为似然比,可以用于比较不同特征-结果关系

    # 选定初始特征集,一种能有效完善特征集的方法称为错误分析。首先,选择开发集,其中包含用于创
    # 建模型的语料数据。然后将这种开发集分为训练集和开发测试集
    train_names = names[1500:]
    devtest_names = names[500:1500]
    test_names = names[:500]
    # 将语料分为适当的数据集,然后使用训练集来训练模型 1 ,之后在开发测试集上运行
    train_set = [(gender_features(n), g) for (n, g) in train_names]
    devtest_set = [(gender_features(n), g) for (n, g) in devtest_names]
    test_set = [(gender_features(n), g) for (n, g) in test_names]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, devtest_set)
    # 使用开发测试集可以生成分类器在预测名字性别时出现的错误列表
    errors = []
    for (name, tag) in devtest_names:
        guess = classifier.classify(gender_features(name))
        if guess != tag:
            errors.append((tag, guess, name))
    # 然后,检查个别错误案例,在案例中该模型预测了错误的标签,尝试确定加入什么样的额外信息才能
    # 够使其作出正确的决定(或者是现有的哪部分信息导致其做出了错误的决定)。然后相应地调整特征集。
    # 下例中已建立的名字分类器在开发测试语料上产生约100个错误。
    for (tag, guess, name) in sorted(errors):  # doctest: +ELLIPSIS +NORMALIZE_ WHITESPACE
        print 'correct=%-8s guess=%-8s name=%-30s' %(tag, guess, name)
    # 浏览这个错误列表,它明确指出某些多字母后缀也可以指示名字性别。例如:以yn结尾的名字大多以
    # 女性为主,尽管事实上,以n结尾的名字往往是男性;以ch结尾的名字通常是男性,尽管以h结尾的名字倾
    # 向于是女性。因此,调整特征提取器使其包含两个字母后缀的特征
    # 使用新的特征提取器重建分类器
    train_set = [(gender_features(n), g) for (n, g) in train_names]
    devtest_set = [(gender_features(n), g) for (n, g) in devtest_names]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, devtest_set)


def fun2():
    import random
    # 在2.1节中,我们看到了几个有关语料库的例子,其中文档已经按类别标记。使用这些语料库,建立分
    # 类器,自动为新文档添加适当的类别标签。首先,构造已标记相应类别的文档清单。对于下面的例子,选
    # 择电影评论语料库,将每个评论归类为正面或负面
    from nltk.corpus import movie_reviews
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    # 接下来,为文档定义特征提取器,这样分类器就会知道应注意哪些方面的数据(见例6-2)。对于文档
    # 主题识别,可以为每个词定义一个特性以表示该文档是否包含这个词。为了限制分类器需要处理的特征数
    # 目,构建整个语料库中前2000个最频繁词的链表 1 。然后,定义一个特征提取器 2 ,简单地检查这些词是否
    # 在一个给定的文档中。
    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    word_features = all_words.keys()[:2000]
    def document_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features
    print document_features(movie_reviews.words('pos/cv957_8737.txt'))
    # 现在,定义特征提取器,用它来训练分类器,并为新的电影评论加标签(见例6-3)。为了检查生成的
    # 分类器可靠性如何,可在测试集上计算其准确性 1 。同时,我们还可以使用show_most_informative_features()来找出哪些特
    # 征是分类器发现的并且是最有信息量的
    featuresets = [(document_features(d), c) for (d, c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)
    print classifier.show_most_informative_features(5)


def fun3():
    # 探索上下文语境
    # 通过增加特征提取函数,可以修改词性标注器以利用各种词内部的其他特征,例如:词长、所包含的
    # 音节数或者前缀。然而,只要特征提取器仅仅关注目标词,我们就没法添加特征,这些依赖于词所出现的
    # 上下文语境。然而语境特征往往提供关于正确标记的强大线索——例如:标注词fly时,如果知道它前面的
    # 词是“a”,能够确定它是名词,而不是动词。
    # 为了应用基于词的上下文这个特征,必须修改定义特征提取器的模式。我们不是只传递已标注的词,
    # 而是传递整个(未标注的)句子,以及目标词的索引。例6-4演示了这种方法,使用依赖上下文的特征提取
    # 器来定义一个词性标记分类器。
    from nltk.corpus import brown
    def pos_features(sentence, i):
        features = {"suffix(1)": sentence[i][-1:],
                    "suffix(2)": sentence[i][-2:],
                    "suffix(3)": sentence[i][-3:]}
        if i == 0:
            features["prev-word"] = "<START>"
        else:
            features["prev-word"] = sentence[i - 1]
        return features
    print pos_features(brown.sents()[0], 8)
    tagged_sents = brown.tagged_sents(categories='news')
    featuresets = []
    for tagged_sent in tagged_sents:
        print tagged_sent
        untagged_sent = nltk.tag.untag(tagged_sent)
        print untagged_sent
        for i, (word, tag) in enumerate(tagged_sent):
            featuresets.append((pos_features(untagged_sent, i),tag))
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)


def fun4():
    # 序列分类
    # 为了获取相关分类任务之间的依赖关系,我们可以使用联合分类器模型,为一些相关的输入选择适当
    # 的标签。在词性标注的例子中,可以使用各种不同的序列分类器模型为给定的句子中的所有词选择词性标
    # 签。
    # 一种称为连续分类或贪婪序列分类的序列分类器策略,为第一个输入找到最有可能的类标签,然后在
    # 此基础上找到下一个输入的最佳的标签。这个过程可以不断重复直到所有的输入都被贴上标签。如5.5节中
    # 的双字母标注器,首先为句子的第一个词选择词性标记,然后基于词本身和前面词的预测标记,为每个随
    # 后的词选择标记。
    # 例6-5演示了这一过程。首先,扩展特征提取函数使其具有参数history,其中包括已经为句子预测的标
    # 记链表 1 。history中的每个标记对应sentence中的一个词。但是请注意,history将只包含已经归类的词的标
    # 记,也就是目标词左侧的词。因此,虽然有可能查看目标词右边词的某些特征,但查看这些词的标记是不
    # 可能的(因为还未生成它们)。
    # 定义特征提取器,继续建立序列分类器 2 。在训练中,使用已标注的标记为征提取器提供适当的历史信
    # 息,但标注新的句子时,基于标注器本身的输出来产生历史信息。
    def pos_features(sentence, i, history):

        features = {"suffix(1)": sentence[i][-1:],
                    "suffix(2)": sentence[i][-2:],
                    "suffix(3)": sentence[i][-3:]}
        if i == 0:
            features["prev-word"] = "<START>"
            features["prev-tag"] = "<START>"
        else:
            features["prev-word"] = sentence[i - 1]
            features["prev-tag"] = history[i - 1]
        return features


    class ConsecutivePosTagger(nltk.TaggerI):

        def __init__(self, train_sents):
            train_set = []
            for tagged_sent in train_sents:
                untagged_sent = nltk.tag.untag(tagged_sent)
                history = []
                for i, (word, tag) in enumerate(tagged_sent):
                    featureset = pos_features(untagged_sent, i, history)
                    train_set.append((featureset, tag))
                    history.append(tag)
                self.classifier = nltk.NaiveBayesClassifier.train(train_set)


        def tag(self, sentence):
            history = []
            for i, word in enumerate(sentence):
                featureset = pos_features(sentence, i, history)
                tag = self.classifier.classify(featureset)
                history.append(tag)
            return zip(sentence, history)

    from nltk.corpus import brown
    tagged_sents = brown.tagged_sents(categories='news')
    size = int(len(tagged_sents) * 0.1)
    train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
    tagger = ConsecutivePosTagger(train_sents)
    print tagger.evaluate(test_sents)

# nltk.download('movie_reviews')
fun4()