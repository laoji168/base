# coding=utf-8
import nltk
"""
监督式分类的举例
句子分割
"""
def fun1():
    # 句子分割可以看作是标点符号的分类任务:每当遇到可能会结束句子的符号时,如句号或问号,必须
    # 决定它是否终止了当前句子。
    # 第一步是获得一些已被分割成句子的数据,将它转换成一种适合提取特征的形式
    sents = nltk.corpus.treebank_raw.sents()
    tokens = []
    boundaries = set()
    offset = 0
    for sent in sents:
        tokens.extend(sent)
        offset += len(sent)
        boundaries.add(offset-1)
    # 在这里,tokens是单独句子标识符的合并链表,boundaries是一个包含所有句子-边界标识符索引的集
    # 合。下一步,我们需要指定用于决定标点是否表示句子边界的数据特征
    def punct_features(tokens, i):
        return {'next-word-capitalized': tokens[i + 1][0].isupper(),
                'prevword': tokens[i - 1].lower(),
                'punct': tokens[i],
                'prev-word-is-one-char': len(tokens[i - 1]) == 1}
    # 基于这一特征提取器,我们可以通过选择所有的标点符号创建一个加标签的特征集链表,然后标注它
    # 们是否是边界标识符。
    featuresets = [(punct_features(tokens, i), (i in boundaries))
                    for i in range(1, len(tokens) - 1)
                    if tokens[i] in '.?!']
    # 使用这些特征集,我们可以训练和评估一个标点符号分类器。
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)
    # 使用这种分类器断句,我们只需检查每个标点符号,看它是否是边界标识符,在边界标识符处分割词
    # 链表。例6-6中的列表显示了这一点是如何做到的。
    def segment_sentences(words):
        start = 0
        sents = []
        for i, word in words:
            if word in '.?!' and classifier.classify(punct_features(words, i)) == True:
                sents.append(words[start:i + 1])
                start = i + 1
        if start < len(words):
            sents.append(words[start:])
            return sents


def fun2():
    # 识别对话行为类型
    # 在2.1节中展示过的NPS聊天语料库,包括超过10000个来自即时消息会话的帖子。这些帖子都已经被贴上了15种对话行为类型中的某一种标签,例如:“陈述”、“情感”、“ynQuestion”、 “Continuer”。因此,我们
    # 可以利用这些数据建立一个分类器,用来识别新的即时消息帖子的对话行为类型。首先是提取基本的消息
    # 数据。调用xml_posts()得到一个数据结构,以表示每个帖子的XML注释
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    # 然后,定义一个简单的特征提取器,用于检查帖子包含什么词
    def dialogue_act_features(post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains(%s)' % word.lower()] = True
        return features
    # 最后,通过把特征提取器应用到每个帖子中(使用post.get('class')获取该帖子的对话行为类型)以构造
    # 训练和测试数据,并创建一个新的分类器
    featuresets = [(dialogue_act_features(post.text), post.get('class'))
                             for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print nltk.classify.accuracy(classifier, test_set)


def fun3():
    # 在RTE特征探测器(例6-7)中,我们让词(即词类型)作为信息的代理,计数词重叠的程度和假设中
    # 有而文本中没有的词的程度(由hyp_extra()方法获取)。不是所有的词都是同样重要的——提到的命名实
    # 体,如人、组织和地方的名称,可能会更为重要,这促使我们分别为words和nes(命名实体)提取不同的信息。此外,一些高频虚词作为“停用词”被过滤掉
    def rte_features(rtepair):
        extractor = nltk.RTEFeatureExtractor(rtepair)
        features = {}
        features['word_overlap'] = len(extractor.overlap('word'))
        features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
        features['ne_overlap'] = len(extractor.overlap('ne'))
        features['ne_hyp_extra'] = len(extractor.hyp_extra('ne'))
        return features
    # 为了说明这些特征的内容,检查前面显示的文本/假设对34的一些属性
    rtepair = nltk.corpus.rte.pairs(['rte3_dev.xml'])[33]
    extractor = nltk.RTEFeatureExtractor(rtepair)
    print extractor.text_words
    print extractor.hyp_words
    print extractor.overlap('word')
    print extractor.overlap('ne')
    print extractor.hyp_extra('word')
    nltk.pos_tag()


fun2()