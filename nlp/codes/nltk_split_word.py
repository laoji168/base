# coding=utf-8
"""
第一章 字符串操作
1.1 切分
"""

# 1.1.1 将文本切分为语句
def fun_1_1_1_1():
    import nltk
    from nltk.tokenize import sent_tokenize
    text = "Welcome readers. I hope you find it interesting. Please do reply."
    print sent_tokenize(text)


def fun_1_1_1_2():
    import nltk
    # 切 分 大 批 量 的 句 子 , 我 们 可 以 加 载 PunktSentenceTokenizer
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    text = " Hello everyone. Hope all are fine and doing well. Hope you find the book interesting"
    print tokenizer.tokenize(text)


# 1.1.2 其他语言文本的切分
def fun_1_1_2():
    # 加载它们各自的 pickle 文件(可以在tokenizers/punkt 里边找到)
    import nltk
    french_tokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
    print french_tokenizer.tokenize("Deux agressions en quelques jours,\
        voilà ce qui a motivé hier matin le débrayage collège franco-\
        britanniquede Levallois-Perret. Deux agressions en quelques jours,\
        voilà ce qui a motivé hier matin le débrayage Levallois. L'équipe\
        pédagogique de ce collège de 750 élèves avait déjà été choquée\
        par l'agression, janvier , d'un professeur d'histoire. L'équipe\
        pédagogique de ce collège de 750 élèves avait déjà été choquée par\
        l'agression, mercredi , d'un professeur d'histoire')\
        ['Deux agressions en quelques jours, voilà ce qui a motivé hier\
        matin le débrayage collège franco-britanniquedeLevallois-Perret.',\
        'Deux agressions en quelques jours, voilà ce qui a motivé hier matin\
        le débrayage Levallois.', 'L'équipe pédagogique de ce collège de\
        750 élèves avait déjà été choquée par l'agression, janvier , d'un\
        professeur d'histoire.', 'L'équipe pédagogique de ce collège de\
        750 élèves avait déjà été choquée par l'agression, mercredi , d'un\
        professeur d'histoire")


# 1.1.3 将句子划分为单词
def fun_1_1_3():
    import nltk
    text = nltk.word_tokenize("PierreVinken , 59 years old , will join as a nonexecutive director on Nov. 29 .")
    print text

    from nltk import word_tokenize
    r = raw_input("Please write a text")
    print "The length of text is", len(word_tokenize(r)), "words"


# 1.1.4 使用TreebankWordTokenizer执行切分
def fun_1_1_4():
    import nltk
    from nltk.tokenize import TreebankWordTokenizer
    tokenizer = TreebankWordTokenizer()
    print tokenizer.tokenize("Don't worry! Have a nice day. I hope you find the book interesting")
    print nltk.word_tokenize("Don't worry! Have a nice day. I hope you find the book interesting")
    from nltk.tokenize import WordPunctTokenizer
    tokenizer = WordPunctTokenizer()
    print tokenizer.tokenize("Don't worry! Have a nice day. I hope you find the book interesting")


# 1.1.5 使用正则表达式实现切分
def fun_1_1_5():
    import nltk
    from nltk.tokenize import RegexpTokenizer
    from nltk.tokenize import regexp_tokenize
    tokenizer = RegexpTokenizer("[\w]+")
    print "RegexpTokenizer:", tokenizer.tokenize("Don't hesitate to ask questions")
    print "regexp_tokenizer:", regexp_tokenize("Don't hesitate to ask questions", pattern="\w+|\$[\d\.]+|\S+")
    # 通过空格来执行切分
    tokenizer = RegexpTokenizer('\s+', gaps=True)
    print "RegexpTokenizer:", tokenizer.tokenize("Don't hesitate to ask questions")
    # 筛选以大写字母开头的单词
    sent = " She secured 90.56 % in class X \n. She is a meritorious student"
    capt = RegexpTokenizer('[A-Z]\w+')
    print "RegexpTokenizer:", capt.tokenize(sent)
    # RegexpTokenizer 的一个子类是如何使用预定义正则表达式的
    from nltk.tokenize import BlanklineTokenizer
    print "BlanklineTokenizer:", BlanklineTokenizer().tokenize(sent)
    # 字符串的切分可以通过空格、间隔、换行等来完成
    from nltk.tokenize import WhitespaceTokenizer
    print "WhitespaceTokenizer:", WhitespaceTokenizer().tokenize(sent)
    # WordPunctTokenizer 使用正则表达式\w+|[^\w\s]+来执行文本的切分,并将其
    # 切分为字母与非字母字符
    from nltk.tokenize import WordPunctTokenizer
    print "WordPunctTokenizer:", WordPunctTokenizer().tokenize(sent)
    # 使用 split()方法进行切分
    print "split():", sent.split()
    print "split(' '):", sent.split(' ')
    print "split('\n'):", sent.split('\n')
    # 类似于 sent.split('\n')方法,LineTokenizer 通过将文本切分为行来执行切分
    from nltk.tokenize import LineTokenizer
    print "LineTokenizer:", LineTokenizer().tokenize(sent)
    print "LineTokenizer:", LineTokenizer(blanklines='keep').tokenize(sent)
    print "LineTokenizer:", LineTokenizer(blanklines='discard').tokenize(sent)
    # SpaceTokenizer 与 sent.split('')方法的工作原理类似
    from nltk.tokenize import SpaceTokenizer
    print "SpaceTokenizer:", SpaceTokenizer().tokenize(sent)
    # nltk.tokenize.util 模块通过返回元组形式的序列来执行切分,该序列为标识符
    # 在语句中的位置和偏移量
    print "标识符序列：", list(WhitespaceTokenizer().span_tokenize(sent))
    # 给定一个标识符的序列,则可以返回其跨度序列
    from nltk.tokenize.util import spans_to_relative
    print "位置和偏移：", list(spans_to_relative(WhitespaceTokenizer().span_tokenize(sent)))
    # 通过在每一个分隔符的连接处进行分割,nltk.tokenize.util.string_span_tokenize(sent,separator)将返回 sent 中标识符的偏移量:
    from nltk.tokenize.util import string_span_tokenize
    print "标识符序列：", list(string_span_tokenize(sent, " "))


"""
1.2 标准化
为了实现对自然语言文本的处理,我们需要对其执行标准化,主要涉及消除标点符号、
将整个文本转换为大写或小写、数字转换成单词、扩展缩略词、文本的规范化等操作
"""
# 1.2.1 消除标点符号
def fun_1_2_1():
    import re, string
    from nltk import tokenize
    text = [" It is a pleasant evening.","Guests, who came from US arrived at the venue","Food was tasty."]
    # 得到切分文本
    tokenized_docs = [tokenize.word_tokenize(doc) for doc in text]
    print "切分文本：", tokenized_docs
    # 删除标点符号,string.punctuation特殊字符 re.escape 将字符串中所有特殊正则表达式字符转义
    x = re.compile('[%s]'% re.escape(string.punctuation))
    tokenized_docs_no_punctuation = []
    for review in tokenized_docs:
        new_review = []
        for token in review:
            new_token = x.sub(u" ", token)  # 将匹配上的符号替换成空格
            print new_token
            if not new_token == u" ":  # 未被替换则是字符
                new_review.append(new_token)
        tokenized_docs_no_punctuation.append(new_review)
    print "去除标点后：", tokenized_docs_no_punctuation


# 1.2.2 文本的大小写转换
def fun_1_2_2():
    text = 'HARdWork IS KEy to SUCCESS'
    print text.lower()
    print text.upper()


# 1.2.3 处理停止词
# NLTK 库为多种语言提供了一系列的停止词,为了可以从 nltk_data/corpora/
# stopwords 中访问停止词列表,我们需要解压 datafile 文件
# nltk.corpus.reader.WordListCorpusReader 类的实例是一个 stopwords
# 语料库,它拥有一个参数为 fileid 的 words()函数。这里参数为 English,它指的是在
# 英语文件中存在的所有停止词。如果 words()函数没有参数,那么它指的将是关于所有语
# 言的全部停止词。
# 可以在其中执行停止词删除的其他语言,或者在 NLTK 中其文件存在停止词的语言数
# 量都可以通过使用 fileids()函数找到
def fun_1_2_3():
    import nltk
    from nltk.corpus import stopwords
    stops = set(stopwords.words('english'))
    words = ["Don't", 'hesitate','to','ask','questions']
    print [word for word in words if word not in stops]
    print stopwords.fileids()


# 1.2.4 计算英语中的停止词
def fun_1_2_4():
    from nltk import corpus
    from nltk.corpus import stopwords
    print stopwords.words('english')

    def para_fraction(text):
        stopwords = corpus.stopwords.words('english')
        para = [w for w in text if w.lower() not in stopwords]
        return len(para) / len(text)
    print para_fraction(corpus.reuters.words())
    print para_fraction(corpus.inaugural.words())


"""
1.3 替换和交换标识符
"""
# 1.3.1 使用正则表达式替换单词
# 为了消除错误或执行文本的标准化,需要做单词替换。一种可以完成文本替换的方法
# 是使用正则表达式。之前,在执行缩略词切分时我们遇到了问题。通过使用文本替换,我
# 们可以用缩略词的扩展形式来替换缩略词。例如,doesn’t 可以被替换为 does not
import re
class RegexpReplacer(object):
    replacement_patterns = [
        (r'won\'t', 'will not'),
        (r'can\'t', 'cannot'),
        (r'i\'m', 'i am'),
        (r'ain\'t', 'is not'),
        (r'(\w+)\'ll', '\g<1> will'),
        (r'(\w+)n\'t', '\g<1> not'),
        (r'(\w+)\'ve', '\g<1> have'),
        (r'(\w+)\'s', '\g<1> is'),
        (r'(\w+)\'re', '\g<1> are'),
        (r'(\w+)\'d', '\g<1> would')
    ]
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s


# 1.3.2 用其他文本替换文本的示例
def fun_1_3_2():
    import nltk
    replacer = RegexpReplacer()
    print replacer.replace("Don't hesitate to ask questions, won't worry ")
    print replacer.replace("She must've gone to the market but she didn't go")


# 1.3.3 在执行切分前先执行替换操作
# 标识符替换操作可以在切分前执行,以避免在切分缩略词的过程中出现问题
def fun_1_3_3():
    import nltk
    from nltk import tokenize
    print tokenize.word_tokenize("Don't hesitate to ask questions")
    print tokenize.word_tokenize(RegexpReplacer().replace("Don't hesitate to ask questions"))


# 1.3.4 处理重复字符
# 使用 RepeatReplacer 的问题是它会将 happy 转换为 hapy,这样是不妥的。为了
# 避免这个问题,我们可以嵌入 wordnet 与其一起使用
from nltk.corpus import wordnet
class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'
    def replace(self, word):
        if wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


# 1.3.5 去除重复字符的示例
def fun_1_3_5():
    import nltk
    print RepeatReplacer().replace('lotttt')
    print RepeatReplacer().replace('ohhhhh')
    print RepeatReplacer().replace('ooohhhhh')
    print RepeatReplacer().replace("happy")


# 1.3.6 用单词的同义词替换
class WordReplacer(object):
    def __init__(self, word_map):
        self.word_map = word_map
    def replace(self, word):
        return self.word_map.get(word, word)


# 1.3.7 用单词的同义词替换的示例
def fun_1_3_7():
    import nltk
    replacer = WordReplacer({'congrats':'congratulations'})
    print replacer.replace('congrats')
    print replacer.replace('maths')


"""
1.4 在文本上应用Zipf定律
Zipf 定律指出,文本中标识符出现的频率与其在排序列表中的排名或位置成反比。该
定律描述了标识符在语言中是如何分布的:一些标识符非常频繁地出现,另一些出现频率
较低,还有一些基本上不出现。
让我们来看看 NLTK 中用于获取基于 Zipf 定律的双对数图(log-log plot)的代码

代码将获取一个关于单词在文档中的排名相对其出现的频率的双对数图。因此,我们
可以通过查看单词的排名与其频率之间的比例关系来验证 Zipf 定律是否适用于所有文档
"""
def fun_1_4():
    import nltk
    from nltk.corpus import gutenberg
    from nltk.probability import FreqDist
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('TkAgg')
    fd = FreqDist()
    for text in gutenberg.fileids():
        for word in gutenberg.words(text):
            fd.inc(word)
    ranks = []
    freqs = []
    for rank, word in enumerate(fd):
        ranks.append(rank + 1)
        freqs.append(fd[word])
    plt.loglog(ranks, freqs)
    plt.xlabel('frequency(f)', fontsize=14, fontweight='bold')
    plt.ylabel('rand(r)', fontsize=14, fontweight='bold')
    plt.grid(True)
    plt.show()


"""
1.5 相似性度量
有许多可用于执行 NLP 任务的相似性度量。NLTK 中的 nltk.metrics 包用于提供
各种评估或相似性度量,这将有利于执行各种各样的 NLP 任务。
在 NLP 中,为了测试标注器、分块器等的性能,可以使用从信息检索中检索到的标准分数。
让我们来看看如何使用标准分(从一个训练文件中获取的)来分析命名实体识别器的
输出
"""
def fun_1_5():
    # from __future__ import print_function
    from nltk.metrics import *
    training = 'PERSON OTHER PERSON OTHER OTHER ORGANIZATION'.split()
    testing = 'PERSON OTHER OTHER OTHER OTHER OTHER'.split()
    print accuracy(training, testing)
    trainset = set(training)
    testset = set(testing)
    print precision(trainset, testset)
    print recall(trainset, testset)
    print f_measure(trainset, testset)


# 1.5.1 使用编辑距离算法执行相似性度量
# 两个字符串之间的编辑距离或 Levenshtein 编辑距离算法用于计算为了使两个字符串
# 相等所插入、替换或删除的字符数量。
# 在编辑距离算法中需要执行的操作包含以下内容:
# •
# 将字母从第一个字符串复制到第二个字符串(cost 为 0),并用另一个字母替换字母
# (cost 为 1):
# D(i−1,j−1) + d(si,tj)(替换 /复制操作)
# •
# 删除第一个字符串中的字母(cost 为 1):
# D(i,j−1)+1(删除操作)
# •
# 在第二个字符串中插入一个字母(cost 为 1):
# D(i,j) = min D(i−1,j)+1 (插入操作)
# nltk.metrics 包中的 Edit Distance 算法的 Python 代码如下所示
def fun_1_5_1():
    # 编辑距离pyton实现
    def _edit_dist_init(len1, len2):
        lev = []
        for i in range(len1):
            lev.append([0] * len2)  # initialize 2D array to zero
        for i in range(len1):
            lev[i][0] = i  # column 0:0,1,2,3,4,......
        for j in range(len2):
            lev[0][j] = j  # row 0:0,1,2,3,4,......
        return lev

    def _edit_dist_step(lev, i, j, s1, s2, transpositions=False):
        c1 = s1[i-1]
        c2 = s2[j-1]
        # skipping a character in s1
        a = lev[i-1][j] + 1
        # skipping a character in s2
        b = lev[i][j-1] + 1
        # substitution
        c = lev[i-1][j-1] + (c1 != c2)
        # transposition
        d = c + 1  # never picked by default
        if transpositions and i >1 and j > 1:
            if s1[i-2] == c2 and s2[j-2] == c1:
                d = lev[i-2][j-2] + 1
        # pick the cheapest
        lev[i, j] = min(a, b, c, d)

    def edit_distance(s1, s2, transportsitions=False):
        # set-up a 2-D array
        len1 = len(s1)
        len2 = len(s2)
        lev = _edit_dist_init(len1+1, len2+1)
        # iterate over the array
        for i in range(len1):
            for j in range(len2):
                _edit_dist_step(lev, i+1, j+1, s1, s2, transportsitions = transportsitions)
        return lev[len1][len2]

    import nltk
    from nltk.metrics import edit_distance
    print edit_distance('relate', 'relation')
    print edit_distance("suggestion","calculation")


# 1.5.2 使用Jaccard系数执行相似性度量
# Jaccard 系数或 Tanimoto 系数可以认为是两个集合 X 和 Y 交集的相似程度。
# 它可以定义如下:
# • Jaccard(X,Y)=|X∩Y|/|XUY|。
# • Jaccard(X,X)=1。
# • Jaccard(X,Y)=0 if X∩Y=0。
def fun_1_5_2():
    def jacc_similarity(query, document):
        first = set(query).intersection(set(document))
        second = set(query).union(set(document))
        return len(first)/len(second)
    from nltk.metrics import jaccard_distance
    X = set([10,20,30,40])
    Y = set([20, 30, 60])
    print jaccard_distance(X, Y)


# 1.5.3 使用 Smith Waterman 距离算法执行相似性度量
# Smith Waterman 距离算法类似于编辑距离算法。开发这种相似度指标以便检测相关蛋
# 白质序列和 DNA 之间的光学比对。它包括被分配的成本和将字母表映射到成本值的函数
# (替换);成本也分配给 gap 惩罚(插入或删除)。
# 1.0 //start over
# 2.D(i−1,j−1) −d(si,tj) //subst/copy
# 3.D(i,j) = max D(i−1,j) −G //insert
# 1.D(i,j−1) −G //delete
# Distance is maximum over all i,j in table of
# D(i,j)。
# 4.G = 1 //example value for gap
# 5.d(c,c) = −2 //context dependent substitution cost
# 6.d(c,d) = +1 //context dependent substitution cost
# 与编辑距离算法类似,Smith Waterman 的 Python 代码可以嵌入到 nltk.metrics 包
# 中,以便使用 NLTK 中的 Smith Waterman 算法执行字符串相似性度量。


# 1.5.4 其他字符串相似性度量
def fun_1_5_4():
    from nltk import metrics
    # 二进制距离是一个字符串相似性指标。如果两个标签相同,它的返回值为 0.0;否则,
    # 它的返回值为 1.0
    def binary_distance(label1, label2):
        return 0.0 if label1 == label2 else 1.0
    print metrics.binary_distance((10,20,30,40), (30, 50, 70))
    # 当存在多个标签时,Masi 距离基于部分协议。
    # 包含在 nltk.metrics 包中的 masi 距离算法的 Python 代码如下
    def masi_distance(label1, label2):
        len_intersection = len(label1.intersection(label2))
        len_union = len(label1.union(label2))
        len_label1 = len(label1)
        len_label2 = len(label2)
        if len_label1 == len_label2 and len_label1 == len_intersection:
            m = 1
        elif len_intersection == min(len_label1, len_label2):
            m = 0.67
        elif len_intersection > 0:
            m = 0.33
        else:
            m = 0
        return 1 - (len_intersection / float(len_union)) * m
    print metrics.masi_distance((10,20,30,40), (30, 50, 70))


if __name__ == '__main__':

    import nltk
    # nltk.download('punkt')
    # nltk.download('stopwords')
    # nltk.download('reuters')
    # nltk.download('inaugural')
    # nltk.download("wordnet")
    # nltk.download('gutenberg')
    fun_1_5_4()