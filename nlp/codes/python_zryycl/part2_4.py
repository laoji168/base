# coding=utf-8
import nltk
"""
词汇列表语料库
NLTK中包括一些仅仅包含词汇列表的语料库。词汇语料库是UNIX中的/usr/dict/ words文件,被一些拼
写检查程序所使用。我们可以用它来寻找文本语料中不常见的或拼写错误的词汇
"""
def fun1():
    def unusual_words(text):
        text_vocab = set(w.lower() for w in text if w.isalpha())
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        unusual = text_vocab.difference(english_vocab)
        return sorted(unusual)

    print unusual_words(nltk.corpus.gutenberg.words('austen-sense.txt'))
    print unusual_words(nltk.corpus.nps_chat.words())

    # 定义一个函数来计算文本中不包含在停用词列表中的词所占的比例
    def content_fraction(text):
        stops = nltk.corpus.stopwords.words("english")
        content = [w for w in text if w.lower() not in stops]
        print float(len(content))/len(text)

    content_fraction(nltk.corpus.reuters.words())


# nltk.download('words')


def fun2():
    # 猜谜游戏  词谜:在由随机选择的字母组成的网格中,选择里面的字母组成单词。这个谜题叫做“目标”
    # e g i v r v o n l 每个单词必须有r， 单词长度大于等于6， 被选中的字母在单词中只能有一个
    # 运行程序遍历每一个词,检查每一个词是否符合条件。检
    # 查必须出现的字母 2 和长度限制 1 是很容易的(这里我们只查找6个或6个以上字母的词)。只使用指定的字
    # 母组合作为候选方案,尤其是在一些指定的字母出现了两次(如字母v)时,这样的检查是很棘手的。利用
    # FreqDist比较法 3 检查候选词中的每个字母出现的频率是否小于或等于其相应在词谜中出现的频率
    puzzle_letters = nltk.FreqDist('eqivrvonl')
    obligatory = 'r'
    wordlist = nltk.corpus.words.words()
    print [w for w in wordlist if len(w) >= 6 and
                                  obligatory in w and
                                  nltk.FreqDist(w) <= puzzle_letters]


def fun3():
    # 另一个词汇列表是名字语料库,包括8000个按性别分类的名字。男性和女性的名字存储在单独的文件
    # 中。找出同时出现在两个文件中的名字即分辨不出性别的名字
    names = nltk.corpus.names
    print names.fileids()
    male_names = names.words('male.txt')
    female_names = names.words('female.txt')
    print [w for w in male_names if w in female_names]

    cfd = nltk.ConditionalFreqDist(
        (fileid, name[-1])
        for fileid in names.fileids()
        for name in names.words(fileid)
    )
    cfd.plot()
# nltk.download('names')


def fun4():
    # 发音的词典
    # 表格(或电子表格)是一种略微丰富的词典资源,在每一行中含有一个词及其一些性质。NLTK中包括
    # 美国英语的CMU发音词典,它是为语音合成器而设计的。
    entries = nltk.corpus.cmudict.entries()
    print len(entries)
    for entry in entries[39943:39951]:
        print entry
    prondict = nltk.corpus.cmudict.dict()
    print prondict['fire']
    # 对任意一个词,词典资源都有语音的代码——不同的声音有着不同的标签——称做音素。fire有两个发
    # 音(美国英语中):单音节F AY1 R和双音节F AY1 ER0。CMU发音词典中的符号是从Arpabet来的
    # 音素包含数字表示主重音(1)、次重音(2)和无重音(0)


def fun5():
    # 比较词表
    # 表格词典的另一个例子是比较词表。NLTK中包含了所谓的斯瓦迪士核心词列表(Swadesh
    # wordlists),包括几种语言的约200个常用词的列表。语言标识符使用ISO639双字母码
    from nltk.corpus import swadesh
    print swadesh.fileids()
    print swadesh.words('en')
    # 可以通过使用entries()
    # 方法来指定一个语言链表来访问多语言中的同源词。而且, 还可以把它转换成一
    # 个简单的词典
    fr2en = swadesh.entries(['fr', 'en'])
    print fr2en
    translate = dict(fr2en)
    print translate['chien']
    print translate['jeter']

# nltk.download('cmudict')
# nltk.download('swadesh')


def fun6():
    # 词汇工具:Toolbox和Shoebox
    # Toolbox文件由一些条目的集合组成, 其中每个条目由一个或多个字段组成。大多数字段都是可选的或
    # 重复的, 这意味着这个词汇资源不能作为一个表格或电子表格来处理
    # 条目包括一系列的“属性 - 值”对, 如('ps', 'V'), 表示词性是
    # 'V'(动词), ('ge', 'gag') 表示英文注释是'gag'。最后的3个配对包含一个罗托卡特语例句及其巴布亚皮钦语和英语的翻译
    from nltk.corpus import toolbox
    print toolbox.entries('rotokas.dic')



nltk.download('toolbox')
fun6()