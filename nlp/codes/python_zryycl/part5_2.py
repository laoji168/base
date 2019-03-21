# coding=utf-8
import nltk
"""
标注语料库
"""
def fun1():
    """
    按照NLTK的约定,已标注的标识符使用一个由标识符和标记组成的元组来表示。我们可以使用函数
str2tuple()表示一个已标注的标识符的标准字符串创建一个如下的特殊元组
    :return:
    """
    tagged_token = nltk.tag.str2tuple('fly/NN')
    print tagged_token

    # 我们可以直接从一个字符串构造一个已标注的标识符的链表。第一步是对字符串分词以便能访问单独
    # 的词/标记字符串,然后将每一个转换成一个元组(使用str2tuple())
    sent = '''
     The/AT grand/JJ jury/NN commented/VBD on/IN a/AT number/NN of/IN
     other/AP topics/NNS ,/, AMONG/IN them/PPO the/AT Atlanta/NP and/CC
     Fulton/NP-tl County/NN-tl purchasing/VBG departments/NNS which/WDT it/PPS
     said/VBD ``/`` ARE/BER well/QL operated/VBN and/CC follow/VB generally/RB
     accepted/VBN practices/NNS which/WDT inure/VB to/IN the/AT best/JJT
     interest/NN of/IN both/ABX governments/NNS ''/'' ./.
    '''
    print [nltk.tag.str2tuple(t) for t in sent.split()]


    # 读取已标注的语料库
    # 其他语料库使用各种格式存储词性标记。NLTK中的语料库阅读器提供了统一的接口,以至于不必理会
    # 不同的文件格式。与刚才上面提取并显示的文件不同,布朗语料库的语料库阅读器按如下所示的方式表示
    # 数据。注意:部分词性标记已转换为大写的。自从布朗语料库发布以来,这已成为标准的做法
    print nltk.corpus.brown.tagged_words()
    print nltk.corpus.nps_chat.tagged_words()
    print nltk.corpus.treebank.tagged_words()

    # NLTK中还有其他几种语言的已标注语料库,包括中文、印地语、葡萄牙语、西班牙语、荷兰语和加泰
    # 罗尼亚语。这些通常含有非ASCII文本,当输出较大的结构如列表时,Python总是以十六进制显示
    print nltk.corpus.sinica_treebank.tagged_words()
    for (word, pos) in nltk.corpus.sinica_treebank.tagged_words():
        print "%s/%s"%(word,pos)
    print nltk.corpus.indian.tagged_words()
    print nltk.corpus.mac_morpho.tagged_words()
    print nltk.corpus.conll2002.tagged_words()
    print nltk.corpus.cess_cat.tagged_words()

    # 如果语料库也被分割成句子,则利用tagged_sents()方法将已标注的词划分成句子,而不是将它们表示
    # 成一个大链表。这对开发自动标注器是有益的,因为它们在句子链表上进行训练和测试,而不是词链表
    # 标  记 含  义
    # 例  子
    # ADJ 形容词 new, good, high, special, big, local
    # ADV 动词 really, already, still, early, now
    # CNJ 连词 and, or, but, if, while, although
    # DET 限定词 the, a, some, most, every, no
    # EX 存在量词 there, there's
    # FW 外来词
    # dolce, ersatz, esprit, quo, maitre
    # MOD 情态动词
    # will, can, would, may, must, should
    # N 名词
    # year, home, costs, time, education
    # NP 专有名词
    # Alison, Africa, April, Washington
    # NUM 数词
    # twenty-four, fourth, 1991, 14:24
    # PRO 代词
    # he, their, her, its, my, I, us
    # P 介词
    # on, of, at, with, by, into, under
    # TO 词to
    # to
    # UH 感叹词
    # ah, bang, ha, whee, hmpf, oops
    # V 动词
    # is, has, get, do, make, see, run
    # VD 过去式
    # said, took, told, made, asked
    # VG 现在分词
    # making, going, playing, working
    # VN 过去分词
    # given, taken, begun, sung
    # WH Wh限定词 who, which, when, what, where, how

    # 我们来看看这些标记中哪些是布朗语料库的新闻类中最常见的
    from nltk.corpus import brown
    brown_tags_news = brown.tagged_words(categories='news')
    tag_fd = nltk.FreqDist(tag for (word, tag) in brown_tags_news)
    print tag_fd.keys()
    # tag_fd.plot(cumulative=True)


def fun2():
    """
    未简化的标记
让我们找出每个名词类型中最频繁的名词。例5-1中的程序找出了所有以NN开始的标记,并为每个标记
提供了几个示例词汇。名词有的变化形式,最重要的含有$的名词所有格,含有S的复数名词(因为复数名词
通常以s结尾),以及含有P的专有名词。此外,大多数的标记都有后缀修饰符:-NC表示引用,-HL表示标
题中的词,-TL表示标题(布朗标记的特征)。
    :return:
    """
    def findtags(tag_prefix, tagged_text):
        cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
                                       if tag.startswith(tag_prefix))
        return dict((tag, cfd[tag].keys()[:5]) for tag in cfd.conditions())

    tagdict = findtags('NN', nltk.corpus.brown.tagged_words(categories='news'))
    for tag in sorted(tagdict):
        print tag, tagdict[tag]


    # 探索已标注的语料库
    # 假设我们正在研究词often, 想看看它是如何在文本中使用的。我们可以试着观察跟在often后面的词汇。
    brown_learned_text = nltk.corpus.brown.words(categories='learned')
    print sorted(set(b for (a, b) in nltk.bigrams(brown_learned_text) if a == 'often'))

    # 然后,使用tagged_words()方法查看跟随词的词性标记可能更有指导性。
    brown_lrnd_tagged = nltk.corpus.brown.tagged_words(categories='learned')
    tags = [b[1] for (a, b) in nltk.bigrams(brown_lrnd_tagged) if a[0] == 'often']
    fd = nltk.FreqDist(tags)
    fd.tabulate()

    # 请注意often后面最高频率的词性是动词。名词从来没有在这个位置出现(在这个特定的语料中)。
    # 接下来,在较大范围的上下文中找出涉及特定标记和词序列的词(在这种情况下,“<Verb>到
    # <Verb>”)。在例5-2中,考虑句子中的每个三词窗口 1 ,检查它们是否符合我们的标准 2 。如果标记匹配,
    # 将输出对应的词 3 。
    from nltk.corpus import brown
    def process(sentence):
        for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(sentence):
            if (t1.startswith('V') and t2 == 'TO' and t3.startswith('V')):
                print w1, w2, w3

    for tagged_sent in brown.tagged_sents():
        process(tagged_sent)

    # 最后,让我们看看与它们的标记关系高度模糊不清的词。要了解为什么要标注这样的词,是因为它们
    # 各自的上下文可以帮助我们弄清楚标记之间的区别。
    brown_news_tagged = brown.tagged_words(categories='news')
    data = nltk.ConditionalFreqDist((word.lower(), tag)
                                    for (word, tag) in brown_news_tagged)
    for word in data.conditions():
        if len(data[word]) > 3:
            tags = data[word].keys()
            print word, ' '.join(tags)



# nltk.download('treebank')
# nltk.download('sinica_treebank')
# nltk.download('indian')
# nltk.download('mac_morpho')
# nltk.download('conll2002')
# nltk.download('cess_cat')
fun2()