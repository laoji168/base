# coding=utf-8
import nltk
"""
2.2条件概率分布
FreqDist()以一个简单的链表作为输入,ConditionalFreqDist()以一个配对链表作为输入
"""
def fun1():
    from nltk.corpus import brown
    # FreqDist()
    cdf = nltk.FreqDist([x for x in brown.words(categories='news')])
    print cdf
    print list(cdf)
    print cdf['stock']
    # ConditionalFreqDist()
    cdf = nltk.ConditionalFreqDist(
        (genre, word)
        for genre in brown.categories()[:2]
        for word in brown.words(categories=genre)[:10]
    )
    print cdf.conditions()
    print cdf['belles_lettres']
    print list(cdf['belles_lettres'])
    print cdf['belles_lettres']['and']
    cdf.plot()


def fun2():
    # 绘制分布图和分布表
    # 条件是词america或citizen 2 ,绘图中的
    # 计数是指在特定演讲中出现该词的次数。它利用了每个演讲的文件名——例如1865-Lincoln.txt——前4个字
    # 符包含了年代信息的特
    # 点 1 。这段代码为文件1865-Lincoln.txt中每个以america小写形式开头的词——
    # 如:Americans——产生一个配对('america', '1865')
    from nltk.corpus import inaugural
    cfd = nltk.ConditionalFreqDist(
        (target, fileid[:4])  # 行， 列
        for fileid in inaugural.fileids()
        for w in inaugural.words(fileid)
        for target in ['america', 'citizen']
        if w.lower().startswith(target)  # 某列中符合条件的单词计数
    )
    cfd.tabulate()
    cfd.plot()


def fun3():
    from nltk.corpus import udhr
    languages = ['Chickasaw', 'English', 'German_Deutsch', 'Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
    cfd = nltk.ConditionalFreqDist(
        (lang, len(word))
        for lang in languages
        for word in udhr.words(lang + '-Latin1')
    )
    # 在plot()和tabulate()方法中,可以使用conditions= 参数来指定显示哪些条件。如果我们忽略它,所有条
    # 件都会显示出来。同样,可以使用samples= 参数来限制要显示的样本。这能将大量数据载入到一个条件频
    # 率分布,然后通过选定条件和样品,对完成的绘图或制表进行探索。这也使我们能全面控制条件和样本的
    # 显示顺序。例如:可以为两种语言和长度少于10个字符的词汇绘制累计频率数据表,如下所示。我们可以
    # 解释最上排最后一个单元格中数值的含义是英文文本中9个或少于9个字符长的词有1638个
    cfd.tabulate(conditions=['English', 'German_Deutsch'], samples=range(10), cumulative=True)
    cfd.plot(conditions=['English', 'German_Deutsch'], samples=range(10), cumulative=True)


def fun4():
    # 处理布朗语料库的新闻和言情文体,找出一周中最有新闻价值并且是最浪漫的日子。定义一个变
    # 量days其中包含星期的链表,如['Monday',
    # ...]。然后使用cfd.tabulate(samples=days)为这些词的计数制
    # 表。接下来用绘图替代制表尝试同样的事情。你可以在另一个参数conditions=['Monday', ...]的帮助下控
    # 制星期输出的顺序。
    from nltk.corpus import brown
    cates = ['news', 'romance']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    cfd = nltk.ConditionalFreqDist(
        (cate, w)
        for cate in cates
        for day in days
        for w in brown.words(categories=cate)
        if w == day
    )
    cfd.tabulate()
    cfd.plot(samples=days)


def fun5():
    # 使用双连词生成随机文本
    # 我们可以使用条件频率分布创建一个双连词表(词对,在1.3节介绍过)。bigrams() 函数能接受一个词
    # 汇链表,并建立起一个连续的词对链表。
    sent = ['In', 'the', 'beginning', 'God', 'created', 'the', 'heaven',
         'and', 'the', 'earth', '.']
    print list(nltk.bigrams(sent))
    # 将每个词作为一个条件,对于每个词都有效地依据后续词的创建频率分布。函数
    # generate_model()包含简单的循环以生成文本。在调用函数时,选择一个词(如living”)作为初始内容。进
    # 入循环后,输入变量word的当前值,重新设置word为上下文中最可能的标识符(使用max())。下一次进入
    # 循环时,将这个词作为新的初始内容。通过检查输出可以发现,这种简单的文本生成方法往往会在循环中
    # 卡住。另一种方法是从可用的词汇中随机选择下一个词
    def generate_model(cfdlist, word, num=15):
        for i in range(num):
            print word
            word = cfdlist[word].max()
    text = nltk.corpus.genesis.words('english-kjv.txt')
    bigrams = nltk.bigrams(text)
    cfd = nltk.ConditionalFreqDist(bigrams)
    print cfd['living']
    print generate_model(cfd, 'living')


def fun6():
    # 英文变复数
    def plural(word):
        if word.endswith('y'):
            return word[:-1] + 'ies'
        elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
            return word + 'es'
        elif word.endswith('an'):
            return word[:-2] + 'en'
        else:
            return word + 's'

# nltk.download('genesis')
fun5()