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


if __name__ == '__main__':

    # import nltk
    # nltk.download('punkt')
    fun_1_1_4()