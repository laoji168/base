# coding=utf-8
import nltk
"""
nltk.corpus.gutenberg 代表既定的文学
"""
def fun1():
    print nltk.corpus.gutenberg.fileids()
    emma = nltk.corpus.gutenberg.words('austen-emma.txt')
    print len(emma)

    # 执行索引
    emma = nltk.Text(emma)
    print emma.concordance('surprize')


def fun2():
    # 这个程序运行结果显示出每个文本的3个统计量:平均词长、平均句子长度和本文中每个词出现的平均
    # 次数(词汇多样性得分)。平均词长看似是英语的一个一般属性,因为它的值总是4。(事实上,平均词长
    # 是3而不是4,因为num_chars变量计数了空白字符。)相比之下,平均句子长度和词汇多样性看上去是作者
    # 个人的特点。
    # 前面的例子也表明我们怎样才能获取“原始”文本 1 而不用把它分割成标识符。raw()函数能在没有进行
    # 过任何语言学处理之前把文件的内容分析出来。例如:len(gutenberg.raw('blake-poems.txt') 能告诉我们文本
    # 中出现的词汇个数,包括词之间的空格。sents()函数把文本划分成句子,其中每一个句子是一个词链表
    from nltk.corpus import gutenberg
    for fileid in gutenberg.fileids():
        num_chars = len(gutenberg.raw(fileid))
        num_words = len(gutenberg.words(fileid))
        num_sents = len(gutenberg.sents(fileid))
        num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
        print int(num_chars/num_words), int(num_words/num_sents), int(num_words/num_vocab), fileid

    print "1:", gutenberg.raw('austen-emma.txt')
    print "2:", gutenberg.words('austen-emma.txt')
    print "3:", gutenberg.sents('austen-emma.txt')


"""
网络文本 nltk.corpus.webtext
"""

def fun3():
    from nltk.corpus import webtext
    for fileid in webtext.fileids():
        print fileid, webtext.raw(fileid)[:65]


"""
即时信息聊天语料 nltk.corpus.nps_chat
"""
def fun4():
    from nltk.corpus import nps_chat
    nltk.download('nps_chat')
    chatroom = nps_chat.posts('10-19-20s_706posts.xml')
    print chatroom[123]
    for i in nps_chat.fileids():
        print i


"""
布朗语料库是第一个百万词级的英语电子语料库,由布朗大学于1961年创建。这个语料库包含500个不
同来源的文本,按照文体分类,如新闻、社论等
nltk.corpus.brown
"""
def fun5():
    from nltk.corpus import brown
    # nltk.download('brown')
    for i in brown.fileids():
        print i
    print brown.categories()
    print brown.words(categories='news')
    print brown.words(fileids='cg22')
    print brown.sents(categories=['news', 'editorial', 'reviews'])


def fun6():
    # 布朗语料库是一个研究文体之间的系统性差异(又叫做文体学的语言学研究)的资源。让我们来比较
    # 不同文体中的情态动词的用法
    from nltk.corpus import brown
    news_text = brown.words(categories='news')
    fdist = nltk.FreqDist([w.lower() for w in news_text])
    modals = ['can', 'could', 'may', 'might', 'must', 'will']
    for m in modals:
        print m + ":", fdist[m]


"""
路透社语料库包含10788个新闻文档,共计130万字。这些文档分成90个主题,按照“训练”和“测试”分为
两组。因此,编号为“test/14826”的文档属于测试组。这样分割是为了方便运用训练和测试算法的自动检测
文档的主题
nltk.corpus.reuters
"""
def fun7():
    from nltk.corpus import reuters
    print reuters.fileids()
    print reuters.categories()
    # 与布朗语料库不同,路透社语料库的类别是互相重叠的,因为新闻报道往往涉及多个主题。我们可以
    # 查找由一个或多个文档涵盖的主题,也可以查找包含在一个或多个类别中的文档。为了方便起见,语料库
    # 方法既接受单个的标示也接受标示列表作为参数
    print reuters.categories('training/9865')
    print reuters.categories(['training/9865', 'training/9880'])
    print reuters.fileids('barley')
    print reuters.fileids(['barley', 'corn'])


"""
就职演说语料库
语料库实际上是55个文本的集合,每个文本都是一个总统的演说。这个集合的一个显着特性是时间维度
需要注意的是,每个文本的年代都出现在它的文件名中。要从文件名中获得年代,使用fileid[:4]提取前
4个字符
nltk.corpus.inaugural
"""
def fun8():
    from nltk.corpus import inaugural
    print inaugural.fileids()
    print [w[:4] for w in inaugural.fileids()]

    cfd = nltk.ConditionalFreqDist((target, fileid[:4])
                                   for fileid in inaugural.fileids()
                                   for w in inaugural.words(fileid)
                                   for target in ['america', 'citizen']
                                   if w.lower().startswith(target))
    cfd.plot()  # 条件频率分布图


"""
标注文本语料库
许多文本语料库都包含语言学标注,有词性标注、命名实体、句法结构、语义角色等。NLTK中提供了
几种很方便的方法来访问这几个语料库,而且还包含有语料库和语料样本的数据包,用于教学和科研时,
可以免费下载。表2-2列出了其中一些语料库。有关下载信息请参阅http://www.nltk.org/ data。关于如何访问
NLTK语料库的其他例子,请在http://www.nltk.org/howto上查阅语料库的HOWTO。
"""

"""
NLTK包含多国语言语料库
"""
def fun9():
    # nltk.download('cess_esp')
    # nltk.download('floresta')
    # nltk.download('indian')
    # nltk.download('udhr')
    print nltk.corpus.cess_esp.words()
    print nltk.corpus.floresta.words()
    print nltk.corpus.indian.words('hindi.pos')
    print nltk.corpus.udhr.fileids()
    print nltk.corpus.udhr.words('Javanese-Latin1')[11:]


def fun10():
    from nltk.corpus import udhr
    languages = ['Chickasaw', 'English', 'German_Deutsch', 'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
    cfd = nltk.ConditionalFreqDist((lang, len(word))
                                   for lang in languages
                                   for word in udhr.words(lang + '-Latin1'))
    cfd.plot(cumulative=True)



"""
载入你自己的语料库
如果你有自己收集的文本文件,并想使用前面讨论的方法来访问它们,在NLTK中的
PlaintextCorpusReader帮助下,你能很容易地载入它们。在你的文件系统中检查文件的位置;在下面的例子
中,假定你的文件在/usr/share/dict目录下。不管是什么位置,将变量corpus_root 1 的值设置为这个目录。
PlaintextCorpusReader初始化函数 2 的第二个参数可以是一个如['a.txt', 'test/b.txt']这样的fileids链表,或者一个
匹配所有标示的模式,如:'[abc]/.*.txt'(关于正则表达式的信息见3.4节)。

>>> from nltk.corpus import PlaintextCorpusReader
>>> corpus_root = '/usr/share/dict' 1
>>> wordlists = PlaintextCorpusReader(corpus_root, '.*') 2
>>> wordlists.fileids()
['README', 'connectives', 'propernames', 'web2', 'web2a', 'words']
>>> wordlists.words('connectives')
['the', 'of', 'and', 'to', 'a', 'in', 'that', 'is', ...]

下面是另一个例子,假设你在本地硬盘上有自己的宾州树库(第3版)的副本,放在C:\corpora。我们可
以使用BracketParseCorpusReader来访问这些语料。我们指定corpus_root来存放语料库中已解析过的《华尔街
日报》部分 1 ,并指定file_pattern与它的子文件夹中所包含的文件匹配 2 (用前斜杠)。

>>> from nltk.corpus import BracketParseCorpusReader
>>> corpus_root = r"C:\corpora\penntreebank\parsed\mrg\wsj" 1
>>> file_pattern = r".*/wsj_.*\.mrg" 2
>>> ptb = BracketParseCorpusReader(corpus_root, file_pattern)
>>> ptb.fileids()
['00/wsj_0001.mrg', '00/wsj_0002.mrg', '00/wsj_0003.mrg', '00/wsj_0004.mrg', ...]
>>> len(ptb.sents())
49208
>>> ptb.sents(fileids='20/wsj_2013.mrg')[19]
['The', '55-year-old', 'Mr.', 'Noriega', 'is', "n't", 'as', 'smooth', 'as', 'the',
'shah', 'of', 'Iran', ',', 'as', 'well-born', 'as', 'Nicaragua', "'s", 'Anastasio',
'Somoza', ',', 'as', 'imperial', 'as', 'Ferdinand', 'Marcos', 'of', 'the', 'Philippines',
'or', 'as', 'bloody', 'as', 'Haiti', "'s", 'Baby', Doc', 'Duvalier', '.']
"""



fun10()