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




if __name__ == '__main__':

    # import nltk
    # nltk.download('punkt')
    fun_1_1_5()